from pathlib import Path
import re

html_path = Path("src/app/home/home.html")
ts_path = Path("src/app/home/home.ts")
scss_path = Path("src/app/home/home.scss")

html = html_path.read_text(encoding="utf-8")
ts = ts_path.read_text(encoding="utf-8")
scss = scss_path.read_text(encoding="utf-8")

# 1) Garante que links do menu fecham ao clicar.
html = re.sub(
    r'<a class="nav__link" \[href\]="link\.href" \(click\)="goToAnchor\(link\.href, \$event\)"',
    '<a class="nav__link" [href]="link.href" (click)="goToAnchor(link.href, $event); closeMenu()"',
    html
)

# Caso tenha algum link sem closeMenu.
html = re.sub(
    r'<a class="nav__link" \[routerLink\]="link\.routerLink" \(click\)="closeMenu\(\)"',
    '<a class="nav__link" [routerLink]="link.routerLink" (click)="closeMenu()"',
    html
)

html_path.write_text(html, encoding="utf-8")

# 2) Garante HostListener importado.
ts = re.sub(
    r"import \{([^}]*?)\} from '@angular/core';",
    lambda m: "import {" + (
        m.group(1) if "HostListener" in m.group(1)
        else m.group(1).rstrip() + ", HostListener"
    ) + "} from '@angular/core';",
    ts,
    count=1
)

# 3) Remove listener antigo se existir.
ts = re.sub(
    r"\n\s*@HostListener\('document:click', \['\$event'\]\)\s*\n\s*onMobileMenuDocumentClick\([^)]*\): void \{[\s\S]*?\n\s*\}\n(?=\s*(?:@HostListener|toggleMenu|closeMenu|goToAnchor|scrollToTop|$))",
    "\n",
    ts
)

# 4) Adiciona clique fora para fechar menu.
method = r"""
  @HostListener('document:click', ['$event'])
  onMobileMenuDocumentClick(event: MouseEvent): void {
    if (!this.isMenuOpen()) return;

    const target = event.target as HTMLElement | null;
    if (!target) return;

    const clickedInsideHeader = target.closest('.header');
    const clickedInsideNav = target.closest('.nav');
    const clickedToggle = target.closest('.menu-toggle');

    if (clickedInsideNav || clickedToggle || clickedInsideHeader) {
      return;
    }

    this.closeMenu();
  }

"""

if "onMobileMenuDocumentClick" not in ts:
    if "  toggleMenu(): void {" in ts:
        ts = ts.replace("  toggleMenu(): void {", method + "  toggleMenu(): void {", 1)
    else:
        ts = ts.rstrip().replace("\n}", method + "\n}", 1)

# 5) Escape também fecha menu, se já existir mantém.
if "@HostListener('document:keydown.escape')" in ts:
    ts = re.sub(
        r"@HostListener\('document:keydown.escape'\)\s*\n\s*\w+\(\): void \{([\s\S]*?)\n\s*\}",
        lambda m: m.group(0) if "closeMenu()" in m.group(0) else m.group(0).replace("{", "{\n    this.closeMenu();", 1),
        ts,
        count=1
    )

ts_path.write_text(ts, encoding="utf-8")

# 6) CSS mobile: caixa maior, altura da lista, sem ficar aquela barra fina.
scss = re.sub(
    r"/\* PATCH FINAL — MENU MOBILE ABERTO MAIOR E FECHAMENTO \*/[\s\S]*?(?=/\* PATCH|$)",
    "",
    scss
).rstrip()

patch = r'''

/* PATCH FINAL — MENU MOBILE ABERTO MAIOR E FECHAMENTO */
@media (max-width: 920px) {
  .header {
    overflow: visible !important;
  }

  .header__inner {
    overflow: visible !important;
  }

  .nav {
    position: absolute !important;
    left: 1rem !important;
    right: 1rem !important;
    top: calc(100% + 0.8rem) !important;
    width: auto !important;
    min-height: auto !important;
    height: auto !important;
    max-height: calc(100vh - 130px) !important;
    overflow-y: auto !important;
    z-index: 120 !important;

    padding: 1rem !important;
    border-radius: 26px !important;
    border: 1px solid rgba(227, 182, 75, 0.34) !important;

    background:
      radial-gradient(circle at 12% 0%, rgba(227, 182, 75, 0.18), transparent 34%),
      linear-gradient(145deg, rgba(2, 20, 44, 0.99), rgba(8, 33, 59, 0.99)) !important;

    box-shadow: 0 28px 80px rgba(2, 20, 44, 0.48) !important;

    opacity: 0 !important;
    visibility: hidden !important;
    pointer-events: none !important;
    transform: translateY(-10px) scale(0.98) !important;
    transition:
      opacity 180ms ease,
      visibility 180ms ease,
      transform 180ms ease !important;
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
    gap: 0.45rem !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
  }

  .nav__item {
    display: block !important;
    width: 100% !important;
  }

  .nav__link {
    width: 100% !important;
    min-height: 52px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;

    padding: 0.9rem 1.05rem !important;
    border-radius: 18px !important;

    color: #f7efe1 !important;
    background: rgba(255, 255, 255, 0.045) !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;

    font-size: 1rem !important;
    font-weight: 700 !important;
    line-height: 1.1 !important;
    letter-spacing: 0.01em !important;
    text-decoration: none !important;
  }

  .nav__link:hover,
  .nav__link:focus-visible {
    color: #e3b64b !important;
    background: rgba(227, 182, 75, 0.12) !important;
    border-color: rgba(227, 182, 75, 0.32) !important;
  }

  .menu-toggle {
    z-index: 140 !important;
  }

  .header__actions {
    z-index: 140 !important;
  }

  .nav__cta {
    z-index: 140 !important;
  }
}

@media (max-width: 520px) {
  .nav {
    left: 0.8rem !important;
    right: 0.8rem !important;
    top: calc(100% + 0.7rem) !important;
    padding: 0.85rem !important;
    border-radius: 22px !important;
    max-height: calc(100vh - 120px) !important;
  }

  .nav__list {
    gap: 0.38rem !important;
  }

  .nav__link {
    min-height: 50px !important;
    padding: 0.86rem 0.95rem !important;
    font-size: 0.96rem !important;
    border-radius: 16px !important;
  }
}
'''

scss = scss + "\n" + patch + "\n"
scss_path.write_text(scss, encoding="utf-8")

print("OK: menu mobile maior e fechamento por opção, fora ou X aplicado.")
