#!/usr/bin/env bash
# =========================================================================
# PREDATOR System 1 (Defender) Network Hardening Script - Linux iptables/UFW
# Ticket 11: Network Hardening & Validation
# =========================================================================

set -euo pipefail

WHITELIST_PORTS=(3000 8000 8080 9000)

echo "[+] Hardening System 1 Firewall (Linux iptables)..."

# Ensure root
if [ "$EUID" -ne 0 ]; then
    echo "[-] Please run as root (sudo bash iptables_rules.sh)"
    exit 1
fi

# If UFW is active, configure via UFW
if command -v ufw >/dev/null 2>&1 && ufw status | grep -q "Status: active"; then
    echo "[*] UFW detected. Applying port whitelists via UFW..."
    for port in "${WHITELIST_PORTS[@]}"; do
        ufw allow "${port}/tcp" comment "PREDATOR Port ${port}"
        echo "    [✓] UFW Allowed TCP ${port}"
    done
    echo "[+] UFW rules updated."
    exit 0
fi

# Fallback: Raw iptables rules
echo "[*] Applying raw iptables firewall rules..."

# 1. Allow established and loopback traffic
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -i lo -j ACCEPT

# 2. Allow only PREDATOR whitelisted ports
for port in "${WHITELIST_PORTS[@]}"; do
    iptables -A INPUT -p tcp --dport "${port}" -m conntrack --ctstate NEW -j ACCEPT
    echo "    [✓] iptables Allowed Inbound TCP Port ${port}"
done

# 3. Allow ping (ICMP) for lab connectivity diagnostic
iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT

# 4. Reject all other unsolicited incoming connections from LAN
iptables -A INPUT -p tcp -j REJECT --reject-with tcp-reset
iptables -A INPUT -j DROP

echo "[+] System 1 iptables hardening active. Non-whitelisted ports blocked."
