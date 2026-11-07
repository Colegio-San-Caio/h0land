#!/usr/bin/env python3
# h0land v1 - Repo Health Tool
# Usage: python h0land.py check
#        python h0land.py green

import os
import subprocess
import sys

VERSION = "h0land v1 - Cluster h0land"

def run(cmd, cwd):
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=10)
        return r.stdout.strip()
    except Exception:
        return ""

def check_repo(name, path, expected_files=None):
    print(f"\n--- {name} ---")
    if not os.path.isdir(path):
        print(f"🔴 MISSING - folder not found: {path}")
        return False

    # git commit
    commit = run(["git", "rev-parse", "--short", "HEAD"], path)
    # git status clean?
    status = run(["git", "status", "--porcelain"], path)
    dirty = "DIRTY - uncommitted changes" if status else "CLEAN"

    # count files, ignore .git
    total = 0
    for root, dirs, files in os.walk(path):
        if ".git" in root:
            continue
        dirs[:] = [d for d in dirs if d != ".git"]
        total += len(files)

    print(f"Path: {path}")
    print(f"Commit: {commit} - {dirty}")
    print(f"Files: {total}")

    if expected_files and total < expected_files:
        print(f"🔴 FAIL - expected at least {expected_files}, got {total}")
        return False

    if status:
        print(f"🟡 WARN - repo has uncommitted changes")
        return True

    print(f"🟢 OK")
    return True

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ["check", "green"]:
        print(VERSION)
        print("Usage: python h0land.py check")
        print("       python h0land.py green")
        return

    home = os.path.expanduser("~")
    # Adjust these if your clones are elsewhere
    site_path = os.path.join(home, "site-index")
    gold_path = os.path.join(home, "GOLD")

    # Try alternative locations if not found
    if not os.path.isdir(site_path):
        site_path = os.path.join(home, "kaiolafketelhut.github.io")
    if not os.path.isdir(gold_path):
        gold_path = os.path.join(home, "Colegio-San-Caio", "GOLD")

    print(VERSION)

    site_ok = check_repo("site-index - 1 Main = 1 Truth", site_path)
    gold_ok = check_repo("GOLD - Vault", gold_path, expected_files=320)

    print("\n--- RESULT ---")
    if site_ok and gold_ok:
        print("🟢 h0land GREEN - Both repos healthy")
    elif site_ok or gold_ok:
        print("🟡 h0land YELLOW - One repo needs attention")
    else:
        print("🔴 h0land RED - Both repos failing")

if __name__ == "__main__":
    main()
