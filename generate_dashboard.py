import json
from pathlib import Path
from collections import Counter

def load_json(path):
    try:
        return json.loads(Path(path).read_text())
    except Exception as e:
        return {"error": f"Could not load {path}: {e}"}

def bandit_metrics(data):
    try:
        results = data.get("results", [])
        severities = [r.get("issue_severity", "UNKNOWN") for r in results]
        count = Counter(severities)
        return len(results), count
    except:
        return 0, {}
        raise

def trivy_metrics(data):
    try:
        results = data.get("Results", [])
        all_vulns = []
        for res in results:
            all_vulns.extend(res.get("Vulnerabilities", []))
        severities = [v.get("Severity", "UNKNOWN") for v in all_vulns]
        count = Counter(severities)
        return len(all_vulns), count
    except:
        return 0, {}
        raise

def gitleaks_metrics(data):
    try:
        results = data if isinstance(data, list) else data.get("results", [])
        return len(results)
    except:
        return 0
        raise

bandit_data = load_json("report/bandit.json")
trivy_data = load_json("report/trivy.json")
gitleaks_data = load_json("report/gitleaks.json")

bandit_count, bandit_severities = bandit_metrics(bandit_data)
trivy_count, trivy_severities = trivy_metrics(trivy_data)
gitleaks_count = gitleaks_metrics(gitleaks_data)

# Build HTML
html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>DevSecOps Security Dashboard</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 2em; }}
        h1 {{ color: #333; }}
        .section {{ margin-bottom: 3em; }}
        table {{
            border-collapse: collapse;
            width: 60%;
        }}
        th, td {{
            text-align: left;
            padding: 8px;
            border: 1px solid #ccc;
        }}
        th {{
            background-color: #f2f2f2;
        }}
    </style>
</head>
<body>
<h1>🔐 DevSecOps Security Dashboard</h1>

<div class="section">
    <h2>📦 Bandit (Python Code Scan)</h2>
    <p>Total Issues: <strong>{bandit_count}</strong></p>
    <table>
        <tr><th>Severity</th><th>Count</th></tr>
        {''.join(f"<tr><td>{s}</td><td>{c}</td></tr>" for s, c in bandit_severities.items())}
    </table>
</div>

<div class="section">
    <h2>🛡️ Trivy (File Vulnerabilities)</h2>
    <p>Total Issues: <strong>{trivy_count}</strong></p>
    <table>
        <tr><th>Severity</th><th>Count</th></tr>
        {''.join(f"<tr><td>{s}</td><td>{c}</td></tr>" for s, c in trivy_severities.items())}
    </table>
</div>

<div class="section">
    <h2>🔑 Gitleaks (Secrets Detection)</h2>
    <p>Total Secrets Found: <strong>{gitleaks_count}</strong></p>
</div>

</body>
</html>
"""

# Save HTML to file
Path("report/index.html").write_text(html, encoding="utf-8")
