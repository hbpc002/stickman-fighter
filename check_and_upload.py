#!/usr/bin/env python3
import os
import sys
import base64
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError

# Check token first
github_token = os.environ.get("GITHUB_TOKEN")
print(f"GITHUB_TOKEN: {'SET' if github_token else 'NOT SET'}")

if not github_token:
    print("\nPlease set GITHUB_TOKEN environment variable:")
    print("  export GITHUB_TOKEN='your_github_token_here'")
    sys.exit(1)

# Configuration
REPO_OWNER = "hbpc002"
REPO_NAME = "stickman-fighter"

# Files to upload
FILES_TO_UPLOAD = [
    "app.py",
    "app_enhanced.py",
    "test_game.py",
    "stickman_fighter.py",
    "start.sh",
    "QUICK_DEPLOY.md",
    "PROJECT_SUMMARY.md",
    "MOBILE_UPDATE.md",
]

def get_file_content(filepath):
    with open(filepath, "rb") as f:
        content = f.read()
    return base64.b64encode(content).decode("utf-8")

def get_github_file_sha(filepath):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{filepath}"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    try:
        req = Request(url, headers=headers)
        with urlopen(req) as response:
            data = json.loads(response.read())
            return data.get("sha")
    except HTTPError as e:
        if e.code == 404:
            return None
        print(f"Error checking {filepath}: {e}")
        return None

def upload_file(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return False

    sha = get_github_file_sha(filepath)
    content = get_file_content(filepath)

    if sha:
        action = "update"
        message = f"Update {filepath} - Add mobile support with virtual keyboard"
    else:
        action = "create"
        message = f"Add {filepath} - Mobile support with virtual keyboard"

    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{filepath}"
    data = {"message": message, "content": content}
    if sha:
        data["sha"] = sha

    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        req = Request(url, data=json.dumps(data).encode("utf-8"), headers=headers, method="PUT")
        with urlopen(req) as response:
            result = json.loads(response.read())
            print(f"✓ {action.upper()}: {filepath}")
            return True
    except HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"✗ FAILED: {filepath}")
        print(f"  Error: {e.code} - {error_body}")
        return False

print("\n" + "="*60)
print("GitHub Upload - Stickman Fighter Mobile Enhanced")
print("="*60)
print(f"\nRepository: {REPO_OWNER}/{REPO_NAME}")
print(f"Files to upload: {len(FILES_TO_UPLOAD)}")
print("\nUploading files...")
print("-"*60)

success_count = 0
for filepath in FILES_TO_UPLOAD:
    if upload_file(filepath):
        success_count += 1

print("-"*60)
print(f"\nComplete: {success_count}/{len(FILES_TO_UPLOAD)} files uploaded successfully")

if success_count == len(FILES_TO_UPLOAD):
    print("\n✓ All files uploaded to GitHub!")
    print(f"\nView at: https://github.com/{REPO_OWNER}/{REPO_NAME}")
else:
    print(f"\n⚠ {len(FILES_TO_UPLOAD) - success_count} files failed to upload")
    sys.exit(1)
