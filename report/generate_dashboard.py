import json
from pathlib import Path

def load(path):
    try:
        return json.loads(Path(path).read_text())
    except Exception as e:
        return {"error": f"Could not load {path}: {e}"}

bandit = load("report/bandit.json")
gitleaks = load("report/gitleaks.json")
trivy = load("report/trivy.json")

html = f"""
<html>
<head><title>Security Dashboard</title></head>
<body>
<h1>🔐 Security Scan Results</h1>

<h2>Bandit</h2>
<pre>{json.dumps(bandit, indent=2)}</pre>

<h2>Gitleaks</h2>
<pre>{json.dumps(gitleaks, indent=2)}</pre>

<h2>Trivy</h2>
<pre>{json.dumps(trivy, indent=2)}</pre>

</body>
</html>
"""

Path("report/index.html").write_text(html)
