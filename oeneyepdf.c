#!/usr/bin/env python3
import os
NAME = os.environ.get('FAX_NAME', 'oeneye')
FAX = f"FAX by {NAME} - set by oeneye"
PDF = os.environ.get('PDF', './MOSFETQexchange/output/jc_sigma.pdf')
def esc(s):
    return s.replace(chr(92), chr(92)+chr(92)).replace("(", "\\(").replace(")", "\\)")
stream = f"BT /F1 12 Tf 50 750 Td ({esc(FAX)}) Tj ET\nBT /F1 10 Tf 50 730 Td (MOSFETQ Gesamtwerk V2.2 - 2026-0812-CNNN3-BK01) Tj ET".encode()
o = [b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n",
     b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n",
     b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> >> >> /Contents 4 0 R >> endobj\n",
     f"4 0 obj << /Length {len(stream)} >> stream\n".encode() + stream + b"\nendstream endobj\n"]
pdf = b"%PDF-1.4\n"
off = []
for x in o:
    off.append(len(pdf))
    pdf += x
xref = len(pdf)
pdf += f"xref\n0 {len(o)+1}\n0000000000 65535 f \n".encode()
for of in off:
    pdf += f"{of:010d} 00000 n \n".encode()
pdf += f"trailer << /Size {len(o)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF".encode()
os.makedirs(os.path.dirname(PDF), exist_ok=True)
open(PDF, 'wb').write(pdf)
print(f"[oeneye] wrote {PDF}")
