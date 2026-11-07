import json
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
            rules.append([k.strip().lower(), v])
load("main.BLY")
T = """<!doctype html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>BLUH :: BLY</title>
<style>
body{background:#000;margin:16px}
.box{border:1px solid #1c2430;border-radius:10px;overflow:hidden;background:linear-gradient(145deg,#050607,#0d1014 55%,#030304);color:#3dff9a;font:13px monospace}
.bar{padding:6px 10px;letter-spacing:2px;background:#10151b;border-bottom:1px solid #1c2430}
pre{margin:0;padding:10px;height:220px;overflow:auto;white-space:pre-wrap}
.in{display:flex;border-top:1px solid #1c2430}
input{flex:1;min-width:0;background:transparent;border:0;outline:0;color:#3dff9a;font:13px monospace;padding:8px}
</style></head><body>
<div class="box"><div class="bar">__BANNER__</div>
<pre id="o"></pre>
<div class="in"><span style="padding:8px 0 8px 10px">&gt;</span><input id="i" autocomplete="off"></div></div>
<script>
var R=__RULES__,M="__MODE__",o=document.getElementById("o"),i=document.getElementById("i");
function p(t){o.textContent+=t+"\\n";o.scrollTop=o.scrollHeight;}
p("GRID __GRID__ BLOCK __BLOCK__");
i.addEventListener("keydown",function(e){
 if(e.key!=="Enter")return;
 var q=i.value.trim();i.value="";if(!q)return;p("> "+q);
 var a="NO MATCH. TYPE help";
 for(var n=0;n<R.length;n++){if(q.toLowerCase().indexOf(R[n][0])>=0){a=R[n][1];break;}}
 p("["+M+"] "+a);
});
</script></body></html>
"""
out = (T.replace("__RULES__", json.dumps(rules))
        .replace("__BANNER__", cfg.get("BANNER", "BLUH"))
        .replace("__MODE__", cfg.get("MODE", "STUB"))
        .replace("__GRID__", cfg.get("GRID", ""))
        .replace("__BLOCK__", cfg.get("BLOCK", "")))
open("bluh.HTML", "w", encoding="utf-8").write(out)
print("wrote bluh.HTML", len(out), "bytes")
