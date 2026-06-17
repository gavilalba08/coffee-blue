from pathlib import Path
import re

html_path = Path("src/app/home/home.html")
scss_path = Path("src/app/home/home.scss")

html = html_path.read_text(encoding="utf-8")
scss = scss_path.read_text(encoding="utf-8")

LOGO_WHITE = "assets/designs/coffee-blue-design-03.png"

# Corrige somente a imagem dentro do footer para uma classe exclusiva.
footer_match = re.search(r"<footer[\s\S]*?</footer>", html)

if not footer_match:
    raise SystemExit("Não encontrei <footer>...</footer> no home.html")

footer = footer_match.group(0)

footer = re.sub(
    r'<img[^>]*alt="Blue Coffee"[^>]*>',
    f'<img class="footer-logo-blue-coffee" src="{LOGO_WHITE}" alt="Blue Coffee" loading="lazy" />',
    footer,
    count=1
)

html = html[:footer_match.start()] + footer + html[footer_match.end():]
html_path.write_text(html, encoding="utf-8")

# Remove regras antigas que estavam deixando a logo do footer gigante.
scss = re.sub(
    r"\.footer__logo-img,\s*\n\.footer img\[alt=\"Blue Coffee\"\]\s*\{[\s\S]*?\}",
    "",
    scss
)

scss = re.sub(
    r"\.footer__logo-img,\s*\n\s*\.footer img\[alt=\"Blue Coffee\"\]\s*\{[\s\S]*?\}",
    "",
    scss
)

# Classe exclusiva do footer, mesmo tamanho visual da logo do header.
patch = r'''

/* PATCH FINAL — LOGO EXCLUSIVA DO FOOTER */
.footer-logo-blue-coffee {
  width: auto !important;
  height: 64px !important;
  max-height: 64px !important;
  max-width: 150px !important;
  object-fit: contain !important;
  display: block !important;
  margin: 0 auto 1rem !important;
  opacity: 1 !important;
  visibility: visible !important;
  transform: none !important;
  position: static !important;
}

@media (max-width: 760px) {
  .footer-logo-blue-coffee {
    height: 52px !important;
    max-height: 52px !important;
    max-width: 120px !important;
  }
}
'''

# Evita duplicar se rodar mais de uma vez.
scss = re.sub(
    r"/\* PATCH FINAL — LOGO EXCLUSIVA DO FOOTER \*/[\s\S]*$",
    "",
    scss
).rstrip()

scss += "\n" + patch + "\n"
scss_path.write_text(scss, encoding="utf-8")

print("OK: logo do footer isolada com classe própria.")
