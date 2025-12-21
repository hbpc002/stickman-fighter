#!/usr/bin/env python3
import os, sys, base64, json
from urllib.request import Request, urlopen
from urllib.error import HTTPError

# Configuration
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO_OWNER = "hbpc002"
REPO_NAME = "stickman-fighter"
FILES = ["app.py", "app_enhanced.py", "test_game.py", "stickman_fighter.py", "start.sh", "QUICK_DEPLOY.md", "PROJECT_SUMMARY.md", "MOBILE_UPDATE.md"]

# Check token
if not GITHUB_TOKEN:
    print("ERROR: GITHUB_TOKEN not set")
    print("Run: export GITHUB_TOKEN='your_token'")
    sys.exit(1)

print("="*60)
print("GitHub Upload - Stickman Fighter Mobile Enhanced")
print("="*60)
print(f"Repository: {REPO_OWNER}/{REPO_NAME}")
print(f"Files: {len(FILES)}")
print("-"*60)

success = 0
for fp in FILES:
    try:
        # Read file
        with open(fp, "rb") as f:
            content = base64.b64encode(f.read()).decode("utf-8")

        # Check existing
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{fp}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}

        sha = None
        try:
            with urlopen(Request(url, headers=headers)) as r:
                sha = json.loads(r.read()).get("sha")
        except HTTPError:
            pass

        # Upload
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

print("-"*60)
print(f"Complete: {success}/{len(FILES)} files uploaded")
if success == len(FILES):
    print(f"View: https://github.com/{REPO_OWNER}/{REPO_NAME}")
