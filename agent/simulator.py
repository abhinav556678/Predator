import time
import os
import random
import string
import socket
import argparse
import threading

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def simulate_failed_logins(attempts=5, delay=1.0):
    print(f"[*] Simulating {attempts} failed login attempts...")
    for i in range(attempts):
        print(f"   [!] Failed login attempt {i+1}/{attempts} for user 'admin' from 192.168.1.100")
        # To make this visible to net_connections telemetry if needed, we could make dummy outbound connections to port 22
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect(("192.168.1.100", 22))
            s.close()
        except:
            pass
        time.sleep(delay)
    print("[*] Failed logins simulation complete.")

def simulate_ransomware(watch_dir="dummy_sensitive_files", num_files=10, delay=0.1):
    print(f"[*] Simulating ransomware in '{watch_dir}'...")
    os.makedirs(watch_dir, exist_ok=True)
    
    # Create some dummy files
    files = []
    for _ in range(num_files):
        fname = os.path.join(watch_dir, f"doc_{generate_random_string(5)}.txt")
        with open(fname, 'w') as f:
            f.write("Important sensitive data.")
        files.append(fname)
        
    time.sleep(1) # Let agent register creations
    
    # Rapidly modify them
    print("   [!] Encrypting files rapidly...")
    for fname in files:
        with open(fname, 'w') as f:
            f.write(generate_random_string(100)) # "Encrypted" content
        # Rename to .encrypted
        os.rename(fname, fname + ".encrypted")
        time.sleep(delay)
        
    print("[*] Ransomware simulation complete.")

def run_port_scan(target_ip, target_ports=[80, 443, 22, 21, 3306], delay=0.5):
    print(f"[*] Simulating port scan against {target_ip}...")
    for port in target_ports:
        print(f"   [!] Scanning port {port}...")
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect((target_ip, port))
            print(f"      - Port {port} is OPEN")
            s.close()
        except (socket.timeout, ConnectionRefusedError):
            print(f"      - Port {port} is CLOSED")
        except Exception as e:
            print(f"      - Error scanning port {port}: {e}")
        time.sleep(delay)
    print("[*] Port scan simulation complete.")

def main():
    parser = argparse.ArgumentParser(description="PREDATOR Attack Simulator")
    parser.add_argument("--watch-dir", type=str, default="dummy_sensitive_files", help="Directory to target for ransomware simulation")
    parser.add_argument("--target", type=str, default="127.0.0.1", help="Target IP for port scan (e.g. M4 Deception Server)")
    parser.add_argument("--all", action="store_true", help="Run all simulations")
    
    args = parser.parse_args()

    print("=== PREDATOR Attack Simulator ===")
    
    if args.all:
        simulate_failed_logins()
        time.sleep(2)
        simulate_ransomware(args.watch_dir)
        time.sleep(2)
        run_port_scan(args.target)
    else:
        print("No specific attack chosen. Running all by default for demonstration...")
        simulate_failed_logins()
        time.sleep(2)
        simulate_ransomware(args.watch_dir)
        time.sleep(2)
        run_port_scan(args.target)

if __name__ == "__main__":
    main()
