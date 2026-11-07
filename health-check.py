import urllib.request, json, sys
BASE="https://kaiolafketelhut.github.io/"
PAGES=["index.html","isms.html","links.html","flyers.html","flyer.html","flyer-de.html","flyer-github.html","CERTIFICATE.html","sitemap.xml","robots.txt","og-image.png","README.md","MOSFETQ-PROOF-PACK-v41.zip"]
print("MOSFETQismsOENEYE.exe — HEALTH CHECK v48")
print("="*50)
ok=0; fail=0
for p in PAGES:
    url=BASE+p
    try:
        req=urllib.request.Request(url, headers={"User-Agent":"MOSFETQ-HealthCheck-v48"})
        with urllib.request.urlopen(req, timeout=10) as r:
            body=r.read()
            status=r.status
            checks=[]
            if p.endswith(".html"):
                if b"application/ld+json" in body: checks.append("JSON-LD ✔")
                if b"KAI OLAF KETELHUT" in body: checks.append("Author ✔")
                if b"ISMS" in body: checks.append("ISMS ✔")
            if status==200:
                print(f"✔ {p:35} {status} {len(body)} bytes {' | '.join(checks)}")
                ok+=1
            else:
                print(f"✘ {p:35} {status}")
                fail+=1
    except Exception as e:
        print(f"✘ {p:35} FAIL {e}")
        fail+=1
print("="*50)
print(f"RESULT: {ok}/{len(PAGES)} PASS • {fail} FAIL")
if fail==0:
    print("🏆 ALL GREEN — CERTIFIED PASS v48 • READY TO SHARE")
    print("Share this: https://kaiolafketelhut.github.io/links.html")
else:
    print("⚠️ Fix failed pages, then re-run: python3 health-check.py")
