from pathlib import Path
import re

scss_path = Path("src/app/home/home.scss")
html_path = Path("src/app/home/home.html")
ts_path = Path("src/app/home/home.ts")

scss = scss_path.read_text(encoding="utf-8")
html = html_path.read_text(encoding="utf-8")
ts = ts_path.read_text(encoding="utf-8")

# 1) Garantir que links do menu fecham ao clicar
html = re.sub(
    r'<a class="nav__link" \[href\]="link\.href" \(click\)="goToAnchor\(link\.href, \$event\)(?:; closeMenu\(\))?"',
    '<a class="nav__link" [href]="link.href" (click)="goToAnchor(link.href, $event); closeMenu()"',
    html
)

# 2) Garantir clique fora fechando menu
ts = re.sub(
    r"import \{([^}]*?)\} from '@angular/core';",
    lambda m: "import {" + (
        m.group(1) if "HostListener" in m.group(1)
        else m.group(1).rstrip() + ", HostListener"
    ) + "} from '@angular/core';",
    ts,
    count=1
)

if "onMobileMenuDocumentClick" not in ts:
    method = r"""
  @HostListener('document:click', ['$event'])
  onMobileMenuDocumentClick(event: MouseEvent): void {
    if (!this.isMenuOpen()) return;

    const target = event.target as HTMLElement | null;
    if (!target) return;

    if (target.closest('.nav') || target.closest('.menu-toggle')) {
      return;
    }

    this.closeMenu();
  }

"""
    if "  toggleMenu(): void {" in ts:
        ts = ts.replace("  toggleMenu(): void {", method + "  toggleMenu(): void {", 1)
    else:
        ts = ts.rstrip().replace("\n}", method + "\n}", 1)

# 3) Remove patches antigos grandes/duplicados do mobile para não estourar budget
for marker in [
    "PATCH FINAL — HEADER MOBILE COFFEE BLUE",
    "PATCH FINAL — MENU MOBILE ABERTO MAIOR E FECHAMENTO",
    "PATCH FINAL — MENU MOBILE COMPACTO",
    "PATCH MOBILE FINAL — HEADER MENU E PRODUTOS",
]:
    scss = re.sub(
        rf"/\* {re.escape(marker)} \*/[\s\S]*?(?=/\* PATCH|$)",
        "",
        scss
    )

# Remove regra que escondia o botão em telas pequenas
scss = re.sub(
    r"@media\s*\(max-width:\s*380px\)\s*\{[\s\S]*?\.nav__cta\s*\{[\s\S]*?display:\s*none\s*!important;[\s\S]*?\}[\s\S]*?\}",
    "",
    scss
)

