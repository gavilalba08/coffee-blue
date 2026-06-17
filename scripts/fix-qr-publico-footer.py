from pathlib import Path
import re
import sys
import subprocess

ROOT = Path(".")
QR_DIR = ROOT / "public/assets/qr"
QR_DIR.mkdir(parents=True, exist_ok=True)

PUBLIC_URL = "https://coffeeblue.com.br/cardapiodigital"
NEW_QR = QR_DIR / "qr-cardapio-digital-coffeeblue-publico-v2.png"

print("=== GERANDO QR CODE PUBLICO ===")

try:
    import qrcode
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "qrcode[pil]"])
    import qrcode

qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=14,
    border=3,
)

qr.add_data(PUBLIC_URL)
qr.make(fit=True)

img = qr.make_image(fill_color="#02142C", back_color="#FFFFFF").convert("RGB")
img.save(NEW_QR)

print(f"OK: {NEW_QR}")
print(f"URL: {PUBLIC_URL}")

print("")
print("=== TROCAR TODAS AS REFERENCIAS DE QR NO CODIGO ===")

qr_patterns = [
    "assets/qr/qr-cardapio-digital.png",
    "assets/qr/qr-cardapio-digital-publico.png",
    "assets/qr/qr-cardapio-digital-coffeeblue-publico.png",
    "assets/qr/qr-cardapio-digital-coffeeblue-publico-v2.png",
]

new_ref = "assets/qr/qr-cardapio-digital-coffeeblue-publico-v2.png"

for path in list((ROOT / "src").rglob("*.*")):
    if path.suffix.lower() not in [".html", ".ts", ".scss", ".css"]:
        continue

    text = path.read_text(encoding="utf-8")
    old_text = text

    for p in qr_patterns:
        text = text.replace(p, new_ref)

    # Se tiver algum localhost hardcoded no QR/link do cardápio, troca também.
    text = text.replace("http://localhost:4200/cardapiodigital", PUBLIC_URL)
    text = text.replace("https://localhost:4200/cardapiodigital", PUBLIC_URL)
    text = text.replace("localhost:4200/cardapiodigital", PUBLIC_URL)

    if text != old_text:
        path.write_text(text, encoding="utf-8")
        print(f"Atualizado: {path}")

print("")
print("=== CORRIGIR LOGO DO FOOTER ===")

home = ROOT / "src/app/home/home.html"
html = home.read_text(encoding="utf-8")

# Usa uma logo existente da pasta designs para não quebrar no deploy.
# Se o footer tinha src quebrado de brand, substitui por designs.
footer_logo_ref = "assets/designs/coffee-blue-design-03.png"

broken_refs = [
    "assets/brand/footer-logo-white.png",
    "assets/brand/header-logo-white.png",
    "assets/brand/logo-footer-white.png",
    "assets/brand/logo-white.png",
]

for ref in broken_refs:
    html = html.replace(ref, footer_logo_ref)

# Caso exista imagem do footer sem classe clara, garante que a logo do footer use um asset existente.
html = re.sub(
    r'(<footer[\s\S]*?<img[^>]+src=")([^"]+)("[^>]*alt="Blue Coffee"[^>]*>)',
    r'\1' + footer_logo_ref + r'\3',
    html,
    count=1
)

home.write_text(html, encoding="utf-8")
print(f"OK: footer revisado em {home}")

print("")
print("=== VERIFICACAO FINAL DE LOCALHOST ===")
for base in ["src", "public"]:
    for path in (ROOT / base).rglob("*.*"):
        if path.suffix.lower() not in [".html", ".ts", ".scss", ".css", ".json", ".txt"]:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "localhost" in text or "127.0.0.1" in text:
            print(f"ATENCAO: ainda existe localhost em {path}")

print("")
print("Finalizado.")
