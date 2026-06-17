from pathlib import Path
from PIL import Image
import json
import re

ROOT = Path(".")
DESIGNS = ROOT / "public/assets/designs"
BRAND = ROOT / "public/assets/brand"
BRAND.mkdir(parents=True, exist_ok=True)

required = [
    "coffee-blue-design-01.png",
    "coffee-blue-design-02.png",
    "coffee-blue-design-03.png",
    "coffee-blue-design-04.png",
    "coffee-blue-design-05.png",
    "coffee-blue-design-06.png",
]

missing = [name for name in required if not (DESIGNS / name).exists()]
if missing:
    raise SystemExit(f"Arquivos ausentes em public/assets/designs: {missing}")

# Mapeia tudo para a pasta Designs, que agora é a origem oficial.
mapping = {
    "assets/brand-new/logo-blue-coffee-com-mascote-azul.png": "assets/designs/coffee-blue-design-01.png",
    "assets/brand-new/logo-blue-coffee-com-mascote-branca.png": "assets/designs/coffee-blue-design-02.png",
    "assets/brand-new/wordmark-blue-coffee-azul.png": "assets/designs/coffee-blue-design-03.png",
    "assets/brand-new/wordmark-blue-coffee-branca.png": "assets/designs/coffee-blue-design-04.png",
    "assets/brand-new/mascote-coelho-azul.png": "assets/designs/coffee-blue-design-05.png",
    "assets/brand-new/mascote-coelho-branco.png": "assets/designs/coffee-blue-design-06.png",

    "assets/brand/logo-blue-coffee-com-mascote-azul.png": "assets/designs/coffee-blue-design-01.png",
    "assets/brand/logo-blue-coffee-com-mascote-branca.png": "assets/designs/coffee-blue-design-02.png",
    "assets/brand/wordmark-blue-coffee-azul.png": "assets/designs/coffee-blue-design-03.png",
    "assets/brand/wordmark-blue-coffee-branca.png": "assets/designs/coffee-blue-design-04.png",
    "assets/brand/mascote-coelho-azul.png": "assets/designs/coffee-blue-design-05.png",
    "assets/brand/mascote-coelho-branco.png": "assets/designs/coffee-blue-design-06.png",
}

for path in list(Path("src/app").rglob("*.html")) + list(Path("src/app").rglob("*.scss")) + list(Path("src/app").rglob("*.ts")):
    text = path.read_text(encoding="utf-8")
    original = text

    for old, new in mapping.items():
        text = text.replace(old, new)
        text = text.replace("/" + old, "/" + new)

    if path.name == "home.html":
        # Corrige a logo do header para usar a wordmark da pasta Designs.
        logo_markup = """
          <img
            class="logo__image logo__image--dark"
            src="assets/designs/coffee-blue-design-04.png"
            alt="Blue Coffee"
          />
          <img
            class="logo__image logo__image--light"
            src="assets/designs/coffee-blue-design-03.png"
            alt="Blue Coffee"
          />
        """.rstrip()

        text = re.sub(
            r'(<a\b(?=[^>]*class="[^"]*\blogo\b[^"]*")[^>]*>)([\s\S]*?)(</a>)',
            lambda m: m.group(1) + "\n" + logo_markup + "\n" + m.group(3),
            text,
            count=1,
        )

        # Corrige o botão de voltar ao topo para usar o mascote branco.
        text = re.sub(
            r'(<button\b(?=[^>]*class="[^"]*(?:to-top|back-to-top|scroll-top)[^"]*")[^>]*>)([\s\S]*?)(</button>)',
            lambda m: m.group(1) + '\n  <img src="assets/designs/coffee-blue-design-06.png" alt="" aria-hidden="true" />\n' + m.group(3),
            text,
            count=1,
        )

    if text != original:
        path.write_text(text, encoding="utf-8")
        print("Atualizado:", path)

# Garante método scrollToTop no Home, caso o botão use esse método.
home_ts = Path("src/app/home/home.ts")
text = home_ts.read_text(encoding="utf-8")
if "scrollToTop()" not in text:
    before, sep, after = text.rpartition("\n}")
    if sep:
        text = before + """

  scrollToTop(): void {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
""" + sep + after
        home_ts.write_text(text, encoding="utf-8")
        print("Adicionado scrollToTop em:", home_ts)

# CSS final: centralização do contato, logo maior, botão topo com mascote.
home_scss = Path("src/app/home/home.scss")
scss = home_scss.read_text(encoding="utf-8")

marker = "/* ===== AJUSTES FINAIS DESIGNS / CONTATO / TO TOP ===== */"

