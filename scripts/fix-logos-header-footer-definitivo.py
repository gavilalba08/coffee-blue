from pathlib import Path
import re

html_path = Path("src/app/home/home.html")
scss_path = Path("src/app/home/home.scss")

html = html_path.read_text(encoding="utf-8")
scss = scss_path.read_text(encoding="utf-8")

# Arquivos conforme padrão já usado no projeto:
# design-03 = logo clara/branca
# design-04 = logo azul/escura
LOGO_LIGHT = "assets/designs/coffee-blue-design-03.png"
LOGO_DARK = "assets/designs/coffee-blue-design-04.png"

# 1) Normaliza a logo do HEADER para ter as duas versões, sem depender de HTML quebrado antigo.
header_logo = f'''<a class="logo" href="#hero" (click)="goToAnchor('#hero', $event)">
      <img
        class="logo__image logo__image--light"
        src="{LOGO_LIGHT}"
        alt="Blue Coffee"
      />
      <img
        class="logo__image logo__image--dark"
        src="{LOGO_DARK}"
        alt="Blue Coffee"
      />
    </a>'''

html = re.sub(
    r'<a class="logo"[\s\S]*?</a>',
    header_logo,
    html,
    count=1
)

# 2) Corrige a logo do FOOTER para usar a logo clara/branca e ficar visível no fundo azul.
footer_match = re.search(r"<footer[\s\S]*?</footer>", html)

if footer_match:
    footer = footer_match.group(0)

    if re.search(r'<img[^>]*alt="Blue Coffee"[^>]*>', footer):
        footer = re.sub(
            r'<img[^>]*alt="Blue Coffee"[^>]*>',
            f'<img class="footer__logo-img" src="{LOGO_LIGHT}" alt="Blue Coffee" loading="lazy" />',
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
            f'>\n  <img class="footer__logo-img" src="{LOGO_LIGHT}" alt="Blue Coffee" loading="lazy" />',
            1
        )

    html = html[:footer_match.start()] + footer + html[footer_match.end():]

html_path.write_text(html, encoding="utf-8")

# 3) Remove patches conflitantes anteriores de logo.
patterns = [
    r"/\* PATCH FINAL — LOGOS HEADER E FOOTER \*/[\s\S]*?(?=/\* PATCH|$)",
    r"/\* PATCH FINAL — LOGO DO HEADER COM MESMO TAMANHO NO HERO E NO SCROLL \*/[\s\S]*?(?=/\* PATCH|$)",
]

for pattern in patterns:
    scss = re.sub(pattern, "", scss)

# 4) CSS definitivo, no fim do arquivo, com prioridade máxima.
patch = r'''

/* PATCH DEFINITIVO — LOGO HEADER E FOOTER */
.header .logo,
.header.header--scrolled .logo,
.header__inner .logo {
  position: relative !important;
  width: 148px !important;
  min-width: 148px !important;
  height: 78px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  flex: 0 0 148px !important;
  overflow: visible !important;
}

.header .logo__image,
.header.header--scrolled .logo__image,
.header__inner .logo__image {
  position: absolute !important;
  left: 50% !important;
  top: 50% !important;
  width: auto !important;
  height: 66px !important;
  max-height: 66px !important;
  max-width: 148px !important;
  object-fit: contain !important;
  display: block !important;
  transform: translate(-50%, -50%) !important;
  transition: opacity 180ms ease, visibility 180ms ease !important;
}

/* Estado inicial/Hero: fundo escuro, usa logo branca */
.header:not(.header--scrolled) .logo__image--light {
  opacity: 1 !important;
  visibility: visible !important;
  z-index: 2 !important;
}

.header:not(.header--scrolled) .logo__image--dark {
  opacity: 0 !important;
  visibility: hidden !important;
  z-index: 1 !important;
}

/* Estado com scroll: fundo branco, usa logo azul */
.header.header--scrolled .logo__image--dark {
  opacity: 1 !important;
  visibility: visible !important;
  z-index: 2 !important;
}

.header.header--scrolled .logo__image--light {
  opacity: 0 !important;
  visibility: hidden !important;
  z-index: 1 !important;
}

/* Footer: logo maior e visível */
.footer__logo-img,
.footer img[alt="Blue Coffee"] {
  width: auto !important;
  height: 72px !important;
  max-height: 72px !important;
  max-width: 180px !important;
  object-fit: contain !important;
  display: block !important;
  margin: 0 auto 1.25rem !important;
}

@media (max-width: 760px) {
  .header .logo,
  .header.header--scrolled .logo,
  .header__inner .logo {
    width: 118px !important;
    min-width: 118px !important;
    height: 68px !important;
    flex-basis: 118px !important;
  }

  .header .logo__image,
  .header.header--scrolled .logo__image,
  .header__inner .logo__image {
    height: 54px !important;
    max-height: 54px !important;
    max-width: 118px !important;
  }

  .footer__logo-img,
  .footer img[alt="Blue Coffee"] {
    height: 58px !important;
    max-height: 58px !important;
    max-width: 150px !important;
  }
}
'''

scss = scss.rstrip() + "\n" + patch + "\n"
scss_path.write_text(scss, encoding="utf-8")

print("OK: logos corrigidas definitivamente.")
