from pathlib import Path
import re

html_path = Path("src/app/home/home.html")
scss_path = Path("src/app/home/home.scss")

html = html_path.read_text(encoding="utf-8")
scss = scss_path.read_text(encoding="utf-8")

# Logo branca para fundo azul escuro
LOGO_WHITE = "assets/designs/coffee-blue-design-03.png"

# Logo azul para fundo branco
LOGO_BLUE = "assets/designs/coffee-blue-design-04.png"

# HEADER: duas versões, uma branca e uma azul.
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

# FOOTER: usa logo branca, pois o fundo do footer é azul escuro.
footer_match = re.search(r"<footer[\s\S]*?</footer>", html)

if footer_match:
    footer = footer_match.group(0)

    if re.search(r'<img[^>]*alt="Blue Coffee"[^>]*>', footer):
        footer = re.sub(
            r'<img[^>]*alt="Blue Coffee"[^>]*>',
            f'<img class="footer__logo-img" src="{LOGO_WHITE}" alt="Blue Coffee" loading="lazy" />',
            footer,
            count=1
        )
    else:
        footer = footer.replace(
            "<footer",
            f'<footer',
            1
        )
        footer = footer.replace(
            ">",
            f'>\n  <img class="footer__logo-img" src="{LOGO_WHITE}" alt="Blue Coffee" loading="lazy" />',
            1
        )

    html = html[:footer_match.start()] + footer + html[footer_match.end():]

html_path.write_text(html, encoding="utf-8")

# Remove patches antigos/conflitantes de logo.
patterns = [
    r"/\* PATCH FINAL — LOGOS HEADER E FOOTER \*/[\s\S]*?(?=/\* PATCH|$)",
    r"/\* PATCH FINAL — LOGO DO HEADER COM MESMO TAMANHO NO HERO E NO SCROLL \*/[\s\S]*?(?=/\* PATCH|$)",
    r"/\* PATCH DEFINITIVO — LOGO HEADER E FOOTER \*/[\s\S]*?(?=/\* PATCH|$)",
    r"/\* PATCH DEFINITIVO — LOGO DO HEADER SEMPRE VISÍVEL \*/[\s\S]*?(?=/\* PATCH|$)",
]

for pattern in patterns:
    scss = re.sub(pattern, "", scss)

patch = r'''

/* PATCH FINAL — LOGOS HEADER/FOOTER COFFEE BLUE */
.header .logo,
.header.header--scrolled .logo,
.header__inner .logo {
  position: relative !important;
  width: 150px !important;
  min-width: 150px !important;
  height: 78px !important;
  flex: 0 0 150px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  overflow: visible !important;
  opacity: 1 !important;
  visibility: visible !important;
  z-index: 30 !important;
}

.header .logo__image,
.header.header--scrolled .logo__image,
.header__inner .logo__image {
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
  transition: opacity 180ms ease, visibility 180ms ease !important;
}

/* Fundo azul escuro / início / hero: logo branca */
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

/* Fundo branco / scroll: logo azul */
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

/* Footer: mesmo tamanho visual do header, mas sem gigantismo */
.footer__logo-img,
.footer img[alt="Blue Coffee"] {
  width: auto !important;
  height: 64px !important;
  max-height: 64px !important;
  max-width: 150px !important;
  object-fit: contain !important;
  display: block !important;
  margin: 0 auto 1rem !important;
  opacity: 1 !important;
  visibility: visible !important;
}

@media (max-width: 760px) {
  .header .logo,
  .header.header--scrolled .logo,
  .header__inner .logo {
    width: 120px !important;
    min-width: 120px !important;
    height: 68px !important;
    flex-basis: 120px !important;
  }

  .header .logo__image,
  .header.header--scrolled .logo__image,
  .header__inner .logo__image {
    height: 52px !important;
    max-height: 52px !important;
    max-width: 120px !important;
  }

  .footer__logo-img,
  .footer img[alt="Blue Coffee"] {
    height: 52px !important;
    max-height: 52px !important;
    max-width: 120px !important;
  }
}
'''

scss = scss.rstrip() + "\n" + patch + "\n"
scss_path.write_text(scss, encoding="utf-8")

print("OK: header com logo branca no fundo azul, azul no fundo branco, e footer ajustado.")
