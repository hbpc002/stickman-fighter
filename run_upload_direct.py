#!/usr/bin/env python3
# Direct execution of GitHub upload without subprocess

import os
import sys
import base64
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError

# Get token
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

print("="*60)
print("GitHub Upload - Stickman Fighter Mobile Enhanced")
print("="*60)

if not GITHUB_TOKEN:
    print("\nERROR: GITHUB_TOKEN environment variable is not set!")
    print("\nTo fix this, set the token:")
    print("  export GITHUB_TOKEN='your_github_token_here'")
    sys.exit(1)

print(f"\nRepository: hbpc002/stickman-fighter")
print("Files to upload: 8")
print("\nUploading files...")
print("-"*60)

REPO_OWNER = "hbpc002"
REPO_NAME = "stickman-fighter"

FILES = ["app.py", "app_enhanced.py", "test_game.py", "stickman_fighter.py",
         "start.sh", "QUICK_DEPLOY.md", "PROJECT_SUMMARY.md", "MOBILE_UPDATE.md"]

success_count = 0

for filepath in FILES:
    try:
        # Read file
        with open(filepath, "rb") as f:
            content = base64.b64encode(f.read()).decode("utf-8")

        # Check existing
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{filepath}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}

        sha = None
        try:
            with urlopen(Request(url, headers=headers)) as r:
                sha = json.loads(r.read()).get("sha")
        except HTTPError:
            pass

        # Upload
        action = "update" if sha else "create"
        message = f"{action.capitalize()} {filepath} - Add mobile support with virtual keyboard"
        data = {"message": message, "content": content}
        if sha:
            data["sha"] = sha

        req = Request(url, data=json.dumps(data).encode("utf-8"), headers=headers, method="PUT")
        with urlopen(req) as r:
            json.loads(r.read())
            print(f"✓ {action.upper()}: {filepath}")
            success_count += 1

    except Exception as e:
        print(f"✗ FAILED: {filepath} - {e}")

print("-"*60)
print(f"\nComplete: {success_count}/{len(FILES)} files uploaded successfully")

if success_count == len(FILES):
    print("\n✓ All files uploaded to GitHub!")
    print(f"\nView at: https://github.com/{REPO_OWNER}/{REPO_NAME}")
else:
    print(f"\n⚠ {len(FILES) - success_count} files failed to upload")
