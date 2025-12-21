#!/usr/bin/env python3
import os, sys, base64, json
from urllib.request import Request, urlopen
from urllib.error import HTTPError

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO_OWNER, REPO_NAME = "hbpc002", "stickman-fighter"
FILES = ["app.py", "app_enhanced.py", "test_game.py", "stickman_fighter.py", "start.sh", "QUICK_DEPLOY.md", "PROJECT_SUMMARY.md", "MOBILE_UPDATE.md"]

print("="*60)
print("GitHub Upload - Stickman Fighter Mobile Enhanced")
print("="*60)

if not GITHUB_TOKEN:
    print("\nERROR: GITHUB_TOKEN not set!\n\nSet with: export GITHUB_TOKEN='your_token'")
    sys.exit(1)

print(f"\nRepository: {REPO_OWNER}/{REPO_NAME}")
print(f"Files: {len(FILES)}\n")
print("-"*60)

success = 0
for fp in FILES:
    try:
        with open(fp, "rb") as f:
            content = base64.b64encode(f.read()).decode("utf-8")

        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{fp}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}

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

print("-"*60)
print(f"\nComplete: {success}/{len(FILES)} files uploaded")

if success == len(FILES):
    print("\n✓ All files uploaded to GitHub!")
    print(f"View: https://github.com/{REPO_OWNER}/{REPO_NAME}")
else:
    print(f"\n⚠ {len(FILES) - success} files failed")
