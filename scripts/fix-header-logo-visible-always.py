from pathlib import Path
import re

html_path = Path("src/app/home/home.html")
scss_path = Path("src/app/home/home.scss")

html = html_path.read_text(encoding="utf-8")
scss = scss_path.read_text(encoding="utf-8")

LOGO = "assets/designs/coffee-blue-design-03.png"

# Substitui SOMENTE a primeira logo do header por uma versão única e sempre visível.
new_logo = f'''<a class="logo logo--always-visible" href="#hero" (click)="goToAnchor('#hero', $event)" aria-label="Voltar ao início">
      <img
        class="logo__image logo__image--always-visible"
        src="{LOGO}"
        alt="Blue Coffee"
      />
    </a>'''

html = re.sub(
    r'<a class="logo[^"]*"[\s\S]*?</a>',
    new_logo,
    html,
    count=1
)

html_path.write_text(html, encoding="utf-8")

# Remove patches antigos de logo que estavam conflitando.
scss = re.sub(
    r"/\* PATCH FINAL — LOGOS HEADER E FOOTER \*/[\s\S]*?(?=/\* PATCH|$)",
    "",
    scss
)

scss = re.sub(
    r"/\* PATCH FINAL — LOGO DO HEADER COM MESMO TAMANHO NO HERO E NO SCROLL \*/[\s\S]*?(?=/\* PATCH|$)",
    "",
    scss
)

scss = re.sub(
    r"/\* PATCH DEFINITIVO — LOGO HEADER E FOOTER \*/[\s\S]*?(?=/\* PATCH|$)",
    "",
    scss
)

patch = r'''

/* PATCH DEFINITIVO — LOGO DO HEADER SEMPRE VISÍVEL */
.header .logo.logo--always-visible,
.header.header--scrolled .logo.logo--always-visible,
.logo.logo--always-visible {
  width: 150px !important;
  min-width: 150px !important;
  height: 78px !important;
  flex: 0 0 150px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  position: relative !important;
  overflow: visible !important;
  padding: 0 !important;
  margin: 0 !important;
  border-radius: 0 !important;
  background: transparent !important;
  opacity: 1 !important;
  visibility: visible !important;
  z-index: 20 !important;
}

.header .logo__image.logo__image--always-visible,
.header.header--scrolled .logo__image.logo__image--always-visible,
.logo__image.logo__image--always-visible {
  position: static !important;
  display: block !important;
  width: auto !important;
  height: 66px !important;
  max-height: 66px !important;
  max-width: 150px !important;
  object-fit: contain !important;
  transform: none !important;
  opacity: 1 !important;
  visibility: visible !important;
  filter: none !important;
}

/* Evita que regras antigas escondam a logo */
.header .logo__image--dark,
.header .logo__image--light {
  opacity: 1;
  visibility: visible;
}

@media (max-width: 760px) {
  .header .logo.logo--always-visible,
  .header.header--scrolled .logo.logo--always-visible,
  .logo.logo--always-visible {
    width: 118px !important;
    min-width: 118px !important;
    height: 68px !important;
    flex-basis: 118px !important;
  }

  .header .logo__image.logo__image--always-visible,
  .header.header--scrolled .logo__image.logo__image--always-visible,
  .logo__image.logo__image--always-visible {
    height: 54px !important;
    max-height: 54px !important;
    max-width: 118px !important;
  }
}
'''

scss = scss.rstrip() + "\n" + patch + "\n"
scss_path.write_text(scss, encoding="utf-8")

print("OK: logo do header restaurada, grande e sempre visível.")
