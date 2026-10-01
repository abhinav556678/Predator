"""
PREDATOR Deception Subsystem - Realistic Decoy Corporate Intranet Templates
Renders authentic-looking enterprise portal interfaces to entice attackers.
"""

def get_login_page_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Apex Global Financial — Corporate Intranet Gateway</title>
    <style>
        :root {
            --bg-color: #0d1117;
            --card-bg: #161b22;
            --border-color: #30363d;
            --accent-blue: #2f81f7;
            --text-main: #e6edf3;
            --text-muted: #8b949e;
            --warning-badge: #d29922;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .header-bar {
            position: absolute;
            top: 0; left: 0; right: 0;
            background: #010409;
            border-bottom: 1px solid var(--border-color);
            padding: 14px 28px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .logo-area { display: flex; align-items: center; gap: 10px; font-weight: 700; font-size: 1.15rem; letter-spacing: 0.5px; }
        .logo-badge { background: #238636; color: #fff; font-size: 0.72rem; padding: 2px 7px; border-radius: 12px; }
        .sys-id { color: var(--text-muted); font-size: 0.85rem; font-family: monospace; }
        .login-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            width: 100%;
            max-width: 440px;
            padding: 32px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            margin-top: 50px;
        }
        .login-title { font-size: 1.4rem; font-weight: 600; margin-bottom: 8px; }
        .login-subtitle { font-size: 0.88rem; color: var(--text-muted); margin-bottom: 24px; line-height: 1.4; }
        .form-group { margin-bottom: 18px; }
        label { display: block; font-size: 0.85rem; font-weight: 500; margin-bottom: 6px; color: var(--text-main); }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 10px 12px;
            background: #0d1117;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            color: #fff;
            font-size: 0.95rem;
            outline: none;
            transition: border-color 0.2s;
        }
        input[type="text"]:focus, input[type="password"]:focus {
            border-color: var(--accent-blue);
            box-shadow: 0 0 0 3px rgba(47, 129, 247, 0.25);
        }
        .btn-submit {
            width: 100%;
            padding: 11px;
            background: #238636;
            color: #fff;
            border: none;
            border-radius: 6px;
            font-size: 0.95rem;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
            margin-top: 10px;
        }
        .btn-submit:hover { background: #2ea043; }
        .banner-warning {
            background: rgba(210, 153, 34, 0.12);
            border: 1px solid rgba(210, 153, 34, 0.4);
            border-radius: 6px;
            padding: 12px;
            margin-top: 24px;
            font-size: 0.78rem;
            color: #e3b341;
            line-height: 1.45;
        }
        .portal-links {
            margin-top: 24px;
            border-top: 1px solid var(--border-color);
            padding-top: 18px;
            font-size: 0.82rem;
            color: var(--text-muted);
        }
        .portal-links a { color: var(--accent-blue); text-decoration: none; margin-right: 14px; }
        .portal-links a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <header class="header-bar">
        <div class="logo-area">
            <span>🛡️ APEX GLOBAL FINANCIAL</span>
            <span class="logo-badge">SECURE INTRANET</span>
        </div>
        <div class="sys-id">ZONE: CORE-FIN-PROD-VLAN100</div>
    </header>

    <div class="login-card">
        <h1 class="login-title">Employee Single Sign-On</h1>
        <p class="login-subtitle">Restricted gateway for Apex Global Financial staff and internal operations.</p>

        <form action="/login" method="POST">
            <div class="form-group">
                <label for="username">Username or Corporate Email</label>
                <input type="text" id="username" name="username" placeholder="e.g. jdoe@apexfinancial.local" required autocomplete="username" autofocus>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" placeholder="••••••••••••" required autocomplete="current-password">
            </div>
            <button type="submit" class="btn-submit">Sign In to Enterprise Portal</button>
        </form>

        <div class="banner-warning">
            <strong>NOTICE:</strong> Authorized personnel only. All access, session tokens, and query commands are monitored and audited under Corporate Defense Policy SEC-881.
        </div>

        <div class="portal-links">
            <div>Internal Resources:</div>
            <div style="margin-top: 6px;">
                <a href="/portal">Employee Portal</a>
                <a href="/api/v1/users">User Directory</a>
                <a href="/api/v1/finance/records">Finance Ledger</a>
                <a href="/documents">Documents</a>
                <a href="/admin">Admin Console</a>
            </div>
        </div>
    </div>
</body>
</html>"""


def get_dashboard_html(username: str = "Authorized Analyst") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Apex Global Financial — Internal Management Dashboard</title>
    <style>
        :root {{
            --bg-color: #0b0f14;
            --panel-bg: #151b23;
            --border-color: #2b323b;
            --accent: #2f81f7;
            --text-main: #f0f6fc;
            --text-dim: #8b949e;
            --success: #3fb950;
            --warning: #d29922;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
        body {{ background: var(--bg-color); color: var(--text-main); min-height: 100vh; padding: 24px; }}
        .navbar {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); padding-bottom: 16px; margin-bottom: 24px; }}
        .brand {{ font-size: 1.25rem; font-weight: 700; display: flex; align-items: center; gap: 8px; }}
        .user-tag {{ font-size: 0.85rem; color: var(--text-dim); background: #21262d; padding: 6px 12px; border-radius: 20px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; }}
        .card {{ background: var(--panel-bg); border: 1px solid var(--border-color); border-radius: 8px; padding: 20px; }}
        .card-header {{ font-size: 1.05rem; font-weight: 600; margin-bottom: 12px; display: flex; justify-content: space-between; }}
        .stat {{ font-size: 1.8rem; font-weight: 700; color: var(--accent); margin-bottom: 4px; }}
        .links-list {{ list-style: none; margin-top: 12px; }}
        .links-list li {{ padding: 8px 0; border-bottom: 1px solid #21262d; }}
        .links-list a {{ color: var(--accent); text-decoration: none; font-size: 0.9rem; }}
        .links-list a:hover {{ text-decoration: underline; }}
        .btn {{ display: inline-block; padding: 8px 14px; background: #238636; color: #fff; text-decoration: none; border-radius: 6px; font-size: 0.85rem; font-weight: 600; margin-top: 12px; }}
        .code-box {{ background: #010409; padding: 12px; border-radius: 6px; font-family: monospace; font-size: 0.82rem; color: #7ee787; overflow-x: auto; }}
    </style>
</head>
<body>
    <div class="navbar">
        <div class="brand">🛡️ APEX GLOBAL FINANCIAL — INTRANET PORTAL</div>
        <div class="user-tag">User: {username} | Status: Authenticated</div>
    </div>

    <div class="grid">
        <div class="card">
            <div class="card-header">
                <span>Corporate Treasury Ledger</span>
                <span style="color: var(--success); font-size: 0.85rem;">Active Q3/Q4</span>
            </div>
            <div class="stat">$3,342,000.50</div>
            <p style="color: var(--text-dim); font-size: 0.85rem;">Total tracked offshore & domestic wire settlements</p>
            <ul class="links-list">
                <li><a href="/api/v1/finance/records">View Raw JSON Ledger Feed &rarr;</a></li>
                <li><a href="/documents/q3_confidential_financials.csv">Download Q3 Financials (.CSV) &rarr;</a></li>
            </ul>
        </div>

        <div class="card">
            <div class="card-header">
                <span>Enterprise User Directory</span>
                <span style="color: var(--accent); font-size: 0.85rem;">5 Identities</span>
            </div>
            <p style="color: var(--text-dim); font-size: 0.85rem;">Identity credentials, active API bearer tokens & roles.</p>
            <ul class="links-list">
                <li><a href="/api/v1/users">REST Endpoint: /api/v1/users &rarr;</a></li>
                <li><a href="/api/v1/credentials">View Secrets & Token Vault &rarr;</a></li>
            </ul>
        </div>

        <div class="card">
            <div class="card-header">
                <span>Core Infrastructure & Network</span>
                <span style="color: var(--warning); font-size: 0.85rem;">VLAN 100 DMZ</span>
            </div>
            <p style="color: var(--text-dim); font-size: 0.85rem;">Internal host inventory & network architecture diagrams.</p>
            <ul class="links-list">
                <li><a href="/api/v1/servers">Server Inventory Asset API &rarr;</a></li>
                <li><a href="/documents/network_topology_confidential.txt">Confidential Network Topology &rarr;</a></li>
                <li><a href="/documents/vpn_passwords_internal.txt">Emergency IT VPN Credentials &rarr;</a></li>
            </ul>
        </div>

        <div class="card">
            <div class="card-header">
                <span>Database Administration Console</span>
                <span style="color: var(--accent); font-size: 0.85rem;">SQLite Engine</span>
            </div>
            <p style="color: var(--text-dim); font-size: 0.85rem; margin-bottom: 10px;">Execute internal diagnostic queries on `fake_corporate.db`.</p>
            <a href="/admin" class="btn">Launch SQL Explorer Console &rarr;</a>
        </div>
    </div>
</body>
</html>"""


def get_admin_sql_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Apex Financial — Internal Database Explorer</title>
    <style>
        :root {
            --bg: #0d1117; --card: #161b22; --border: #30363d; --text: #e6edf3;
            --accent: #58a6ff; --code: #7ee787;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: monospace; }
        body { background: var(--bg); color: var(--text); padding: 24px; }
        .container { max-width: 900px; margin: 0 auto; }
        h1 { font-size: 1.3rem; margin-bottom: 8px; color: var(--accent); }
        p { font-size: 0.85rem; color: #8b949e; margin-bottom: 16px; }
        textarea {
            width: 100%; height: 120px; background: #010409; color: var(--code);
            border: 1px solid var(--border); border-radius: 6px; padding: 12px;
            font-size: 0.95rem; resize: vertical; outline: none; margin-bottom: 12px;
        }
        button {
            padding: 10px 18px; background: #238636; color: #fff; border: none;
            border-radius: 6px; font-weight: 700; cursor: pointer; font-size: 0.9rem;
        }
        button:hover { background: #2ea043; }
        #results { margin-top: 20px; background: #010409; border: 1px solid var(--border); border-radius: 6px; padding: 16px; font-size: 0.85rem; min-height: 80px; overflow-x: auto; }
        table { border-collapse: collapse; width: 100%; margin-top: 10px; }
        th, td { border: 1px solid var(--border); padding: 6px 10px; text-align: left; }
        th { background: #161b22; color: var(--accent); }
        .sample-queries { margin-top: 16px; font-size: 0.8rem; color: #8b949e; }
        .sample-queries span { color: var(--code); cursor: pointer; text-decoration: underline; margin-right: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>SQL Query Diagnostic Console [INTERNAL IT ONLY]</h1>
        <p>Direct query access to `fake_corporate.db` (Tables: `users`, `finance_records`, `server_inventory`, `credentials_vault`)</p>

        <textarea id="sqlQuery" placeholder="SELECT * FROM users;"></textarea>
        <div>
            <button onclick="runQuery()">Execute Query</button>
            <a href="/portal" style="color: var(--accent); margin-left: 16px; text-decoration: none;">&larr; Back to Portal</a>
        </div>

        <div class="sample-queries">
            Quick Queries:
            <span onclick="setQ('SELECT * FROM users;')">users</span>
            <span onclick="setQ('SELECT * FROM finance_records;')">finance_records</span>
            <span onclick="setQ('SELECT * FROM credentials_vault;')">credentials_vault</span>
            <span onclick="setQ('SELECT * FROM server_inventory;')">server_inventory</span>
        </div>

        <div id="results">Execution results will appear here...</div>
    </div>

    <script>
        function setQ(q) { document.getElementById('sqlQuery').value = q; }
        async function runQuery() {
            const sql = document.getElementById('sqlQuery').value;
            const resDiv = document.getElementById('results');
            resDiv.innerHTML = "Executing query against database...";
            try {
                const resp = await fetch('/api/v1/query', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: sql })
                });
                const data = await resp.json();
                if (!data.success) {
                    resDiv.innerHTML = `<div style="color: #f85149;">Error: ${data.message}</div>`;
                    return;
                }
                if (data.rows.length === 0) {
                    resDiv.innerHTML = `<div style="color: #8b949e;">Query executed. 0 rows returned.</div>`;
                    return;
                }
                const headers = Object.keys(data.rows[0]);
                let tableHtml = '<table><thead><tr>' + headers.map(h => `<th>${h}</th>`).join('') + '</tr></thead><tbody>';
                data.rows.forEach(row => {
                    tableHtml += '<tr>' + headers.map(h => `<td>${row[h] !== null ? row[h] : 'NULL'}</td>`).join('') + '</tr>';
                });
                tableHtml += '</tbody></table>';
                resDiv.innerHTML = `<div style="color: #7ee787; margin-bottom: 8px;">✓ ${data.message} (${data.rows.length} rows)</div>` + tableHtml;
            } catch (err) {
                resDiv.innerHTML = `<div style="color: #f85149;">Connection error: ${err.message}</div>`;
            }
        }
    </script>
</body>
</html>"""
