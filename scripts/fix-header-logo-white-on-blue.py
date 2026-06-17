from pathlib import Path
import re

html_path = Path("src/app/home/home.html")
scss_path = Path("src/app/home/home.scss")

html = html_path.read_text(encoding="utf-8")
scss = scss_path.read_text(encoding="utf-8")

# Usa os assets que já existem no projeto.
# Pelo histórico do projeto:
# header-logo-white.png = branca
# header-logo-blue.png ou coffee-blue-design-04.png = azul
white_candidates = [
    "assets/brand/header-logo-white.png",
    "assets/designs/coffee-blue-design-03.png",
]

blue_candidates = [
    "assets/brand/header-logo-blue.png",
    "assets/designs/coffee-blue-design-04.png",
]

def pick(candidates):
    for asset in candidates:
        if Path("public", asset).exists():
            return asset
    return candidates[-1]

LOGO_WHITE = pick(white_candidates)
LOGO_BLUE = pick(blue_candidates)

print("Logo branca:", LOGO_WHITE)
print("Logo azul:", LOGO_BLUE)

header_logo = f'''<a class="logo" href="#hero" (click)="goToAnchor('#hero', $event)" aria-label="Voltar ao início">
      <img
        class="logo__image logo__image--white"
        src="{LOGO_WHITE}"
        alt="Blue Coffee"
      />
      <img
        class="logo__image logo__image--blue"
        src="{LOGO_BLUE}"
        alt="Blue Coffee"
      />
    </a>'''

html = re.sub(
    r'<a class="logo[^"]*"[\s\S]*?</a>',
    header_logo,
    html,
    count=1
)

html_path.write_text(html, encoding="utf-8")

# Remove patches anteriores que possam estar escondendo a logo.
for marker in [
    "PATCH FINAL — LOGOS HEADER E FOOTER",
    "PATCH FINAL — LOGO DO HEADER COM MESMO TAMANHO NO HERO E NO SCROLL",
    "PATCH DEFINITIVO — LOGO HEADER E FOOTER",
    "PATCH DEFINITIVO — LOGO DO HEADER SEMPRE VISÍVEL",
    "PATCH FINAL — LOGOS HEADER/FOOTER COFFEE BLUE",
    "PATCH DEFINITIVO — HEADER LOGO BRANCA NO AZUL",
]:
    scss = re.sub(
        rf"/\* {re.escape(marker)} \*/[\s\S]*?(?=/\* PATCH|$)",
        "",
        scss
    )

patch = r'''

/* PATCH DEFINITIVO — HEADER LOGO BRANCA NO AZUL */
.header .logo,
.header__inner .logo,
.header.header--scrolled .logo {
  position: relative !important;
  width: 150px !important;
  min-width: 150px !important;
  height: 78px !important;
  flex: 0 0 150px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  overflow: visible !important;
  z-index: 50 !important;
}

.header .logo__image {
  position: absolute !important;
  left: 50% !important;
  top: 50% !important;
  width: auto !important;
  height: 64px !important;
  max-height: 64px !important;
  max-width: 150px !important;
  object-fit: contain !important;
  display: block !important;
  transform: translate(-50%, -50%) !important;
  transition: opacity 160ms ease, visibility 160ms ease !important;
}

/* Página no topo / Hero / header azul: mostra a logo branca */
.header:not(.header--scrolled) .logo__image--white {
  opacity: 1 !important;
  visibility: visible !important;
  z-index: 2 !important;
}

.header:not(.header--scrolled) .logo__image--blue {
  opacity: 0 !important;
  visibility: hidden !important;
  z-index: 1 !important;
}

/* Depois do scroll / header branco: mostra a logo azul */
.header.header--scrolled .logo__image--blue {
  opacity: 1 !important;
  visibility: visible !important;
  z-index: 2 !important;
}

.header.header--scrolled .logo__image--white {
  opacity: 0 !important;
  visibility: hidden !important;
  z-index: 1 !important;
}

@media (max-width: 760px) {
  .header .logo,
  .header__inner .logo,
  .header.header--scrolled .logo {
    width: 120px !important;
    min-width: 120px !important;
    height: 68px !important;
    flex-basis: 120px !important;
  }

  .header .logo__image {
    height: 52px !important;
    max-height: 52px !important;
    max-width: 120px !important;
  }
}
'''

scss = scss.rstrip() + "\n" + patch + "\n"
scss_path.write_text(scss, encoding="utf-8")

print("OK: header corrigido para usar logo branca no fundo azul e azul no fundo branco.")
