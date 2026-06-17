from pathlib import Path
from PIL import Image, ImageChops
import re

ROOT = Path(".")
BRAND = ROOT / "public/assets/brand"
BRAND.mkdir(parents=True, exist_ok=True)

def trim_transparent(src: Path, dst: Path, padding: int = 8):
    img = Image.open(src).convert("RGBA")

    alpha = img.getchannel("A")
    bbox = alpha.getbbox()

    if not bbox:
        img.save(dst)
        return

    left, top, right, bottom = bbox
    left = max(0, left - padding)
    top = max(0, top - padding)
    right = min(img.width, right + padding)
    bottom = min(img.height, bottom + padding)

    cropped = img.crop((left, top, right, bottom))
    cropped.save(dst)

# Arquivos da pasta designs:
# 03 = wordmark azul
# 04 = wordmark branca
trim_transparent(
    ROOT / "public/assets/designs/coffee-blue-design-03.png",
    BRAND / "header-logo-blue.png",
    padding=10
)

trim_transparent(
    ROOT / "public/assets/designs/coffee-blue-design-04.png",
    BRAND / "header-logo-white.png",
    padding=10
)

# Atualiza header da landing para usar logos recortadas
home = Path("src/app/home/home.html")
html = home.read_text(encoding="utf-8")

html = html.replace(
    'src="assets/designs/coffee-blue-design-04.png"',
    'src="assets/brand/header-logo-white.png"',
    1
)

html = html.replace(
    'src="assets/designs/coffee-blue-design-03.png"',
    'src="assets/brand/header-logo-blue.png"',
    1
)

home.write_text(html, encoding="utf-8")

# Atualiza header do cardápio digital, se existir referência à wordmark branca
cardapio = Path("src/app/cardapio/cardapio.html")
if cardapio.exists():
    card = cardapio.read_text(encoding="utf-8")
    card = card.replace(
        'ngSrc="assets/designs/coffee-blue-design-04.png"',
        'ngSrc="assets/brand/header-logo-white.png"'
    )
    card = card.replace(
        'src="assets/designs/coffee-blue-design-04.png"',
        'src="assets/brand/header-logo-white.png"'
    )
    cardapio.write_text(card, encoding="utf-8")

print("OK: logos recortadas criadas e referências do header atualizadas.")
