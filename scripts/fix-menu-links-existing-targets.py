from pathlib import Path
import re

ts_path = Path("src/app/home/home.ts")
html_path = Path("src/app/home/home.html")
scss_path = Path("src/app/home/home.scss")

ts = ts_path.read_text(encoding="utf-8")
html = html_path.read_text(encoding="utf-8")
scss = scss_path.read_text(encoding="utf-8")

# 1) Menu apontando somente para IDs que existem hoje no HTML
navlinks = """readonly navLinks: readonly NavLink[] = [
    { label: 'Início', href: '#hero' },
    { label: 'CEOs', href: '#ceos' },
    { label: 'Nossos Cafés', href: '#cafes' },
    { label: 'Bebidas Prontas', href: '#produtos' },
    { label: 'Kits & Cápsulas', href: '#produtos' },
    { label: 'Cardápio Digital', href: '#cardapio-digital' },
    { label: 'Diferenciais', href: '#diferenciais' },
    { label: 'Contato', href: '#contato' },
  ];"""

ts, count = re.subn(
    r"readonly navLinks: readonly NavLink\[\] = \[[\s\S]*?\];",
    navlinks,
    ts,
    count=1
)

if count == 0:
    raise SystemExit("ERRO: não encontrei readonly navLinks no home.ts")

# 2) Garantir método de scroll suave
if "goToAnchor(" not in ts:
    method = """
  goToAnchor(href: string | undefined, event?: Event): void {
    if (!href || !href.startsWith('#')) {
      return;
    }

    event?.preventDefault();
    this.closeMenu();

    const target = document.querySelector(href);

    if (!target) {
      return;
    }

    target.scrollIntoView({
      behavior: 'smooth',
      block: 'start',
    });

    history.replaceState(null, '', href);
  }

"""
    ts = ts.replace("  toggleMenu(): void {", method + "  toggleMenu(): void {", 1)

ts_path.write_text(ts, encoding="utf-8")

# 3) Garantir clique do logo e dos links chamando goToAnchor
html = re.sub(
    r'<a class="logo" href="#hero"[^>]*>',
    '<a class="logo" href="#hero" (click)="goToAnchor(\'#hero\', $event)">',
    html,
    count=1
)

html = re.sub(
    r'<a class="nav__link" \[href\]="link\.href"[^>]*>\{\{ link\.label \}\}</a>',
    '<a class="nav__link" [href]="link.href" (click)="goToAnchor(link.href, $event)">{{ link.label }}</a>',
    html
)

html_path.write_text(html, encoding="utf-8")

# 4) Scroll margin para compensar header fixo
css_patch = """

/* PATCH MENU LINKS EXISTENTES */
#hero,
#ceos,
#cafes,
#produtos,
#cardapio-digital,
#diferenciais,
#contato {
  scroll-margin-top: 125px;
}
"""

if "PATCH MENU LINKS EXISTENTES" not in scss:
    scss += css_patch

scss_path.write_text(scss, encoding="utf-8")

print("OK: menu corrigido para apontar somente para IDs existentes.")
