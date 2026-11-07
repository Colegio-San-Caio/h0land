import sys, json, pathlib, re

RULES = [
    ("H0L001", "DangerousEval", r"eval\(|innerHTML\s*="),
    ("H0L002", "TodoLeft", r"\b(TODO|FIXME)\b\s*:?"),
    ("H0L003", "HardcodedHttp", r"http://[^\s\"']+"),
]
CODE_EXTS = {".py", ".js", ".ts", ".tsx", ".jsx", ".html", ".css", ".go", ".rs", ".java", ".php"}
SKIP_DIRS = {".git", "docs", "node_modules", "precomputer", "__pycache__", ".github", "v86", "build", "dist", "generated", "e2e"}
SKIP_FILES = {"h0land.py"}
# line contains any of these -> never a finding
ALLOW_SUBSTR = ["www.w3.org", "w3.org/TR/", "example.com", "example.org", "zombo.com", "DOCTYPE", "xmlns", "localhost", "127.0.0.1"]

def do_scan(target, sarif):
    findings = []
    for p in pathlib.Path(target).rglob("*"):
        if not p.is_file(): continue
        if p.suffix not in CODE_EXTS: continue
        if p.name in SKIP_FILES: continue
        if p.name.endswith(".d.ts"): continue
        if ".test." in p.name: continue
        if p.name.startswith("made_"): continue
        if "generated" in str(p): continue
        if any(part in SKIP_DIRS for part in p.parts): continue
        try: text = p.read_text(errors="ignore")
        except: continue
        for lineno, line in enumerate(text.splitlines(), 1):
            if any(s in line for s in ALLOW_SUBSTR): continue
            for rid, name, pat in RULES:
                if re.search(pat, line):
                    findings.append((rid, name, str(p), lineno, line.strip()[:140]))
    print(f"Findings: {len(findings)}")
    for rid, name, f, ln, msg in findings:
        print(f"{rid} {f}:{ln} - {msg}")
    rules = [{"id": r[0], "name": r[1], "shortDescription": {"text": r[1]}, "fullDescription": {"text": r[1]}, "defaultConfiguration": {"level": "warning"}} for r in RULES]
    results = [{"ruleId": rid, "level": "warning", "message": {"text": msg}, "locations": [{"physicalLocation": {"artifactLocation": {"uri": f}, "region": {"startLine": ln}}}]} for rid, name, f, ln, msg in findings]
    out = {"version": "2.1.0", "$schema": "https://json.schemastore.org/sarif-2.1.0.json", "runs": [{"tool": {"driver": {"name": "h0land", "version": "3.3.0", "informationUri": "https://github.com/Colegio-San-Caio/h0land", "rules": rules}}, "results": results}]}
    with open(sarif, "w") as o: json.dump(out, o, indent=2)
    print(f"SARIF written: {sarif}")

if __name__ == "__main__":
    target = sys.argv[2] if len(sys.argv) > 2 else "."
    sarif = "h0land.sarif"
    if "--sarif" in sys.argv:
        sarif = sys.argv[sys.argv.index("--sarif")+1]
    do_scan(target, sarif)
