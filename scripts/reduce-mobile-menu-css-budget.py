from pathlib import Path
import re

path = Path("src/app/home/home.scss")
scss = path.read_text(encoding="utf-8")

# Remove patches antigos grandes/duplicados do menu mobile.
markers = [
    "PATCH FINAL — HEADER MOBILE COFFEE BLUE",
    "PATCH FINAL — MENU MOBILE ABERTO MAIOR E FECHAMENTO",
]

for marker in markers:
    scss = re.sub(
        rf"/\* {re.escape(marker)} \*/[\s\S]*?(?=/\* PATCH|$)",
        "",
        scss
    )

# Remove patch compacto anterior se já existir.
scss = re.sub(
    r"/\* PATCH FINAL — MENU MOBILE COMPACTO \*/[\s\S]*?(?=/\* PATCH|$)",
    "",
    scss
).rstrip()

patch = r'''

/* PATCH FINAL — MENU MOBILE COMPACTO */
@media (max-width: 920px) {
  .header,
  .header__inner {
    overflow: visible !important;
  }

  .header__inner {
    min-height: 74px !important;
    height: 74px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    gap: .75rem !important;
    padding-inline: 1rem !important;
  }

  .header .logo,
  .header.header--scrolled .logo,
  .header__inner .logo {
    width: 112px !important;
    min-width: 112px !important;
    height: 64px !important;
    flex: 0 0 112px !important;
    z-index: 140 !important;
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
    gap: .65rem !important;
    z-index: 150 !important;
  }

  .nav__cta {
    min-height: 42px !important;
    padding: .65rem .95rem !important;
    border-radius: 999px !important;
    font-size: .78rem !important;
    white-space: nowrap !important;
  }

  .menu-toggle {
    display: inline-flex !important;
    width: 44px !important;
    height: 44px !important;
    min-width: 44px !important;
    border-radius: 999px !important;
    border: 1px solid rgba(227, 182, 75, .45) !important;
    background: rgba(2, 20, 44, .92) !important;
    align-items: center !important;
    justify-content: center !important;
    flex-direction: column !important;
    gap: 5px !important;
    padding: 0 !important;
    z-index: 160 !important;
  }

  .menu-toggle__bar {
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
    top: calc(100% + .75rem) !important;
    z-index: 130 !important;
    height: auto !important;
    max-height: calc(100vh - 130px) !important;
    overflow-y: auto !important;
    padding: 1rem !important;
    border-radius: 24px !important;
    border: 1px solid rgba(227, 182, 75, .34) !important;
    background: linear-gradient(145deg, rgba(2, 20, 44, .99), rgba(8, 33, 59, .99)) !important;
    box-shadow: 0 28px 80px rgba(2, 20, 44, .48) !important;
    opacity: 0 !important;
    visibility: hidden !important;
    pointer-events: none !important;
    transform: translateY(-10px) scale(.98) !important;
    transition: opacity 180ms ease, visibility 180ms ease, transform 180ms ease !important;
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
    gap: .45rem !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
  }

  .nav__item {
    width: 100% !important;
  }

  .nav__link {
    width: 100% !important;
    min-height: 52px !important;
    display: flex !important;
    align-items: center !important;
    padding: .9rem 1.05rem !important;
    border-radius: 18px !important;
    color: #f7efe1 !important;
    background: rgba(255, 255, 255, .045) !important;
    border: 1px solid rgba(255, 255, 255, .06) !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    text-decoration: none !important;
  }

  .nav__link:hover,
  .nav__link:focus-visible {
    color: #e3b64b !important;
    background: rgba(227, 182, 75, .12) !important;
    border-color: rgba(227, 182, 75, .32) !important;
  }
}

@media (max-width: 520px) {
  .header__inner {
    padding-inline: .75rem !important;
    gap: .45rem !important;
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
    padding: .58rem .75rem !important;
    font-size: .7rem !important;
    max-width: 132px !important;
  }

  .menu-toggle {
    width: 40px !important;
    height: 40px !important;
    min-width: 40px !important;
  }

  .nav {
    left: .75rem !important;
    right: .75rem !important;
    top: calc(100% + .6rem) !important;
    padding: .85rem !important;
    border-radius: 20px !important;
  }

  .nav__link {
    min-height: 50px !important;
    padding: .82rem .95rem !important;
    font-size: .96rem !important;
  }
}
'''

scss += "\n" + patch + "\n"
path.write_text(scss, encoding="utf-8")

print("OK: CSS mobile reduzido e patches duplicados removidos.")
