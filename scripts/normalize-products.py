from pathlib import Path
from PIL import Image

SRC = Path("public/assets/products")
DST = Path("public/assets/products-packshots")
DST.mkdir(parents=True, exist_ok=True)

def avg_corner_bg(img):
    w, h = img.size
    pts = [
        img.getpixel((0, 0)),
        img.getpixel((w - 1, 0)),
        img.getpixel((0, h - 1)),
        img.getpixel((w - 1, h - 1)),
    ]
    return tuple(sum(p[i] for p in pts) // 4 for i in range(4))

def color_diff(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]-b[2])

def trim_background(img, tolerance=55):
    img = img.convert("RGBA")
    bg = avg_corner_bg(img)
    w, h = img.size

    mask = Image.new("L", (w, h), 0)
    src = img.load()
    dst = mask.load()

    for y in range(h):
        for x in range(w):
            px = src[x, y]
            if px[3] > 0 and color_diff(px, bg) > tolerance:
                dst[x, y] = 255

    bbox = mask.getbbox()
    if not bbox:
        return img

    left, top, right, bottom = bbox
    pad_x = max(8, int((right - left) * 0.08))
    pad_y = max(8, int((bottom - top) * 0.08))

    left = max(0, left - pad_x)
    top = max(0, top - pad_y)
    right = min(w, right + pad_x)
    bottom = min(h, bottom + pad_y)

    cropped = img.crop((left, top, right, bottom))

    # tenta deixar o fundo transparente
    cropped = cropped.convert("RGBA")
    px = cropped.load()
    cw, ch = cropped.size
    for y in range(ch):
        for x in range(cw):
            p = px[x, y]
            if color_diff(p, bg) <= tolerance:
                px[x, y] = (0, 0, 0, 0)

    return cropped

def place_on_canvas(img, canvas_size=(1200, 1400), margin=90):
    canvas_w, canvas_h = canvas_size
    canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))

    max_w = canvas_w - margin * 2
    max_h = canvas_h - margin * 2

    w, h = img.size
    scale = min(max_w / w, max_h / h)
    new_size = (max(1, int(w * scale)), max(1, int(h * scale)))
    img = img.resize(new_size, Image.LANCZOS)

    x = (canvas_w - img.width) // 2
    y = canvas_h - img.height - margin
    canvas.alpha_composite(img, (x, y))
    return canvas

for src in SRC.rglob("*.png"):
    rel = src.relative_to(SRC)
    out = DST / rel
    out.parent.mkdir(parents=True, exist_ok=True)

    img = Image.open(src).convert("RGBA")
    trimmed = trim_background(img, tolerance=55)
    normalized = place_on_canvas(trimmed, canvas_size=(1200, 1400), margin=90)
    normalized.save(out)

    print("OK ->", out)

print("\nPackshots gerados em:", DST)
