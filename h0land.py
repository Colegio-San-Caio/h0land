#!/usr/bin/env python3
# h0land v2 - Repo Health + Scanner + SARIF
import os, subprocess, sys, json, re

VERSION = "h0land v2 - Cluster h0land"

def run(cmd, cwd):
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=10)
        return r.stdout.strip()
    except Exception:
        return ""

def check_repo(name, path, expected_files=None):
    print(f"\n--- {name} ---")
    if not os.path.isdir(path):
        print(f"RED MISSING - {path}")
        return False
    commit = run(["git", "rev-parse", "--short", "HEAD"], path)
    status = run(["git", "status", "--porcelain"], path)
    dirty = "DIRTY" if status else "CLEAN"
    total = 0
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d != ".git"]
        total += len(files)
    print(f"Path: {path}")
    print(f"Commit: {commit} - {dirty}")
    print(f"Files: {total}")
    if expected_files and total < expected_files:
        print(f"RED FAIL - expected {expected_files}, got {total}")
        return False
    print("GREEN OK" if not status else "YELLOW WARN - uncommitted changes")
    return True

def do_check():
    home = os.path.expanduser("~")
    site_path = os.path.join(home, "site-index")
    gold_path = os.path.join(home, "GOLD")
    if not os.path.isdir(site_path):
        site_path = os.path.join(home, "kaiolafketelhut.github.io")
    print(VERSION)
    a = check_repo("site-index - 1 Main = 1 Truth", site_path)
    b = check_repo("GOLD - Vault", gold_path, expected_files=320)
    print("\n--- RESULT ---")
    print("GREEN h0land GREEN" if a and b else "YELLOW / RED - check above")

def do_scan(target=".", sarif_path="h0land.sarif"):
    patterns = [
        ("H0L001", "Possible secret", r"(password|passwd|api_key|apikey|secret|token)\s*=\s*['\"][^'\"]+['\"]"),
        ("H0L002", "TODO left in code", r"TODO|FIXME|XXX"),
        ("H0L003", "Hardcoded http link", r"http://[^\s\"']+"),
    ]
    results = []
    total_files = 0
    for root, dirs, files in os.walk(target):
        dirs[:] = [d for d in dirs if d not in [".git", "__pycache__", "node_modules"]]
        for f in files:
            if not f.endswith((".py", ".js", ".ts", ".html", ".yml", ".yaml", ".json", ".md", ".txt", ".c", ".cpp", ".java")):
                continue
            total_files += 1
            fp = os.path.join(root, f)
            try:
                with open(fp, errors="ignore") as fh:
                    lines = fh.readlines()
            except Exception:
                continue
            for i, line in enumerate(lines, 1):
                for rule, msg, pat in patterns:
                    if re.search(pat, line, re.IGNORECASE):
                        results.append({
                            "ruleId": rule, "level": "warning" if rule != "H0L001" else "error",
                            "message": {"text": f"{msg}: {line.strip()[:120]}"},
                            "locations": [{"physicalLocation": {"artifactLocation": {"uri": os.path.relpath(fp, target)}, "region": {"startLine": i}}}]
                        })
    print(f"{VERSION} scan")
    print(f"Files scanned: {total_files}")
    print(f"Findings: {len(results)}")
    for r in results[:20]:
        print(f"{r['ruleId']} {r['locations'][0]['physicalLocation']['artifactLocation']['uri']}:{r['locations'][0]['physicalLocation']['region']['startLine']} - {r['message']['text'][:80]}")
    sarif = {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [{"tool": {"driver": {"name": "h0land", "version": "2.0.0", "informationUri": "https://github.com/Colegio-San-Caio/h0land", "rules": [
            {"id": "H0L001", "name": "PossibleSecret", "shortDescription": {"text": "Possible hardcoded secret"}},
            {"id": "H0L002", "name": "TodoLeft", "shortDescription": {"text": "TODO left in code"}},
            {"id": "H0L003", "name": "HttpLink", "shortDescription": {"text": "Hardcoded http link"}},
        ]}}, "results": results}]
    }
    with open(sarif_path, "w") as out:
        json.dump(sarif, out, indent=2)
    print(f"SARIF written: {sarif_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python h0land.py check | scan | green")
        sys.exit(0)
    if sys.argv[1] in ["check", "green"]:
        do_check()
    elif sys.argv[1] == "scan":
        sarif = "h0land.sarif"
        if "--sarif" in sys.argv:
            sarif = sys.argv[sys.argv.index("--sarif")+1]
        target = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else "."
        do_scan(target, sarif)
