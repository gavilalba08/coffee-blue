from pathlib import Path
from PIL import Image, ImageChops

files = [
    "public/assets/brand-new/wordmark-blue-coffee-azul.png",
    "public/assets/brand-new/wordmark-blue-coffee-branca.png",
    "public/assets/brand-new/logo-blue-coffee-com-mascote-azul.png",
    "public/assets/brand-new/logo-blue-coffee-com-mascote-branca.png",
]

for file in files:
    path = Path(file)
    if not path.exists():
        print("IGNORADO:", path)
        continue

    img = Image.open(path).convert("RGBA")
    alpha = img.getchannel("A")
    bbox = alpha.getbbox()

    if not bbox:
        print("SEM ALPHA:", path)
        continue

    cropped = img.crop(bbox)

    # pequena margem segura
    pad = 8
    canvas = Image.new("RGBA", (cropped.width + pad * 2, cropped.height + pad * 2), (0, 0, 0, 0))
    canvas.alpha_composite(cropped, (pad, pad))

    out = path.with_name(path.stem + "-cropped.png")
    canvas.save(out)
    print("OK:", out)
