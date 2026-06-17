from pathlib import Path
import re

scss_path = Path("src/app/home/home.scss")
html_path = Path("src/app/home/home.html")

scss = scss_path.read_text(encoding="utf-8")
html = html_path.read_text(encoding="utf-8")

# Garante que o botão do menu tem aria-label correto.
html = re.sub(
    r'aria-label="Abrir menu de navegação"',
    'aria-label="Abrir ou fechar menu de navegação"',
    html
)

html_path.write_text(html, encoding="utf-8")

# Remove patch anterior se rodar de novo
scss = re.sub(
    r"/\* PATCH FINAL — HEADER MOBILE COFFEE BLUE \*/[\s\S]*?(?=/\* PATCH|$)",
    "",
    scss
).rstrip()

patch = r'''

/* PATCH FINAL — HEADER MOBILE COFFEE BLUE */
@media (max-width: 920px) {
  .header {
    min-height: 74px !important;
    padding: 0 !important;
    overflow: visible !important;
  }

  .header__inner {
    min-height: 74px !important;
    height: 74px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    gap: 0.75rem !important;
    position: relative !important;
    padding-inline: 1rem !important;
  }

  .header .logo,
  .header.header--scrolled .logo,
  .header__inner .logo {
    width: 112px !important;
    min-width: 112px !important;
    height: 64px !important;
    flex: 0 0 112px !important;
    z-index: 80 !important;
  }

  .header .logo__image,
  .header.header--scrolled .logo__image,
  .header__inner .logo__image {
    height: 50px !important;
    max-height: 50px !important;
    max-width: 112px !important;
  }

  .header__actions {
    display: flex !important;
    align-items: center !important;
    justify-content: flex-end !important;
    gap: 0.65rem !important;
    flex: 0 0 auto !important;
    z-index: 90 !important;
  }

  .nav__cta {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    min-height: 42px !important;
    padding: 0.65rem 0.95rem !important;
    border-radius: 999px !important;
    font-size: 0.78rem !important;
    white-space: nowrap !important;
    line-height: 1 !important;
  }

  .menu-toggle {
    display: inline-flex !important;
    width: 44px !important;
    height: 44px !important;
    min-width: 44px !important;
    border-radius: 999px !important;
    border: 1px solid rgba(227, 182, 75, 0.45) !important;
    background: rgba(2, 20, 44, 0.92) !important;
    align-items: center !important;
    justify-content: center !important;
    flex-direction: column !important;
    gap: 5px !important;
    padding: 0 !important;
    cursor: pointer !important;
    box-shadow: 0 14px 32px rgba(2, 20, 44, 0.24) !important;
  }

  .menu-toggle__bar {
    display: block !important;
    width: 18px !important;
    height: 2px !important;
    border-radius: 999px !important;
    background: #f7efe1 !important;
    transition: transform 180ms ease, opacity 180ms ease !important;
  }

  .menu-toggle--active .menu-toggle__bar:nth-child(1) {
    transform: translateY(7px) rotate(45deg) !important;
  }

  .menu-toggle--active .menu-toggle__bar:nth-child(2) {
    opacity: 0 !important;
  }

  .menu-toggle--active .menu-toggle__bar:nth-child(3) {
    transform: translateY(-7px) rotate(-45deg) !important;
  }

  .nav {
    position: absolute !important;
    left: 1rem !important;
    right: 1rem !important;
    top: calc(100% + 0.65rem) !important;
    z-index: 70 !important;
    border-radius: 24px !important;
    border: 1px solid rgba(227, 182, 75, 0.22) !important;
    background:
      radial-gradient(circle at top left, rgba(227, 182, 75, 0.14), transparent 38%),
      rgba(2, 20, 44, 0.98) !important;
    box-shadow: 0 26px 70px rgba(2, 20, 44, 0.38) !important;
    padding: 0.8rem !important;
    max-height: calc(100vh - 100px) !important;
    overflow-y: auto !important;
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
    display: grid !important;
    grid-template-columns: 1fr !important;
    gap: 0.25rem !important;
    padding: 0 !important;
    margin: 0 !important;
    list-style: none !important;
  }

  .nav__item {
    width: 100% !important;
  }

  .nav__link {
    width: 100% !important;
    min-height: 46px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    padding: 0.78rem 1rem !important;
    border-radius: 16px !important;
    color: #f7efe1 !important;
    font-size: 0.96rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em !important;
    text-decoration: none !important;
    border: 1px solid transparent !important;
    transition:
      background 160ms ease,
      border-color 160ms ease,
      color 160ms ease,
      transform 160ms ease !important;
  }

  .nav__link:hover,
  .nav__link:focus-visible {
    background: rgba(255, 255, 255, 0.08) !important;
    border-color: rgba(227, 182, 75, 0.25) !important;
    color: #e3b64b !important;
    transform: translateX(3px) !important;
  }
}

@media (max-width: 520px) {
  .header__inner {
    padding-inline: 0.75rem !important;
    gap: 0.45rem !important;
  }

  .header .logo,
  .header.header--scrolled .logo,
  .header__inner .logo {
    width: 98px !important;
    min-width: 98px !important;
    height: 60px !important;
    flex-basis: 98px !important;
  }

  .header .logo__image,
  .header.header--scrolled .logo__image,
  .header__inner .logo__image {
    height: 44px !important;
    max-height: 44px !important;
    max-width: 98px !important;
  }

  .nav__cta {
    min-height: 38px !important;
    padding: 0.58rem 0.75rem !important;
    font-size: 0.7rem !important;
    max-width: 132px !important;
  }

  .menu-toggle {
    width: 40px !important;
    height: 40px !important;
    min-width: 40px !important;
  }

  .nav {
    left: 0.75rem !important;
    right: 0.75rem !important;
    top: calc(100% + 0.5rem) !important;
    border-radius: 20px !important;
  }

  .nav__link {
    min-height: 44px !important;
    padding: 0.72rem 0.9rem !important;
    font-size: 0.92rem !important;
  }
}

@media (max-width: 380px) {
  .nav__cta {
    display: none !important;
  }

  .header .logo,
  .header.header--scrolled .logo,
  .header__inner .logo {
    width: 110px !important;
    min-width: 110px !important;
    flex-basis: 110px !important;
  }

  .header .logo__image,
  .header.header--scrolled .logo__image,
  .header__inner .logo__image {
    height: 48px !important;
    max-height: 48px !important;
    max-width: 110px !important;
  }
}
'''

scss += "\n" + patch + "\n"
scss_path.write_text(scss, encoding="utf-8")

print("OK: menu mobile do header ajustado.")
