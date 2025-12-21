#!/usr/bin/env python3
import os, sys, base64, json
from urllib.request import Request, urlopen
from urllib.error import HTTPError

# Get token
token = os.environ.get("GITHUB_TOKEN", "")
print(f"Token check: {'SET' if token else 'NOT SET'}")

if not token:
    print("Please set: export GITHUB_TOKEN='your_token'")
    sys.exit(1)

# Upload config
repo_owner, repo_name = "hbpc002", "stickman-fighter"
files = ["app.py", "app_enhanced.py", "test_game.py", "stickman_fighter.py", "start.sh", "QUICK_DEPLOY.md", "PROJECT_SUMMARY.md", "MOBILE_UPDATE.md"]

print(f"\nUploading {len(files)} files to {repo_owner}/{repo_name}...")

success = 0
for fp in files:
    try:
        with open(fp, "rb") as f:
            content = base64.b64encode(f.read()).decode("utf-8")

        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{fp}"
        headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}

        sha = None
        try:
            with urlopen(Request(url, headers=headers)) as r:
                sha = json.loads(r.read()).get("sha")
        except HTTPError:
            pass

        action = "update" if sha else "create"
        msg = f"{action.capitalize()} {fp} - Add mobile support with virtual keyboard"
        data = {"message": msg, "content": content}
        if sha:
            data["sha"] = sha

        with urlopen(Request(url, data=json.dumps(data).encode("utf-8"), headers=headers, method="PUT")):
            print(f"✓ {action.upper()}: {fp}")
            success += 1
    except Exception as e:
        print(f"✗ FAILED: {fp} - {e}")

print(f"\nResult: {success}/{len(files)} files uploaded")
if success == len(files):
    print(f"View: https://github.com/{repo_owner}/{repo_name}")
