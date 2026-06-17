from pathlib import Path
import re

home_html = Path("src/app/home/home.html")
home_scss = Path("src/app/home/home.scss")
cardapio_html = Path("src/app/cardapio/cardapio.html")
cardapio_scss = Path("src/app/cardapio/cardapio.scss")

# Logo azul para fundo claro / footer
LOGO_DARK = "assets/designs/coffee-blue-design-04.png"

# Logo branca para fundo escuro, caso exista no header/cardápio
LOGO_LIGHT = "assets/designs/coffee-blue-design-03.png"

html = home_html.read_text(encoding="utf-8")

# 1) Corrige qualquer logo quebrada no footer.
footer_match = re.search(r"<footer[\s\S]*?</footer>", html)

if footer_match:
    footer = footer_match.group(0)

    # Troca qualquer <img> dentro do footer para a logo existente.
    footer_fixed = re.sub(
        r'<img[^>]*alt="Blue Coffee"[^>]*>',
        f'<img class="footer__logo-img" src="{LOGO_DARK}" alt="Blue Coffee" loading="lazy" />',
        footer,
        count=1,
    )

    # Se não encontrou img com alt Blue Coffee, tenta trocar a primeira imagem do footer.
    if footer_fixed == footer:
        footer_fixed = re.sub(
            r'<img[^>]*>',
            f'<img class="footer__logo-img" src="{LOGO_DARK}" alt="Blue Coffee" loading="lazy" />',
            footer,
            count=1,
        )

    html = html[:footer_match.start()] + footer_fixed + html[footer_match.end():]

home_html.write_text(html, encoding="utf-8")

# 2) CSS definitivo para logo do header e footer.
scss = home_scss.read_text(encoding="utf-8")

patch = r'''

/* PATCH FINAL — LOGOS HEADER E FOOTER */
.header .logo,
.header__inner .logo {
  width: auto !important;
  min-width: 118px !important;
  height: 74px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  flex-shrink: 0 !important;
}

.header .logo__image,
.header__inner .logo__image,
.logo__image {
  width: auto !important;
  height: 58px !important;
  max-height: 58px !important;
  max-width: 132px !important;
  object-fit: contain !important;
  display: block !important;
  transform: none !important;
  opacity: 1 !important;
}

.header.header--scrolled .logo,
.header--scrolled .logo {
  height: 74px !important;
}

.header.header--scrolled .logo__image,
.header--scrolled .logo__image {
  height: 58px !important;
  max-height: 58px !important;
  transform: none !important;
}

.footer__logo-img,
.footer img[alt="Blue Coffee"] {
  width: auto !important;
  height: 46px !important;
  max-height: 46px !important;
  max-width: 140px !important;
  object-fit: contain !important;
  display: block !important;
  margin: 0 auto 1rem !important;
}

@media (max-width: 760px) {
  .header .logo,
  .header__inner .logo {
    min-width: 96px !important;
    height: 64px !important;
  }

  .header .logo__image,
  .header__inner .logo__image,
  .logo__image {
    height: 48px !important;
    max-height: 48px !important;
    max-width: 110px !important;
  }

  .footer__logo-img,
  .footer img[alt="Blue Coffee"] {
    height: 40px !important;
    max-height: 40px !important;
  }
}
'''

if "PATCH FINAL — LOGOS HEADER E FOOTER" not in scss:
    scss += patch

home_scss.write_text(scss, encoding="utf-8")

# 3) Cardápio digital: logo maior também, sem mexer no layout.
if cardapio_scss.exists():
    cs = cardapio_scss.read_text(encoding="utf-8")

    card_patch = r'''

/* PATCH FINAL — LOGO HEADER CARDÁPIO */
.cp-header .logo,
.cardapio-header .logo,
.menu-header .logo,
.header .logo {
  min-width: 118px !important;
  height: 74px !important;
  display: inline-flex !important;
  align-items: center !important;
}

.cp-header .logo img,
.cardapio-header .logo img,
.menu-header .logo img,
.header .logo img,
.logo__image {
  height: 58px !important;
  max-height: 58px !important;
  width: auto !important;
  max-width: 132px !important;
  object-fit: contain !important;
}
'''

    if "PATCH FINAL — LOGO HEADER CARDÁPIO" not in cs:
        cs += card_patch

    cardapio_scss.write_text(cs, encoding="utf-8")

print("OK: logos do header e footer corrigidas.")
