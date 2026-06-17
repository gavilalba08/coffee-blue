from pathlib import Path
import re

html_path = Path("src/app/home/home.html")
scss_path = Path("src/app/home/home.scss")

html = html_path.read_text(encoding="utf-8")
scss = scss_path.read_text(encoding="utf-8")

# usa a logo branca no footer
white_logo = "assets/brand/header-logo-white.png"

# 1) troca apenas a imagem dentro do footer
footer_match = re.search(r"<footer[\s\S]*?</footer>", html)
if not footer_match:
    raise SystemExit("Footer não encontrado no home.html")

footer = footer_match.group(0)

# substitui a primeira imagem do footer por uma classe exclusiva
if 'class="footer-logo-blue-coffee"' in footer:
    footer = re.sub(
        r'<img[^>]*class="footer-logo-blue-coffee"[^>]*>',
        f'<img class="footer-logo-blue-coffee" src="{white_logo}" alt="Blue Coffee" loading="lazy" />',
        footer,
        count=1
    )
else:
    footer = re.sub(
        r'<img[^>]*alt="Blue Coffee"[^>]*>',
        f'<img class="footer-logo-blue-coffee" src="{white_logo}" alt="Blue Coffee" loading="lazy" />',
        footer,
        count=1
    )

html = html[:footer_match.start()] + footer + html[footer_match.end():]
html_path.write_text(html, encoding="utf-8")

# 2) remove patch antigo da logo do footer, se existir
scss = re.sub(
    r"/\* PATCH FOOTER LOGO EXCLUSIVA \*/[\s\S]*?(?=\n/\*|\Z)",
    "",
    scss
)

# 3) adiciona regra nova: mesmo tamanho visual do header
patch = r'''

/* PATCH FOOTER LOGO EXCLUSIVA */
.footer-logo-blue-coffee {
  display: block !important;
  width: auto !important;
  height: 64px !important;
  max-height: 64px !important;
  max-width: 180px !important;
  object-fit: contain !important;
  margin: 0 auto 1rem !important;
  opacity: 1 !important;
  visibility: visible !important;
}

@media (max-width: 760px) {
  .footer-logo-blue-coffee {
    height: 56px !important;
    max-height: 56px !important;
    max-width: 150px !important;
  }
}
'''

scss = scss.rstrip() + "\n" + patch + "\n"
scss_path.write_text(scss, encoding="utf-8")

print("OK: logo do footer ajustada para branca e com tamanho do header.")
