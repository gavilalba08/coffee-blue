from pathlib import Path
import re

home_ts = Path("src/app/home/home.ts")
home_html = Path("src/app/home/home.html")
home_scss = Path("src/app/home/home.scss")
card_html = Path("src/app/cardapio/cardapio.html")
card_scss = Path("src/app/cardapio/cardapio.scss")
styles = Path("src/styles.scss")

# =========================================================
# 1) HOME.TS — menu limpo, sem depender de função quebrada
# =========================================================
ts = home_ts.read_text(encoding="utf-8")

new_nav = """  readonly navLinks: readonly NavLink[] = [
    { label: 'Início', href: '#hero' },
    { label: 'CEOs', href: '#ceos' },
    { label: 'Nossos Cafés', href: '#cafes-classicos' },
    { label: 'Bebidas Prontas', href: '#bebidas-prontas' },
    { label: 'Kits & Cápsulas', href: '#kits-capsulas' },
    { label: 'Cardápio Digital', href: '#cardapio-digital' },
    { label: 'Diferenciais', href: '#diferenciais' },
    { label: 'Contato', href: '#contato' },
  ];"""

ts = re.sub(
    r"  readonly navLinks: readonly NavLink\[\] = \[[\s\S]*?\];",
    new_nav,
    ts,
    count=1
)

