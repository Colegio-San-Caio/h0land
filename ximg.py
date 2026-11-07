import sys,struct,zlib
from PIL import Image
M=b'XIMG'
def enc(src,dst):
    im=Image.open(src).convert('RGBA'); w,h=im.size
    open(dst,'wb').write(M+struct.pack('<BBII',1,1,w,h)+zlib.compress(im.tobytes(),9))
def dec(src,dst):
    d=open(src,'rb').read()
    assert d[:4]==M
    v,f,w,h=struct.unpack('<BBII',d[4:14])
    raw=zlib.decompress(d[14:]) if f&1 else d[14:]
    Image.frombytes('RGBA',(w,h),raw).save(dst)
a=sys.argv
(enc if a[1]=='enc' else dec)(a[2],a[3])
