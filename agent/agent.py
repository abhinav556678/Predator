import time
import json
import requests
import socket
from datetime import datetime, timezone
import argparse
import psutil
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

class FileMonitorHandler(FileSystemEventHandler):
    def __init__(self):
        self.events = []
        self.lock = threading.Lock()

    def on_modified(self, event):
        if not event.is_directory:
            with self.lock:
                self.events.append({"type": "modified", "path": event.src_path, "timestamp": datetime.now(timezone.utc).isoformat()})

    def on_created(self, event):
        if not event.is_directory:
            with self.lock:
                self.events.append({"type": "created", "path": event.src_path, "timestamp": datetime.now(timezone.utc).isoformat()})

    def on_deleted(self, event):
        if not event.is_directory:
            with self.lock:
                self.events.append({"type": "deleted", "path": event.src_path, "timestamp": datetime.now(timezone.utc).isoformat()})

    def get_events(self):
        with self.lock:
            events = list(self.events)
            self.events.clear()
            return events

class Agent:
    def __init__(self, backend_url, interval, watch_dir):
        self.backend_url = backend_url
        self.interval = interval
        self.watch_dir = watch_dir
        self.source_ip = self.get_local_ip()
        self.last_pids = set(psutil.pids())
        
        # Setup File Watcher
        os.makedirs(self.watch_dir, exist_ok=True)
        self.file_handler = FileMonitorHandler()
        self.observer = Observer()
        self.observer.schedule(self.file_handler, self.watch_dir, recursive=True)
        
    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"
            
    def get_new_processes(self):
        current_pids = set(psutil.pids())
        new_pids = current_pids - self.last_pids
        self.last_pids = current_pids
        
        processes = []
        for pid in new_pids:
            try:
                p = psutil.Process(pid)
                processes.append({
                    "pid": pid,
                    "name": p.name(),
                    "cmdline": p.cmdline()
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return processes

    def get_network_connections(self):
        conns = []
        try:
            for c in psutil.net_connections(kind='inet'):
                if c.status == 'ESTABLISHED':
                    laddr = f"{c.laddr.ip}:{c.laddr.port}" if c.laddr else ""
                    raddr = f"{c.raddr.ip}:{c.raddr.port}" if c.raddr else ""
                    conns.append({
                        "fd": c.fd,
                        "family": c.family.name if hasattr(c.family, 'name') else c.family,
                        "type": c.type.name if hasattr(c.type, 'name') else c.type,
                        "laddr": laddr,
                        "raddr": raddr,
                        "status": c.status,
                        "pid": c.pid
                    })
        except (psutil.AccessDenied, Exception):
            pass
        return conns

    def collect_telemetry(self):
        file_events = self.file_handler.get_events()
        new_processes = self.get_new_processes()
        net_connections = self.get_network_connections()
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": "OS_TELEMETRY",
            "source_ip": self.source_ip,
            "details": {
                "cpu_usage": psutil.cpu_percent(interval=None),
                "memory_usage": psutil.virtual_memory().percent,
                "file_events": file_events,
                "new_processes": new_processes,
                "network_connections": net_connections[:50]
            }
        }

    def send_event(self, payload):
        url = f"{self.backend_url.rstrip('/')}/events"
        try:
            response = requests.post(url, json=payload, timeout=5)
            response.raise_for_status()
            print(f"[{payload['timestamp']}] Successfully sent event with {len(payload['details']['file_events'])} file events, {len(payload['details']['new_processes'])} new processes.")
            return True
        except requests.exceptions.RequestException as e:
            print(f"[{payload['timestamp']}] Failed to send event to {url}: {e}")
            return False

    def run(self):
        self.observer.start()
        print(f"Started monitoring directory: {self.watch_dir}")
        try:
            while True:
                payload = self.collect_telemetry()
                self.send_event(payload)
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print("\nAgent stopped by user.")
        finally:
            self.observer.stop()
            self.observer.join()

def main():
    parser = argparse.ArgumentParser(description="PREDATOR Agent (OS Telemetry)")
    parser.add_argument("--backend", type=str, default="http://127.0.0.1:8000", help="URL of the PREDATOR backend")
    parser.add_argument("--interval", type=int, default=5, help="Interval in seconds between events")
    parser.add_argument("--watch-dir", type=str, default="dummy_sensitive_files", help="Directory to monitor for file changes")
    args = parser.parse_args()

    print(f"Starting PREDATOR Agent...")
    print(f"Backend URL: {args.backend}")
    print(f"Interval: {args.interval} seconds")
    print("-" * 40)
    
    agent = Agent(args.backend, args.interval, args.watch_dir)
    agent.run()

if __name__ == "__main__":
    main()
