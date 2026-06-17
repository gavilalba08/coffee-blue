from pathlib import Path
import re

html_path = Path("src/app/home/home.html")
ts_path = Path("src/app/home/home.ts")
scss_path = Path("src/app/home/home.scss")

html = html_path.read_text(encoding="utf-8")
ts = ts_path.read_text(encoding="utf-8")
scss = scss_path.read_text(encoding="utf-8")

# Garantir ID correto da seção CEOs
html = re.sub(
    r'(<section\s+class="section section--ceos ceos ceos--horizontal")\s+id="[^"]+"',
    r'\1 id="ceos"',
    html,
    count=1
)

# Remover possível ID antigo errado
html = html.replace('id="cafes-classicos"', 'id="ceos"')

# Evitar contato duplicado: só a seção Redes Sociais fica como contato
sections = re.findall(r'<section[\s\S]*?</section>', html)

for section in sections:
    if 'id="contato"' in section and "Redes Sociais" not in section:
        html = html.replace(section, section.replace('id="contato"', 'id="contato-extra"', 1), 1)

# Inserir anchor Bebidas Prontas antes do loop de readyDrinks
if 'id="bebidas-prontas"' not in html:
    pattern = r'(@for\s*\(\s*product\s+of\s+readyDrinks\b)'
    html, count = re.subn(
        pattern,
        '<div id="bebidas-prontas" class="scroll-anchor" aria-hidden="true"></div>\n        \\1',
        html,
        count=1
    )
    if count == 0:
        print("AVISO: não encontrei loop readyDrinks para inserir #bebidas-prontas")

# Inserir anchor Kits & Cápsulas antes do loop de capsuleDripProducts ou kitsProducts
if 'id="kits-capsulas"' not in html:
    pattern = r'(@for\s*\(\s*product\s+of\s+(?:capsuleDripProducts|kitsProducts)\b)'
    html, count = re.subn(
        pattern,
        '<div id="kits-capsulas" class="scroll-anchor" aria-hidden="true"></div>\n        \\1',
        html,
        count=1
    )
    if count == 0:
        print("AVISO: não encontrei loop capsuleDripProducts/kitsProducts para inserir #kits-capsulas")

# Garantir clique controlado nos links do menu
html = html.replace(
    '<a class="logo" href="#hero" (click)="closeMenu()">',
    '<a class="logo" href="#hero" (click)="goToAnchor(\'#hero\', $event)">'
)

html = html.replace(
    '<a class="nav__link" [href]="link.href">{{ link.label }}</a>',
    '<a class="nav__link" [href]="link.href" (click)="goToAnchor(link.href, $event)">{{ link.label }}</a>'
)

html = html.replace(
    '<a class="nav__link" [href]="link.href" (click)="closeMenu()">{{ link.label }}</a>',
    '<a class="nav__link" [href]="link.href" (click)="goToAnchor(link.href, $event)">{{ link.label }}</a>'
)

html_path.write_text(html, encoding="utf-8")

# Garantir navLinks corretos
new_navlinks = """readonly navLinks: readonly NavLink[] = [
    { label: 'Início', href: '#hero' },
    { label: 'CEOs', href: '#ceos' },
    { label: 'Nossos Cafés', href: '#cafes' },
    { label: 'Bebidas Prontas', href: '#bebidas-prontas' },
    { label: 'Kits & Cápsulas', href: '#kits-capsulas' },
    { label: 'Cardápio Digital', href: '#cardapio-digital' },
    { label: 'Diferenciais', href: '#diferenciais' },
    { label: 'Contato', href: '#contato' },
  ];"""

ts = re.sub(
    r"readonly navLinks: readonly NavLink\[\] = \[[\s\S]*?\];",
    new_navlinks,
    ts,
    count=1
)

# Garantir método goToAnchor
if "goToAnchor(" not in ts:
    method = """
  goToAnchor(href: string | undefined, event?: Event): void {
    if (!href || !href.startsWith('#')) {
      return;
    }

    event?.preventDefault();
    this.closeMenu();

    const id = href.replace('#', '');
    const target = document.getElementById(id);

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

# Garantir margem dos anchors por causa do header fixo
css_patch = """

/* PATCH MENU ANCHORS FINAL */
#hero,
#ceos,
#cafes,
#bebidas-prontas,
#kits-capsulas,
#cardapio-digital,
#diferenciais,
#contato,
.scroll-anchor {
  scroll-margin-top: 125px;
}

.scroll-anchor {
  display: block;
  width: 100%;
  height: 1px;
}
"""

if "PATCH MENU ANCHORS FINAL" not in scss:
    scss += css_patch

scss_path.write_text(scss, encoding="utf-8")

print("OK: anchors finais do menu corrigidos.")