# Remove scrollToSection duplicado/antigo, se ainda existir
def remove_method(text: str, method_name: str) -> str:
    pattern = re.compile(rf"\n\s{{2}}{method_name}\s*\([^)]*\)\s*:\s*void\s*\{{")
    while True:
        m = pattern.search(text)
        if not m:
            return text
        start = m.start()
        brace = text.find("{", m.end() - 1)
        depth = 0
        end = None
        for i in range(brace, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        if end is None:
            raise SystemExit(f"Não consegui remover {method_name}")
        text = text[:start] + text[end:]

ts = remove_method(ts, "scrollToSection")

# Mantém só closeMenu/top, sem função de menu quebrada
home_ts.write_text(ts, encoding="utf-8")

# =========================================================
# 2) HOME.HTML — header com âncoras nativas funcionando
# =========================================================
html = home_html.read_text(encoding="utf-8")

# Garante IDs principais
replacements = {
    r'<section class="hero"': '<section id="hero" class="hero"',
    r'<section class="ceos"': '<section id="ceos" class="ceos"',
    r'<section class="section section--dark coffees"': '<section id="cafes-classicos" class="section section--dark coffees"',
    r'<section class="section ready-drinks"': '<section id="bebidas-prontas" class="section ready-drinks"',
    r'<section class="section kits"': '<section id="kits-capsulas" class="section kits"',
    r'<section class="section cardapio"': '<section id="cardapio-digital" class="section cardapio"',
    r'<section class="section differentials"': '<section id="diferenciais" class="section differentials"',
    r'<section class="section contact"': '<section id="contato" class="section contact"',
}

for old, new in replacements.items():
    if new not in html:
        html = html.replace(old, new, 1)

# Remove IDs duplicados caso algum script anterior já tenha colocado
html = re.sub(r'<section id="hero" id="hero"', '<section id="hero"', html)
html = re.sub(r'<section id="ceos" id="ceos"', '<section id="ceos"', html)
html = re.sub(r'<section id="cafes-classicos" id="cafes-classicos"', '<section id="cafes-classicos"', html)
html = re.sub(r'<section id="bebidas-prontas" id="bebidas-prontas"', '<section id="bebidas-prontas"', html)
html = re.sub(r'<section id="kits-capsulas" id="kits-capsulas"', '<section id="kits-capsulas"', html)
html = re.sub(r'<section id="cardapio-digital" id="cardapio-digital"', '<section id="cardapio-digital"', html)
html = re.sub(r'<section id="diferenciais" id="diferenciais"', '<section id="diferenciais"', html)
html = re.sub(r'<section id="contato" id="contato"', '<section id="contato"', html)

# Substitui o nav inteiro por uma versão simples e funcional
nav_static = """<nav class="nav__links" aria-label="Menu principal">
          <a class="nav__link" href="#hero" (click)="closeMenu()">Início</a>
          <a class="nav__link" href="#ceos" (click)="closeMenu()">CEOs</a>
          <a class="nav__link" href="#cafes-classicos" (click)="closeMenu()">Nossos Cafés</a>
          <a class="nav__link" href="#bebidas-prontas" (click)="closeMenu()">Bebidas Prontas</a>
          <a class="nav__link" href="#kits-capsulas" (click)="closeMenu()">Kits & Cápsulas</a>
          <a class="nav__link" href="#cardapio-digital" (click)="closeMenu()">Cardápio Digital</a>
          <a class="nav__link" href="#diferenciais" (click)="closeMenu()">Diferenciais</a>
          <a class="nav__link" href="#contato" (click)="closeMenu()">Contato</a>
        </nav>"""

html, nav_count = re.subn(
    r'<nav class="nav__links"[\s\S]*?</nav>',
    nav_static,
    html,
    count=1
)

if nav_count == 0:
    print("AVISO: não encontrei nav__links para substituir.")

# Botão principal do header para rota real do cardápio
html = re.sub(
    r'<a class="nav__cta"[\s\S]*?</a>',
    '<a class="nav__cta" routerLink="/cardapiodigital" (click)="closeMenu()">Cardápio Digital</a>',
    html,
    count=1
)

# Remove click errado em contato externo, se existir
html = re.sub(
    r'\s*\(click\)="scrollToSection\(link\.href,\s*\$event\)"',
    '',
    html
)

home_html.write_text(html, encoding="utf-8")

# =========================================================
# 3) CARDÁPIO HTML — logo maior já via CSS; manter rota
# =========================================================
if card_html.exists():
    ch = card_html.read_text(encoding="utf-8")
    # Não mexe nas imagens dos produtos. Apenas evita classes de moldura no HTML, se existirem.
    ch = ch.replace('class="cp-product-card__img-wrap cp-product-card__img-wrap--framed"', 'class="cp-product-card__img-wrap"')
    card_html.write_text(ch, encoding="utf-8")

# =========================================================
# 4) CSS GLOBAL — scroll nativo com header fixo
# =========================================================
global_css = styles.read_text(encoding="utf-8")

append_global = """

/* =========================================================
   PATCH FINAL — ÂNCORAS DO MENU
   ========================================================= */
html {
  scroll-behavior: smooth;
  scroll-padding-top: 96px;
}

section[id],
#hero,
#ceos,
#cafes-classicos,
#bebidas-prontas,
#kits-capsulas,
#cardapio-digital,
#diferenciais,
#contato {
  scroll-margin-top: 96px;
}
"""

if "PATCH FINAL — ÂNCORAS DO MENU" not in global_css:
    global_css += append_global

styles.write_text(global_css, encoding="utf-8")

# =========================================================
# 5) HOME.SCSS — logo maior + contato centralizado
# =========================================================
hs = home_scss.read_text(encoding="utf-8")

append_home = """

/* =========================================================
   PATCH FINAL — HEADER, LOGO, CONTATO
   ========================================================= */

/* Logo maior na landing page */
.header .brand,
.header__brand,
.nav__brand,
.logo,
.brand {
  display: inline-flex !important;
  align-items: center !important;
  flex: 0 0 auto !important;
}

.header .brand img,
.header__brand img,
.nav__brand img,
.logo img,
.logo__image,
.brand img,
img.logo__image {
  width: clamp(92px, 7vw, 150px) !important;
  min-width: 92px !important;
  max-width: 150px !important;
  height: auto !important;
  max-height: 72px !important;
  object-fit: contain !important;
}

/* Menu do header: links reais e clicáveis */
.nav__links {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: clamp(1rem, 1.7vw, 2rem) !important;
}

.nav__link {
  cursor: pointer !important;
  text-decoration: none !important;
  white-space: nowrap !important;
}

/* Contato realmente centralizado */
#contato,
.contact {
  text-align: center !important;
}

#contato .container,
.contact .container {
  margin-left: auto !important;
  margin-right: auto !important;
  text-align: center !important;
}

.contact__links,
.contact__cards,
.contact-grid,
.contacts-grid {
  width: 100% !important;
  max-width: 720px !important;
  margin-left: auto !important;
  margin-right: auto !important;
  display: grid !important;
  grid-template-columns: repeat(2, minmax(220px, 1fr)) !important;
  justify-content: center !important;
  justify-items: center !important;
  align-items: stretch !important;
  gap: 1.25rem !important;
}

.contact__card {
  width: 100% !important;
  max-width: 280px !important;
  margin-left: auto !important;
  margin-right: auto !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  text-align: left !important;
}

@media (max-width: 640px) {
  .contact__links,
  .contact__cards,
  .contact-grid,
  .contacts-grid {
    grid-template-columns: 1fr !important;
    max-width: 320px !important;
  }
}
"""

if "PATCH FINAL — HEADER, LOGO, CONTATO" not in hs:
    hs += append_home

home_scss.write_text(hs, encoding="utf-8")

# =========================================================
# 6) CARDAPIO.SCSS — 4 produtos lado a lado + logo maior
# =========================================================
if card_scss.exists():
    cs = card_scss.read_text(encoding="utf-8")

    append_card = """

/* =========================================================
   PATCH FINAL — CARDÁPIO DIGITAL
   ========================================================= */

/* Logo maior no header do cardápio */
.cp-header img,
.cp-header__logo img,
.cp-header__wordmark,
.cp-brand img,
.cp-header__brand img {
  width: clamp(90px, 7vw, 150px) !important;
  min-width: 90px !important;
  max-width: 150px !important;
  height: auto !important;
  max-height: 72px !important;
  object-fit: contain !important;
}

/* Grid do cardápio: 4 lado a lado no desktop */
.cp-products-grid,
.cp-product-grid,
.cp-menu-grid,
.products-grid,
.menu-grid,
.cp-products {
  display: grid !important;
  grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
  gap: 1.25rem !important;
  align-items: stretch !important;
}

/* Mantém a foto do produto limpa, sem moldura azul/moldura interna */
.cp-product-card__img-wrap,
.cp-product-image,
.cp-card__image,
.product-image {
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
  outline: 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 1rem !important;
  min-height: 250px !important;
}

.cp-product-card__img,
.cp-product-image img,
.cp-card__image img,
.product-image img {
  width: 100% !important;
  height: 245px !important;
  max-height: 245px !important;
  object-fit: contain !important;
  border: 0 !important;
  border-radius: 0 !important;
  box-shadow: none !important;
  background: transparent !important;
}

/* Tablet: 2x2 */
@media (max-width: 1100px) {
  .cp-products-grid,
  .cp-product-grid,
  .cp-menu-grid,
  .products-grid,
  .menu-grid,
  .cp-products {
    grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
  }
}

/* Mobile: torre */
@media (max-width: 640px) {
  .cp-products-grid,
  .cp-product-grid,
  .cp-menu-grid,
  .products-grid,
  .menu-grid,
  .cp-products {
    grid-template-columns: 1fr !important;
  }

  .cp-product-card__img,
  .cp-product-image img,
  .cp-card__image img,
  .product-image img {
    height: 220px !important;
    max-height: 220px !important;
  }
}
"""

    if "PATCH FINAL — CARDÁPIO DIGITAL" not in cs:
        cs += append_card

    card_scss.write_text(cs, encoding="utf-8")

print("OK: patch final aplicado.")
