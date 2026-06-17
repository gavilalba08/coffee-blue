from pathlib import Path
import re

html_path = Path("src/app/home/home.html")
ts_path = Path("src/app/home/home.ts")
scss_path = Path("src/app/home/home.scss")

html = html_path.read_text(encoding="utf-8")
ts = ts_path.read_text(encoding="utf-8")
scss = scss_path.read_text(encoding="utf-8")

# 1) Corrigir ID da seção CEOs
html = re.sub(
    r'(<section\s+class="section section--ceos ceos ceos--horizontal")\s+id="[^"]+"',
    r'\1 id="ceos"',
    html,
    count=1
)

# 2) Corrigir clique da logo para usar rolagem controlada
html = html.replace(
    '<a class="logo" href="#hero" (click)="closeMenu()">',
    '<a class="logo" href="#hero" (click)="goToAnchor(\'#hero\', $event)">'
)

# 3) Corrigir links normais do menu para usar rolagem controlada
html = html.replace(
    '<a class="nav__link" [href]="link.href">{{ link.label }}</a>',
    '<a class="nav__link" [href]="link.href" (click)="goToAnchor(link.href, $event)">{{ link.label }}</a>'
)

# 4) Inserir anchors auxiliares para Bebidas Prontas e Kits & Cápsulas, caso não existam
if 'id="bebidas-prontas"' not in html:
    html = html.replace(
        '@for (product of readyDrinks; track product.name) {',
        '<div id="bebidas-prontas" class="scroll-anchor"></div>\n        @for (product of readyDrinks; track product.name) {',
        1
    )

if 'id="kits-capsulas"' not in html:
    html = html.replace(
        '@for (product of capsuleDripProducts; track product.name) {',
        '<div id="kits-capsulas" class="scroll-anchor"></div>\n        @for (product of capsuleDripProducts; track product.name) {',
        1
    )

# 5) Resolver IDs duplicados de contato:
# mantém id="contato" somente na seção que contém "Redes Sociais"
def fix_contact_ids(match):
    section = match.group(0)
    if "Redes Sociais" in section or "Redes Sociais & Contato" in section:
        return section.replace('id="contato"', 'id="contato"', 1)
    return section.replace('id="contato"', 'id="contato-extra"', 1)

html = re.sub(
    r'<section[^>]*id="contato"[\s\S]*?</section>',
    fix_contact_ids,
    html
)

html_path.write_text(html, encoding="utf-8")

# 6) Padronizar navLinks no TS
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

# 7) Criar função de rolagem confiável
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

# 8) Scroll margin para o header fixo não cobrir o começo da seção
css_patch = """

/* PATCH MENU ANCHORS */
#hero,
#ceos,
#cafes,
#bebidas-prontas,
#kits-capsulas,
#cardapio-digital,
#diferenciais,
#contato,
.scroll-anchor {
  scroll-margin-top: 120px;
}

.scroll-anchor {
  display: block;
  height: 1px;
  width: 100%;
}
"""

if "PATCH MENU ANCHORS" not in scss:
    scss += css_patch

scss_path.write_text(scss, encoding="utf-8")

print("OK: links do menu/header corrigidos.")
