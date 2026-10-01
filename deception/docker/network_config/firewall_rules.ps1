<#
.SYNOPSIS
    PREDATOR System 1 (Defender) Network Hardening Script - Windows Firewall
    Ticket 11: Network Hardening & Validation

.DESCRIPTION
    Configures Windows Defender Firewall on System 1 to only permit required ports:
      - Port 3000: React SOC Frontend Dashboard
      - Port 8000: FastAPI Central Backend & Event Ingestion
      - Port 8080: Deception HTTP Portal & Honeypot (Primary)
      - Port 9000: Deception Alternate Port (Secondary)
    All other inbound traffic on unlisted ports is blocked from external LAN sources.

.PARAMETER Action
    Specifies 'apply', 'remove', or 'status'. Default is 'status'.
#>

param(
    [ValidateSet("apply", "remove", "status")]
    [string]$Action = "status"
)

$WhitelistedPorts = @(
    @{ Name = "PREDATOR-Allow-Frontend-3000"; Port = 3000; Protocol = "TCP"; Description = "PREDATOR SOC React UI" },
    @{ Name = "PREDATOR-Allow-Backend-8000";  Port = 8000; Protocol = "TCP"; Description = "PREDATOR FastAPI Hub & Telemetry Ingestion" },
    @{ Name = "PREDATOR-Allow-Deception-8080"; Port = 8080; Protocol = "TCP"; Description = "PREDATOR Deception Honeypot Server (Primary)" },
    @{ Name = "PREDATOR-Allow-Deception-9000"; Port = 9000; Protocol = "TCP"; Description = "PREDATOR Deception Honeypot Server (Secondary)" }
)

function Apply-PredatorFirewallRules {
    Write-Host "[+] Applying PREDATOR System 1 Firewall Hardening Rules..." -ForegroundColor Cyan

    foreach ($rule in $WhitelistedPorts) {
        # Remove existing rule if present
        Remove-NetFirewallRule -DisplayName $rule.Name -ErrorAction SilentlyContinue

        # Create new inbound allow rule
        New-NetFirewallRule -DisplayName $rule.Name `
                            -Direction Inbound `
                            -Action Allow `
                            -Protocol $rule.Protocol `
                            -LocalPort $rule.Port `
                            -Profile Any `
                            -Description $rule.Description | Out-Null

        Write-Host "    [✓] Allowed Inbound Port $($rule.Port) ($($rule.Name))" -ForegroundColor Green
    }

    Write-Host "[+] System 1 Firewall Hardening applied successfully." -ForegroundColor Green
    Write-Host "    Only ports 3000, 8000, 8080, and 9000 are open for presentation/lab traffic." -ForegroundColor Yellow
}

function Remove-PredatorFirewallRules {
    Write-Host "[*] Removing PREDATOR Firewall Rules..." -ForegroundColor Yellow
    foreach ($rule in $WhitelistedPorts) {
        Remove-NetFirewallRule -DisplayName $rule.Name -ErrorAction SilentlyContinue
        Write-Host "    [-] Removed $($rule.Name)" -ForegroundColor Gray
    }
    Write-Host "[✓] All PREDATOR custom rules removed." -ForegroundColor Green
}

function Show-PredatorFirewallStatus {
    Write-Host "`n=== PREDATOR System 1 Active Firewall Rules ===" -ForegroundColor Cyan
    foreach ($rule in $WhitelistedPorts) {
        $existing = Get-NetFirewallRule -DisplayName $rule.Name -ErrorAction SilentlyContinue
        if ($existing) {
            Write-Host "  [ACTIVE]  Port $($rule.Port) - $($rule.Name) (Action: $($existing.Action))" -ForegroundColor Green
        } else {
            Write-Host "  [MISSING] Port $($rule.Port) - $($rule.Name)" -ForegroundColor Red
        }
    }
    Write-Host "`nUse: powershell -ExecutionPolicy Bypass -File firewall_rules.ps1 -Action apply" -ForegroundColor Gray
}

switch ($Action) {
    "apply"  { Apply-PredatorFirewallRules }
    "remove" { Remove-PredatorFirewallRules }
    "status" { Show-PredatorFirewallStatus }
}
