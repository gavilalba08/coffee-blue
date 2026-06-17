from pathlib import Path
import re

home_ts = Path("src/app/home/home.ts")
home_html = Path("src/app/home/home.html")
home_scss = Path("src/app/home/home.scss")
cardapio_scss = Path("src/app/cardapio/cardapio.scss")
cardapio_html = Path("src/app/cardapio/cardapio.html")

# =========================================================
# 1. MENU CEOs FUNCIONANDO
# =========================================================
text = home_ts.read_text()

# Garante item CEOs apontando para #ceos
text = re.sub(
    r"\{\s*label:\s*'CEOs'[^}]*\}",
    "{ label: 'CEOs', href: '#ceos' }",
    text,
)

# Adiciona scroll manual se não existir
if "scrollToSection(event:" not in text:
    insert = """
  scrollToSection(event: Event, target: string | undefined): void {
    if (!target) {
      this.closeMenu();
      return;
    }

    event.preventDefault();

    const id = target.replace('#', '');
    const element = document.getElementById(id);

    if (element) {
      element.scrollIntoView({
        behavior: 'smooth',
        block: 'start',
      });

      history.replaceState(null, '', `#${id}`);
    }

    this.closeMenu();
  }

"""
    before, sep, after = text.rpartition("\n}")
    if not sep:
        raise SystemExit("Não encontrei fechamento da classe Home.")
    text = before + "\n" + insert + "}" + after

home_ts.write_text(text)

html = home_html.read_text()

# Garante id na seção CEOs
if 'id="ceos"' not in html:
    html = html.replace('<section class="ceos"', '<section id="ceos" class="ceos"', 1)

# Ajusta links do menu para usar scrollToSection quando for âncora
html = re.sub(
    r'\s+\(click\)="link\.href \? scrollToSection\(\$event, link\.href\) : closeMenu\(\)"',
    '',
    html,
)

html = re.sub(
    r'(<a[^>]*class="[^"]*nav__link[^"]*"[^>]*?)>',
    r'\1 (click)="link.href ? scrollToSection($event, link.href) : closeMenu()">',
    html,
)

home_html.write_text(html)

# =========================================================
# 2. CSS LANDING: LOGO MAIOR, CONTATO CENTRALIZADO, SCROLL
# =========================================================
css = home_scss.read_text()

final_home_css = r"""

/* =========================================================
   AJUSTES FINAIS DE LAYOUT — LANDING
   ========================================================= */

/* Links com header fixo */
#hero,
#ceos,
#cafes,
#bebidas,
#kits,
#cardapio-digital,
#diferenciais,
#contato {
  scroll-margin-top: 115px;
}

/* Logo maior no header/menu */
.header .logo,
.header__logo,
.logo {
  min-width: 132px;
  display: flex;
  align-items: center;
}

.header .logo img,
.logo__image,
.logo img,
.header__logo img {
  width: clamp(110px, 8vw, 150px) !important;
  max-height: 64px !important;
  object-fit: contain !important;
}

/* Contato completamente centralizado */
#contato,
.contact {
  text-align: center;
}

#contato .container,
.contact .container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

#contato .contact__links,
#contato .contact-links,
#contato .social-links,
.contact__links,
.contact-links,
.social-links {
  width: 100% !important;
  max-width: 620px !important;
  margin: 2rem auto 0 !important;
  display: grid !important;
  grid-template-columns: repeat(2, minmax(240px, 280px)) !important;
  justify-content: center !important;
  justify-items: stretch !important;
  gap: 1rem !important;
}

#contato .contact-card,
#contato .contact__card,
.contact-card,
.contact__card {
  width: 100% !important;
  min-height: 96px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  text-align: center !important;
  gap: 0.85rem !important;
}

#contato .contact-card *,
#contato .contact__card *,
.contact-card *,
.contact__card * {
  text-align: center !important;
}

#contato a,
.contact a {
  word-break: normal !important;
  overflow-wrap: anywhere !important;
}

@media (max-width: 640px) {
  #contato .contact__links,
  #contato .contact-links,
  #contato .social-links,
  .contact__links,
  .contact-links,
  .social-links {
    grid-template-columns: minmax(240px, 1fr) !important;
    max-width: 330px !important;
  }
}

/* Botão voltar ao topo com mascote */
.to-top,
.back-to-top {
  width: 66px !important;
  height: 66px !important;
  display: grid !important;
  place-items: center !important;
  border-radius: 999px !important;
  overflow: hidden !important;
}

.to-top img,
.back-to-top img {
  width: 44px !important;
  height: 44px !important;
  object-fit: contain !important;
}
"""

if "AJUSTES FINAIS DE LAYOUT — LANDING" not in css:
    css += final_home_css

home_scss.write_text(css)

# =========================================================
# 3. CARDÁPIO DIGITAL: LOGO MAIOR + GRID 4 / 2 / 1
# =========================================================
card_css = cardapio_scss.read_text()

final_card_css = r"""

/* =========================================================
   AJUSTES FINAIS — CARDÁPIO DIGITAL
   ========================================================= */

/* Logo maior no header do cardápio digital */
.cp-header img,
.cp-header__logo img,
.cp-header__wordmark,
.cp-header__brand img {
  width: clamp(110px, 9vw, 158px) !important;
  max-height: 72px !important;
  object-fit: contain !important;
}

/* Grid dos produtos: 4 colunas desktop, 2 tablet, 1 mobile */
.cp-products-grid,
.cp-grid,
.products-grid,
.cp-menu-grid {
  display: grid !important;
  grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
  gap: 1.25rem !important;
  align-items: stretch !important;
}

@media (max-width: 1180px) {
  .cp-products-grid,
  .cp-grid,
  .products-grid,
  .cp-menu-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
  }
}

@media (max-width: 640px) {
  .cp-products-grid,
  .cp-grid,
  .products-grid,
  .cp-menu-grid {
    grid-template-columns: 1fr !important;
  }
}

/* Mantém somente a imagem correta do produto, sem moldura artificial */
.cp-product-card__img-wrap,
.cp-product-image,
.cp-card__image,
.product-image {
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
  outline: 0 !important;
  padding: 1rem 1rem 0.25rem !important;
  min-height: 235px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}

.cp-product-card__img,
.cp-product-image img,
.cp-card__image img,
.product-image img {
  width: auto !important;
  max-width: 100% !important;
  height: 225px !important;
  max-height: 225px !important;
  object-fit: contain !important;
  border: 0 !important;
  border-radius: 0 !important;
  box-shadow: none !important;
  background: transparent !important;
}

@media (max-width: 640px) {
  .cp-product-card__img,
  .cp-product-image img,
  .cp-card__image img,
  .product-image img {
    height: 205px !important;
    max-height: 205px !important;
  }
}
"""

if "AJUSTES FINAIS — CARDÁPIO DIGITAL" not in card_css:
    card_css += final_card_css

cardapio_scss.write_text(card_css)

print("OK: ajustes aplicados sem alterar imagens.")