if marker not in scss:
    scss += """

/* ===== AJUSTES FINAIS DESIGNS / CONTATO / TO TOP ===== */

.logo {
  display: inline-flex;
  align-items: center;
  min-width: 120px;
}

.logo__image {
  display: block;
  width: clamp(96px, 8vw, 142px);
  max-height: 58px;
  object-fit: contain;
}

.header:not(.header--scrolled) .logo__image--dark {
  display: block;
}

.header:not(.header--scrolled) .logo__image--light {
  display: none;
}

.header--scrolled .logo__image--dark {
  display: none;
}

.header--scrolled .logo__image--light {
  display: block;
}

/* Centraliza corretamente Redes Sociais & Contato */
#contato .section__heading,
#contato .section__eyebrow,
#contato .section__title,
#contato .section__subtitle {
  text-align: center;
  margin-left: auto;
  margin-right: auto;
}

#contato .contact-grid,
#contato .contact__links,
#contato .contact-links,
.contact-grid,
.contact__links,
.contact-links {
  width: min(100%, 620px);
  margin-left: auto !important;
  margin-right: auto !important;
  display: grid !important;
  grid-template-columns: repeat(2, minmax(220px, 260px));
  justify-content: center !important;
  justify-items: stretch !important;
  align-items: stretch !important;
  gap: 1rem;
}

#contato .contact-card,
#contato .contact__card,
.contact-card,
.contact__card {
  width: 100%;
  min-height: 96px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Botão voltar ao topo com mascote */
.to-top,
.back-to-top,
.scroll-top {
  position: fixed;
  right: 2rem;
  bottom: 2rem;
  z-index: 80;
  width: 64px;
  height: 64px;
  border-radius: 999px;
  border: 1px solid rgba(201, 154, 75, 0.65);
  background: rgba(2, 20, 44, 0.86);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 18px 42px rgba(0, 0, 0, 0.22);
  cursor: pointer;
}

.to-top img,
.back-to-top img,
.scroll-top img {
  width: 36px;
  height: 36px;
  object-fit: contain;
  display: block;
}

.to-top:hover,
.back-to-top:hover,
.scroll-top:hover {
  transform: translateY(-3px);
  background: rgba(2, 20, 44, 0.96);
}

@media (max-width: 700px) {
  #contato .contact-grid,
  #contato .contact__links,
  #contato .contact-links,
  .contact-grid,
  .contact__links,
  .contact-links {
    grid-template-columns: minmax(220px, 280px);
  }

  .to-top,
  .back-to-top,
  .scroll-top {
    right: 1rem;
    bottom: 1rem;
    width: 56px;
    height: 56px;
  }

  .to-top img,
  .back-to-top img,
  .scroll-top img {
    width: 31px;
    height: 31px;
  }
}
"""
    home_scss.write_text(scss, encoding="utf-8")
    print("CSS final adicionado:", home_scss)

# Gera favicon pelo mascote azul.
src = DESIGNS / "coffee-blue-design-05.png"
img = Image.open(src).convert("RGBA")

bbox = img.getbbox()
if bbox:
    img = img.crop(bbox)

def make_icon(size: int) -> Image.Image:
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    margin = int(size * 0.12)
    max_size = size - margin * 2

    w, h = img.size
    scale = min(max_size / w, max_size / h)
    resized = img.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS)

    x = (size - resized.width) // 2
    y = (size - resized.height) // 2
    canvas.alpha_composite(resized, (x, y))
    return canvas

make_icon(32).save(BRAND / "favicon-32x32.png")
make_icon(192).save(BRAND / "favicon-192x192.png")
make_icon(512).save(BRAND / "favicon-512x512.png")
make_icon(180).save(BRAND / "apple-touch-icon.png")

ico_sizes = [make_icon(16), make_icon(32), make_icon(48), make_icon(64), make_icon(128), make_icon(256)]
ico_sizes[0].save(ROOT / "public/favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])

manifest = {
    "name": "Blue Coffee",
    "short_name": "Blue Coffee",
    "icons": [
        {
            "src": "/assets/brand/favicon-192x192.png",
            "sizes": "192x192",
            "type": "image/png"
        },
        {
            "src": "/assets/brand/favicon-512x512.png",
            "sizes": "512x512",
            "type": "image/png"
        }
    ],
    "theme_color": "#02142C",
    "background_color": "#02142C",
    "display": "standalone"
}
(BRAND / "site.webmanifest").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

# Atualiza index.html com favicon/manifest corretos.
index = Path("src/index.html")
html = index.read_text(encoding="utf-8")

# Remove links antigos de favicon/apple/manifest para não duplicar.
html = re.sub(r'\s*<link[^>]+rel=["\'](?:icon|apple-touch-icon|manifest)["\'][^>]*>', "", html)
html = re.sub(r'\s*<meta[^>]+name=["\']theme-color["\'][^>]*>', "", html)

insert = """
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/brand/favicon-32x32.png">
  <link rel="apple-touch-icon" href="/assets/brand/apple-touch-icon.png">
  <link rel="manifest" href="/assets/brand/site.webmanifest">
  <meta name="theme-color" content="#02142C">
"""

html = html.replace("<head>", "<head>" + insert, 1)
index.write_text(html, encoding="utf-8")

print("Favicons gerados:")
print("-", ROOT / "public/favicon.ico")
print("-", BRAND / "favicon-32x32.png")
print("-", BRAND / "favicon-192x192.png")
print("-", BRAND / "favicon-512x512.png")
print("-", BRAND / "apple-touch-icon.png")
print("-", BRAND / "site.webmanifest")
