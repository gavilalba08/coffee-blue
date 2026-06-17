from pathlib import Path
import re

ts_path = Path("src/app/home/home.ts")
html_path = Path("src/app/home/home.html")
scss_path = Path("src/app/home/home.scss")

ts = ts_path.read_text(encoding="utf-8")
html = html_path.read_text(encoding="utf-8")
scss = scss_path.read_text(encoding="utf-8")

# 1) Menu definitivo: remove Kits & Cápsulas, adiciona Cafeteria
nav_block = """  readonly navLinks: readonly NavLink[] = [
    { label: 'Início', href: '#hero' },
    { label: 'CEOs', href: '#ceos' },
    { label: 'Nossos Cafés', href: '#cafes' },
    { label: 'Bebidas Prontas', href: '#produtos' },
    { label: 'Cardápio Digital', href: '#cardapio-digital' },
    { label: 'Diferenciais', href: '#diferenciais' },
    { label: 'Cafeteria', href: '#cafeteria' },
    { label: 'Contato', href: '#contato' },
  ];"""

ts = re.sub(
    r"  readonly navLinks: readonly NavLink\[\] = \[[\s\S]*?\n  \];",
    nav_block,
    ts,
    count=1
)

# 2) Método definitivo de rolagem: calcula altura real do header
go_to_anchor = """  goToAnchor(href: string | undefined, event?: Event): void {
    event?.preventDefault();

    if (!href || !href.startsWith('#')) {
      return;
    }

    const targetId = href.slice(1);
    const target = document.getElementById(targetId);

    if (!target) {
      return;
    }

    this.closeMenu();

    const header = document.querySelector<HTMLElement>('.header');
    const headerHeight = header?.getBoundingClientRect().height ?? 0;
    const extraGap = 6;

    const targetTop = target.getBoundingClientRect().top + window.scrollY;
    const scrollTop = Math.max(targetTop - headerHeight - extraGap, 0);

    window.history.replaceState(null, '', href);
    window.scrollTo({ top: scrollTop, behavior: 'smooth' });
  }"""

if "  goToAnchor(" in ts:
    start = ts.find("  goToAnchor(")
    end_marker = "\n\n  toggleMenu(): void {"
    end = ts.find(end_marker, start)

    if end == -1:
        raise SystemExit("Não encontrei o método toggleMenu depois de goToAnchor.")

    ts = ts[:start] + go_to_anchor + ts[end:]
else:
    marker = "  toggleMenu(): void {"
    if marker not in ts:
        raise SystemExit("Não encontrei toggleMenu para inserir goToAnchor.")
    ts = ts.replace(marker, go_to_anchor + "\n\n" + marker, 1)

ts_path.write_text(ts, encoding="utf-8")

# 3) IDs corretos no HTML
html = re.sub(
    r'<section([^>]*class="[^"]*\bceos\b[^"]*"[^>]*)id="[^"]*"',
    r'<section\1id="ceos"',
    html,
    count=1
)

html = html.replace('id="contato-extra"', 'id="cafeteria"')

# 4) Garantir clique correto no logo e nos links
html = re.sub(
    r'<a class="logo" href="#hero"[^>]*>',
    "<a class=\"logo\" href=\"#hero\" (click)=\"goToAnchor('#hero', $event)\">",
    html,
    count=1
)

html = re.sub(
    r'<a class="nav__link" \[href\]="link\.href"[^>]*>\{\{\s*link\.label\s*\}\}</a>',
    '<a class="nav__link" [href]="link.href" (click)="goToAnchor(link.href, $event)">{{ link.label }}</a>',
    html
)

html_path.write_text(html, encoding="utf-8")

# 5) CSS definitivo para âncoras
css_patch = """

/* PATCH DEFINITIVO — MENU / ANCHORS */
html {
  scroll-behavior: smooth;
  scroll-padding-top: 78px;
}

#hero,
#ceos,
#cafes,
#produtos,
#cardapio-digital,
#diferenciais,
#cafeteria,
#contato {
  scroll-margin-top: 78px;
}
"""

if "PATCH DEFINITIVO — MENU / ANCHORS" not in scss:
    scss += css_patch

scss_path.write_text(scss, encoding="utf-8")

print("OK: menu, IDs e rolagem corrigidos.")
