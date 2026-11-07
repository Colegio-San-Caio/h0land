import sys
cfg, rules = {}, []
def load(path):
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("INCLUDE="):
            load(line.split("=", 1)[1].strip())
        elif "=" in line.split("|", 1)[0]:
            k, v = line.split("=", 1)
            cfg[k.strip()] = v
        elif "|" in line:
            k, v = line.split("|", 1)
            rules.append((k.strip().lower(), v))
load(sys.argv[1] if len(sys.argv) > 1 else "main.BLY")
mode = cfg.get("MODE", "STUB")
print(cfg.get("BANNER", "BLUH"))
print("GRID", cfg.get("GRID"), "BLOCK", cfg.get("BLOCK"))
while True:
    try:
        q = input(cfg.get("PROMPT", "> "))
    except EOFError:
        break
    if q.strip().lower() == cfg.get("EXIT", "quit"):
        break
    for k, v in rules:
        if k in q.lower():
            print("[" + mode + "]", v)
            break
    else:
        print("[" + mode + "] NO MATCH. TYPE help")
