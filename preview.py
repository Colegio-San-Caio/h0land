from PIL import Image, ImageDraw
import pathlib
ROOT = pathlib.Path(".")

def make_light():
    img = Image.new("RGB", (1200, 1600), "#f5f3ef")
    d = ImageDraw.Draw(img)
    # infinity eye - gold lines
    # center eye
    d.ellipse([450, 600, 750, 800], outline="#b89b5a", width=3)
    d.ellipse([560, 670, 640, 730], fill="#b89b5a")
    # infinity loops
    d.arc([200, 600, 600, 800], 0, 360, fill="#b89b5a", width=2)
    d.arc([600, 600, 1000, 800], 0, 360, fill="#b89b5a", width=2)
    d.text((560, 1400), "OMQ", fill="#b89b5a")
    img.save(ROOT/"og-cover.png")

def make_dark():
    img = Image.new("RGB", (1200, 1600), "#0a0a0a")
    d = ImageDraw.Draw(img)
    d.ellipse([450, 600, 750, 800], outline="#e5d5a0", width=3)
    d.ellipse([560, 670, 640, 730], fill="#e5d5a0")
    d.arc([200, 600, 600, 800], 0, 360, fill="#e5d5a0", width=2)
    d.arc([600, 600, 1000, 800], 0, 360, fill="#e5d5a0", width=2)
    d.text((560, 1400), "OMQ", fill="#e5d5a0")
    img.save(ROOT/"OMQpreview.png")
    img.save(ROOT/"OMQpreview.jpg", quality=92)

make_light()
make_dark()
print("generated og-cover.png + OMQpreview.png - visible eye, no QR")
