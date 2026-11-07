#!/usr/bin/env python3
import os
CODE="2026-0812-CNNN3-BK01"
PDF=os.environ.get('PDF','./MOSFETQ-Gesamt-2026-0812-CNNN3-BK01.pdf')
known=["Single-Loop","Nested-Loops","Triangular","Multiply","Divide","Half-Loop","Sequential","While-Halving","Recursion-n","Recursion-nlogn","Fibonacci","Ada","Assembly","AWK","Bash","C","CPP","CSharp","Clojure","COBOL","Crystal","D","Dart","Elixir","Erlang","FSharp","Fortran","Go","Groovy","Haskell","HTML","Java","JavaScript","Julia","Kotlin","Lisp","Lua","MATLAB","Nim","OCaml","Pascal","Perl","PHP","PowerShell","Python","R","Ruby","Rust","Scala","Shell","SQL","Swift","TypeScript","VBA","VisualBasic","Zig","CSS","Solidity","Racket","Prolog"]
hubs=["main.html","QxD.html","QxD-Languages.html","mosfetq-patterns.html","languages.html","bluh.html"]
titles=["Deckblatt"]+[f"HUB - {h}" for h in hubs]+[f"{u}.html" for u in known]+[f"QxD-{u}.html" for u in known]
def esc(s): return s.replace(chr(92),chr(92)*2).replace('(','\\(').replace(')','\\)')
def page_stream(i,t):
    L=[]
    L.append(f"BT /F1 6 Tf 71 822 Td (KAI OLAF KETELHUT - BUILT IN BERLIN - MOSFETQ - ISBN 978-3-00-068463-0) Tj ET")
    L.append(f"BT /F1 11 Tf 71 760 Td (MOSFETQ GmbH - Kai Olaf Ketelhut) Tj ET")
    L.append(f"BT /F1 11 Tf 71 746 Td (Berlin, Deutschland) Tj ET")
    L.append(f"BT /F1 11 Tf 71 732 Td (An: Alle, die {esc(t)} suchen) Tj ET")
    L.append(f"BT /F1 11 Tf 400 700 Td (Berlin, 06. November 2026) Tj ET")
    L.append(f"BT /F1 9 Tf 71 670 Td (Betreff: {esc(t)} - Seite {i} / {len(titles)} - DIN 5008 - {CODE}) Tj ET")
    L.append(f"BT /F1 11 Tf 71 640 Td (Sehr geehrte Damen und Herren,) Tj ET")
    L.append(f"BT /F1 11 Tf 71 610 Td (hiermit uebersenden wir Ihnen die Datei {esc(t)} gemaess DIN 5008.) Tj ET")
    L.append(f"BT /F1 11 Tf 71 590 Td (Original: https://kaiolafketelhut.github.io/{esc(t)}) Tj ET")
    L.append(f"BT /F1 16 Tf 71 500 Td (Kai Olaf Ketelhut) Tj ET")
    L.append(f"BT /F1B 11 Tf 71 480 Td (KAI OLAF KETELHUT) Tj ET")
    L.append(f"BT /F1 11 Tf 71 460 Td (MOSFETQ - BUILT IN BERLIN - {CODE}) Tj ET")
    L.append(f"BT /F1 6 Tf 71 30 Td (Seite {i} / {len(titles)} - Aktenzeichen: {CODE}) Tj ET")
    return "\n".join(L).encode()
objs=[]; N=len(titles)
# 1=Catalog, 2=Pages, then per page: page obj + content obj
kids=[]
for i in range(N):
    page_id=3+i*2; cont_id=4+i*2
    kids.append(f"{page_id} 0 R")
    objs.append((page_id,f"{page_id} 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> /F1B << /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >> >> >> /Contents {cont_id} 0 R >> endobj\n".encode()))
    s=page_stream(i+1,titles[i])
    objs.append((cont_id,f"{cont_id} 0 obj << /Length {len(s)} >> stream\n".encode()+s+b"\nendstream\nendobj\n"))
objs.sort()
out=b"%PDF-1.4\n"
out+=b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n"
out+=f"2 0 obj << /Type /Pages /Kids [{' '.join(kids)}] /Count {N} >> endobj\n".encode()
offs={1:len(b"%PDF-1.4\n"),2:0}
# need correct offsets - rebuild properly
pdf=b"%PDF-1.4\n"; off={}
off[1]=len(pdf); pdf+=b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n"
off[2]=len(pdf); pdf+=f"2 0 obj << /Type /Pages /Kids [{' '.join(kids)}] /Count {N} >> endobj\n".encode()
for oid,data in objs:
    off[oid]=len(pdf); pdf+=data
xref=len(pdf); total=2+len(objs)
pdf+=f"xref\n0 {total+1}\n0000000000 65535 f \n".encode()
for oid in range(1,total+1): pdf+=f"{off[oid]:010d} 00000 n \n".encode()
pdf+=f"trailer << /Size {total+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF".encode()
open(PDF,'wb').write(pdf)
print(f"OK -> {PDF} Seiten={N}")
