import sys, json, pathlib

RULES = [
    ("H0L001", "DangerousEval", r"eval\(|innerHTML\s*="),
    ("H0L002", "TodoLeft", r"TODO|FIXME|XXX"),
    ("H0L003", "HardcodedHttp", r"http://(?!localhost)(?!127\.0\.0\.1)[^\s\"']+"),
]
# only real code files
CODE_EXTS = {".py", ".js", ".ts", ".tsx", ".jsx", ".html", ".css", ".go", ".rs", ".java", ".php"}
SKIP_DIRS = {".git", "docs", "node_modules", "precomputer", "__pycache__", ".github", "v86", "build", "dist"}
SKIP_FILES = {"h0land.py"}

def do_scan(target, sarif):
    import re
    findings = []
    for p in pathlib.Path(target).rglob("*"):
        if not p.is_file(): continue
        if p.suffix not in CODE_EXTS: continue
        if p.name in SKIP_FILES: continue
        if any(part in SKIP_DIRS for part in p.parts): continue
        try: text = p.read_text(errors="ignore")
        except: continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for rid, name, pat in RULES:
                if re.search(pat, line):
                    findings.append((rid, name, str(p), lineno, line.strip()[:120]))
    print(f"Files scanned: {target}")
    print(f"Findings: {len(findings)}")
    for rid, name, f, ln, msg in findings:
        print(f"{rid} {f}:{ln} - {msg}")
    # SARIF
    rules = [{"id": r[0], "name": r[1], "shortDescription": {"text": r[1]}, "fullDescription": {"text": r[1]}, "defaultConfiguration": {"level": "warning"}} for r in RULES]
    results = [{"ruleId": rid, "level": "warning", "message": {"text": msg}, "locations": [{"physicalLocation": {"artifactLocation": {"uri": f}, "region": {"startLine": ln}}}]} for rid, name, f, ln, msg in findings]
    out = {"version": "2.1.0", "$schema": "https://json.schemastore.org/sarif-2.1.0.json", "runs": [{"tool": {"driver": {"name": "h0land", "version": "3.0.0", "informationUri": "https://github.com/Colegio-San-Caio/h0land", "rules": rules}}, "results": results}]}
    with open(sarif, "w") as o: json.dump(out, o, indent=2)
    print(f"SARIF written: {sarif}")

if __name__ == "__main__":
    # python h0land.py scan . --sarif h0land.sarif
    target = sys.argv[2] if len(sys.argv) > 2 else "."
    sarif = "h0land.sarif"
    if "--sarif" in sys.argv:
        sarif = sys.argv[sys.argv.index("--sarif")+1]
    do_scan(target, sarif)