patch = r'''

/* PATCH MOBILE FINAL — HEADER MENU E PRODUTOS */
@media (max-width: 920px) {
  .header,
  .header__inner {
    overflow: visible !important;
  }

  .header__inner {
    min-height: 86px !important;
    height: 86px !important;
    padding: 0 1rem !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    gap: .65rem !important;
  }

  .header .logo,
  .header.header--scrolled .logo,
  .header__inner .logo {
    width: 132px !important;
    min-width: 132px !important;
    height: 76px !important;
    flex: 0 0 132px !important;
    z-index: 150 !important;
  }

  .header .logo__image,
  .header.header--scrolled .logo__image,
  .header__inner .logo__image {
    height: 64px !important;
    max-height: 64px !important;
    max-width: 132px !important;
    display: block !important;
    object-fit: contain !important;
  }

  .header__actions {
    display: flex !important;
    align-items: center !important;
    justify-content: flex-end !important;
    gap: .55rem !important;
    z-index: 170 !important;
  }

  /* Botão Cardápio Digital fica visível no mobile */
  .nav__cta {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    min-height: 44px !important;
    max-width: none !important;
    padding: .7rem 1rem !important;
    border-radius: 999px !important;
    font-size: .84rem !important;
    font-weight: 800 !important;
    line-height: 1 !important;
    white-space: nowrap !important;
    flex: 0 0 auto !important;
  }

  .menu-toggle {
    display: inline-flex !important;
    width: 48px !important;
    height: 48px !important;
    min-width: 48px !important;
    border-radius: 999px !important;
    border: 1px solid rgba(227, 182, 75, .65) !important;
    background: rgba(2, 20, 44, .94) !important;
    align-items: center !important;
    justify-content: center !important;
    flex-direction: column !important;
    gap: 6px !important;
    padding: 0 !important;
    z-index: 180 !important;
  }

  .menu-toggle__bar {
    display: block !important;
    width: 20px !important;
    height: 2px !important;
    border-radius: 999px !important;
    background: #f7efe1 !important;
    transition: transform 180ms ease, opacity 180ms ease !important;
  }

  .menu-toggle--active .menu-toggle__bar:nth-child(1) {
    transform: translateY(8px) rotate(45deg) !important;
  }

  .menu-toggle--active .menu-toggle__bar:nth-child(2) {
    opacity: 0 !important;
  }

  .menu-toggle--active .menu-toggle__bar:nth-child(3) {
    transform: translateY(-8px) rotate(-45deg) !important;
  }

  /* Caixa do menu hambúrguer com altura da lista completa */
  .nav {
    position: absolute !important;
    left: 1rem !important;
    right: 1rem !important;
    top: calc(100% + .75rem) !important;
    z-index: 160 !important;

    width: auto !important;
    height: auto !important;
    min-height: auto !important;
    max-height: none !important;
    overflow: visible !important;

    padding: 1rem !important;
    border-radius: 24px !important;
    border: 1px solid rgba(227, 182, 75, .38) !important;
    background: linear-gradient(145deg, rgba(2, 20, 44, .99), rgba(8, 33, 59, .99)) !important;
    box-shadow: 0 28px 80px rgba(2, 20, 44, .48) !important;

    opacity: 0 !important;
    visibility: hidden !important;
    pointer-events: none !important;
    transform: translateY(-10px) scale(.98) !important;
    transition: opacity 180ms ease, visibility 180ms ease, transform 180ms ease !important;
  }

  .nav.nav--open {
    opacity: 1 !important;
    visibility: visible !important;
    pointer-events: auto !important;
    transform: translateY(0) scale(1) !important;
  }

  .nav__list {
    display: flex !important;
    flex-direction: column !important;
    gap: .42rem !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    list-style: none !important;
  }

  .nav__item {
    width: 100% !important;
  }

  .nav__link {
    width: 100% !important;
    min-height: 48px !important;
    display: flex !important;
    align-items: center !important;
    padding: .82rem 1rem !important;
    border-radius: 16px !important;
    color: #f7efe1 !important;
    background: rgba(255, 255, 255, .045) !important;
    border: 1px solid rgba(255, 255, 255, .06) !important;
    font-size: .98rem !important;
    font-weight: 700 !important;
    text-decoration: none !important;
  }

  .nav__link:hover,
  .nav__link:focus-visible {
    color: #e3b64b !important;
    background: rgba(227, 182, 75, .12) !important;
    border-color: rgba(227, 182, 75, .32) !important;
  }

  /* Corrige imagens do componente Outros Produtos no mobile */
  #produtos img,
  .section--dark img,
  .product-card img,
  .product-image img,
  .product-card__image img,
  .products-grid img,
  .menu-product-card img {
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
    width: 100% !important;
    max-width: 100% !important;
    height: auto !important;
    min-height: 0 !important;
    max-height: none !important;
    object-fit: contain !important;
    transform: none !important;
  }

  #produtos .product-card,
  #produtos .menu-product-card,
  #produtos .product-image,
  #produtos .product-card__image {
    overflow: visible !important;
  }
}

@media (max-width: 520px) {
  .header__inner {
    min-height: 84px !important;
    height: 84px !important;
    padding: 0 .8rem !important;
    gap: .45rem !important;
  }

  .header .logo,
  .header.header--scrolled .logo,
  .header__inner .logo {
    width: 122px !important;
    min-width: 122px !important;
    height: 72px !important;
    flex-basis: 122px !important;
  }

  .header .logo__image,
  .header.header--scrolled .logo__image,
  .header__inner .logo__image {
    height: 58px !important;
    max-height: 58px !important;
    max-width: 122px !important;
  }

  .nav__cta {
    min-height: 42px !important;
    padding: .66rem .9rem !important;
    font-size: .8rem !important;
  }

  .menu-toggle {
    width: 46px !important;
    height: 46px !important;
    min-width: 46px !important;
  }

  .nav {
    left: .8rem !important;
    right: .8rem !important;
    top: calc(100% + .65rem) !important;
    padding: .9rem !important;
    border-radius: 22px !important;
  }

  .nav__link {
    min-height: 47px !important;
    padding: .8rem .95rem !important;
    font-size: .95rem !important;
  }
}

@media (max-width: 390px) {
  .header .logo,
  .header.header--scrolled .logo,
  .header__inner .logo {
    width: 112px !important;
    min-width: 112px !important;
    flex-basis: 112px !important;
  }

  .header .logo__image,
  .header.header--scrolled .logo__image,
  .header__inner .logo__image {
    height: 54px !important;
    max-height: 54px !important;
    max-width: 112px !important;
  }

  .nav__cta {
    padding: .62rem .75rem !important;
    font-size: .75rem !important;
  }

  .menu-toggle {
    width: 44px !important;
    height: 44px !important;
    min-width: 44px !important;
  }
}
'''

scss = scss.rstrip() + "\n" + patch + "\n"

scss_path.write_text(scss, encoding="utf-8")
html_path.write_text(html, encoding="utf-8")
ts_path.write_text(ts, encoding="utf-8")

print("OK: mobile final corrigido.")
