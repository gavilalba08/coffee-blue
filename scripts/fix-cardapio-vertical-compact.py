from pathlib import Path
import re

path = Path("src/app/cardapio/cardapio.scss")
scss = path.read_text(encoding="utf-8")

# Remove o patch anterior que mexia em muita coisa, inclusive lateralmente.
scss = re.sub(
    r"/\* PATCH FINAL — CARDÁPIO DIGITAL MAIS COMPACTO \*/[\s\S]*?(?=/\* PATCH|$)",
    "",
    scss
)

scss = re.sub(
    r"/\* PATCH FINAL — CARDÁPIO DIGITAL COMPACTO VERTICAL \*/[\s\S]*?(?=/\* PATCH|$)",
    "",
    scss
)

patch = r'''

/* PATCH FINAL — CARDÁPIO DIGITAL COMPACTO VERTICAL */
/* Objetivo: reduzir altura e espaçamentos, sem alterar a largura/colunas principais */

.cp-header,
.cardapio-header,
.menu-header,
.digital-menu-header {
  min-height: 72px !important;
  padding-top: 0.7rem !important;
  padding-bottom: 0.7rem !important;
}

/* Bloco do título principal */
.cp-hero,
.cardapio-hero,
.menu-hero,
.hero-cardapio,
.digital-menu-hero,
.cardapio-intro,
.menu-intro {
  padding-top: 1.45rem !important;
  padding-bottom: 1.2rem !important;
  margin-bottom: 0 !important;
}

/* Selo BLUE COFFEE */
.cp-eyebrow,
.cardapio-eyebrow,
.menu-eyebrow,
.digital-menu-eyebrow,
.eyebrow {
  margin-bottom: 0.35rem !important;
  font-size: 0.72rem !important;
  letter-spacing: 0.22em !important;
}

/* Título Cardápio Digital */
.cp-title,
.cardapio-title,
.menu-title,
.digital-menu-title,
.cardapio-hero h1,
.menu-hero h1,
h1 {
  font-size: clamp(2.6rem, 4.3vw, 3.9rem) !important;
  line-height: 0.95 !important;
  margin-top: 0 !important;
  margin-bottom: 0.65rem !important;
}

/* Subtítulo abaixo do título */
.cp-subtitle,
.cardapio-subtitle,
.menu-subtitle,
.digital-menu-subtitle,
.cardapio-hero p,
.menu-hero p,
.cp-hero p {
  font-size: 0.98rem !important;
  line-height: 1.4 !important;
  max-width: 660px !important;
  margin-top: 0 !important;
  margin-bottom: 0 !important;
}

/* Área menu + categoria + resumo: sobe verticalmente */
.cp-menu-layout,
.cardapio-layout,
.menu-layout,
.digital-menu-layout,
.cardapio-content,
.menu-content {
  margin-top: 1rem !important;
  padding-top: 0 !important;
  align-items: flex-start !important;
}

/* Título da categoria */
.cp-category-title,
.cardapio-category-title,
.menu-category-title,
.category-title,
.cardapio-content h2,
.menu-content h2,
h2 {
  font-size: clamp(1.8rem, 3vw, 2.65rem) !important;
  line-height: 0.98 !important;
  margin-top: 0 !important;
  margin-bottom: 0.45rem !important;
}

/* Texto da categoria */
.cp-category-description,
.cardapio-category-description,
.menu-category-description,
.category-description {
  font-size: 0.95rem !important;
  line-height: 1.35 !important;
  margin-top: 0 !important;
  margin-bottom: 0.9rem !important;
}

/* Menu lateral e resumo: menos altura interna */
.cp-sidebar,
.cardapio-sidebar,
.menu-sidebar,
.category-sidebar,
.cp-order-summary,
.order-summary,
.cardapio-summary,
.menu-summary {
  padding-top: 1rem !important;
  padding-bottom: 1rem !important;
}

/* Itens do menu lateral */
.cp-sidebar button,
.cardapio-sidebar button,
.menu-sidebar button,
.category-sidebar button,
.cp-category-button,
.category-button {
  padding-top: 0.65rem !important;
  padding-bottom: 0.65rem !important;
}

/* Cards dos produtos: reduzir altura sem mudar grid/colunas */
.cp-product-card,
.product-card,
.menu-product-card,
.cardapio-product-card {
  padding-top: 0.8rem !important;
  padding-bottom: 0.85rem !important;
  min-height: auto !important;
}

/* Imagem dos produtos menor verticalmente */
.cp-product-card__img,
.cp-product-image img,
.cp-card__image img,
.product-image img,
.product-card img,
.menu-product-card img,
.cardapio-product-card img {
  height: clamp(115px, 13vw, 150px) !important;
  max-height: 150px !important;
  object-fit: contain !important;
}

/* Texto dos cards */
.cp-product-card h3,
.product-card h3,
.menu-product-card h3,
.cardapio-product-card h3 {
  font-size: 1.08rem !important;
  line-height: 1.05 !important;
  margin-top: 0.55rem !important;
  margin-bottom: 0.35rem !important;
}

.cp-product-card p,
.product-card p,
.menu-product-card p,
.cardapio-product-card p {
  font-size: 0.87rem !important;
  line-height: 1.32 !important;
  margin-bottom: 0.55rem !important;
}

/* Espaçamento do grid: somente vertical menor */
.cp-products-grid,
.cp-product-grid,
.cp-menu-grid,
.products-grid,
.menu-grid,
.cp-products {
  row-gap: 0.85rem !important;
}

/* Em notebook/desktop, encaixa melhor a primeira dobra */
@media (min-width: 1024px) and (min-height: 720px) {
  .cp-hero,
  .cardapio-hero,
  .menu-hero,
  .hero-cardapio,
  .digital-menu-hero,
  .cardapio-intro,
  .menu-intro {
    padding-top: 1.2rem !important;
    padding-bottom: 1rem !important;
  }

  .cp-menu-layout,
  .cardapio-layout,
  .menu-layout,
  .digital-menu-layout,
  .cardapio-content,
  .menu-content {
    margin-top: 0.8rem !important;
  }
}

/* Mobile continua confortável */
@media (max-width: 760px) {
  .cp-hero,
  .cardapio-hero,
  .menu-hero,
  .hero-cardapio,
  .digital-menu-hero,
  .cardapio-intro,
  .menu-intro {
    padding-top: 1.2rem !important;
    padding-bottom: 1rem !important;
  }

  .cp-title,
  .cardapio-title,
  .menu-title,
  .digital-menu-title,
  .cardapio-hero h1,
  .menu-hero h1,
  h1 {
    font-size: clamp(2.2rem, 10vw, 3rem) !important;
  }

  .cp-product-card__img,
  .cp-product-image img,
  .cp-card__image img,
  .product-image img,
  .product-card img,
  .menu-product-card img,
  .cardapio-product-card img {
    height: 130px !important;
    max-height: 130px !important;
  }
}
'''

scss = scss.rstrip() + "\n" + patch + "\n"
path.write_text(scss, encoding="utf-8")

print("OK: ajuste vertical aplicado no cardápio digital.")
