from pathlib import Path
import re

ts_path = Path("src/app/home/home.ts")
scss_path = Path("src/app/home/home.scss")

ts = ts_path.read_text(encoding="utf-8")
scss = scss_path.read_text(encoding="utf-8")

new_method = """  goToAnchor(href: string | undefined, event?: Event): void {
    if (!href || !href.startsWith('#')) {
      return;
    }

    event?.preventDefault();

    const id = href.replace('#', '');
    const section = document.getElementById(id);

    if (!section) {
      this.closeMenu();
      return;
    }

    const header = document.querySelector<HTMLElement>('.header');
    const headerHeight = header?.offsetHeight ?? 78;

    const target =
      id === 'hero'
        ? section
        : section.querySelector<HTMLElement>(
            '.section__header, .section__heading, .section-title, h2, h1'
          ) ?? section;

    const extraGap = id === 'hero' ? 0 : 18;

    const top =
      id === 'hero'
        ? 0
        : window.scrollY + target.getBoundingClientRect().top - headerHeight - extraGap;

    window.history.pushState(null, '', href);
    window.scrollTo({
      top: Math.max(0, top),
      behavior: 'smooth',
    });

    this.closeMenu();
  }

"""

# Substitui o método goToAnchor atual, preservando toggleMenu abaixo dele
ts, count = re.subn(
    r"  goToAnchor\(href:[\s\S]*?\n  toggleMenu\(\): void \{",
    new_method + "  toggleMenu(): void {",
    ts,
    count=1
)

if count == 0:
    raise SystemExit("Não encontrei o método goToAnchor para substituir.")

# Remove patches antigos de scroll-margin duplicados, se existirem
scss = re.sub(r"/\* PATCH MENU ANCHORS[\s\S]*?(?=/\*|$)", "", scss)
scss = re.sub(r"/\* PATCH MENU ANCHORS FINAL[\s\S]*?(?=/\*|$)", "", scss)
scss = re.sub(r"/\* PATCH MENU LINKS EXISTENTES[\s\S]*?(?=/\*|$)", "", scss)
scss = re.sub(r"/\* PATCH DEFINITIVO — MENU / ANCHORS[\s\S]*?(?=/\*|$)", "", scss)

css_patch = """

/* PATCH FINAL — POSIÇÃO DO SCROLL DO MENU */
html {
  scroll-behavior: smooth;
  scroll-padding-top: 92px;
}

#hero,
#ceos,
#cafes,
#produtos,
#cardapio-digital,
#cafeteria,
#diferenciais,
#contato {
  scroll-margin-top: 92px;
}
"""

if "PATCH FINAL — POSIÇÃO DO SCROLL DO MENU" not in scss:
    scss += css_patch

ts_path.write_text(ts, encoding="utf-8")
scss_path.write_text(scss, encoding="utf-8")

print("OK: scroll do menu ajustado para mirar no título interno da seção.")
