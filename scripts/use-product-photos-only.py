from pathlib import Path
import re

ROOT = Path(".")
SRC_DIR = ROOT / "src"

files = [
    p for p in SRC_DIR.rglob("*")
    if p.suffix in {".ts", ".html", ".scss", ".css"}
]

# Mapeia imagens antigas/fatiadas/mockups para as novas imagens limpas.
mapping = {
    # Antigos cafés clássicos
    "assets/products-packshots/cafes/classicos/suave-equilibrado.png": "assets/produtos-blue-coffee-fotos/cafes-classicos/18-blue-light.png",
    "assets/products-packshots/cafes/classicos/forte-intenso.png": "assets/produtos-blue-coffee-fotos/cafes-classicos/06-blue-intense.png",
    "assets/products-packshots/cafes/classicos/gourmet.png": "assets/produtos-blue-coffee-fotos/cafes-classicos/20-blue-gourmet.png",
    "assets/products-packshots/cafes/classicos/extra-especial.png": "assets/produtos-blue-coffee-fotos/cafes-classicos/29-blue-classic.png",

    "assets/products-transparent/cafes/classicos/suave-equilibrado.png": "assets/produtos-blue-coffee-fotos/cafes-classicos/18-blue-light.png",
    "assets/products-transparent/cafes/classicos/forte-intenso.png": "assets/produtos-blue-coffee-fotos/cafes-classicos/06-blue-intense.png",
    "assets/products-transparent/cafes/classicos/gourmet.png": "assets/produtos-blue-coffee-fotos/cafes-classicos/20-blue-gourmet.png",
    "assets/products-transparent/cafes/classicos/extra-especial.png": "assets/produtos-blue-coffee-fotos/cafes-classicos/29-blue-classic.png",

    # Antigas edições
    "assets/products-packshots/cafes/edicoes/festa-junina.png": "assets/produtos-blue-coffee-fotos/cafes-edicoes/16-festa-junina.png",
    "assets/products-packshots/cafes/edicoes/copa-do-mundo.png": "assets/produtos-blue-coffee-fotos/cafes-edicoes/05-copa-do-mundo.png",
    "assets/products-packshots/cafes/edicoes/dia-dos-namorados.png": "assets/produtos-blue-coffee-fotos/cafes-edicoes/12-dia-dos-namorados.png",
    "assets/products-packshots/cafes/edicoes/natal.png": "assets/produtos-blue-coffee-fotos/cafes-edicoes/26-natal.png",

    "assets/products-transparent/cafes/edicoes/festa-junina.png": "assets/produtos-blue-coffee-fotos/cafes-edicoes/16-festa-junina.png",
    "assets/products-transparent/cafes/edicoes/copa-do-mundo.png": "assets/produtos-blue-coffee-fotos/cafes-edicoes/05-copa-do-mundo.png",
    "assets/products-transparent/cafes/edicoes/dia-dos-namorados.png": "assets/produtos-blue-coffee-fotos/cafes-edicoes/12-dia-dos-namorados.png",
    "assets/products-transparent/cafes/edicoes/natal.png": "assets/produtos-blue-coffee-fotos/cafes-edicoes/26-natal.png",

    # Antigos outros produtos
    "assets/products-packshots/outros/cappuccino-classico.png": "assets/produtos-blue-coffee-fotos/bebidas-prontas/14-blue-cappuccino-ice.png",
    "assets/products-packshots/outros/cappuccino-chocolate.png": "assets/produtos-blue-coffee-fotos/bebidas-prontas/08-blue-mocha.png",
    "assets/products-packshots/outros/chocolate-premium.png": "assets/produtos-blue-coffee-fotos/cafes-especiais/01-blue-cacao.png",
    "assets/products-packshots/outros/filtros-de-papel.png": "assets/produtos-blue-coffee-fotos/capsulas-e-drip/07-blue-capsules.png",
    "assets/products-packshots/outros/caneca-exclusiva.png": "assets/produtos-blue-coffee-fotos/imagens-apoio/15-copo-blue-coffee-janela.png",
    "assets/products-packshots/outros/brownie-artesanal.png": "assets/produtos-blue-coffee-fotos/acompanhamentos/13-blue-cookies.png",
    "assets/products-packshots/outros/cookies-artesanais.png": "assets/produtos-blue-coffee-fotos/acompanhamentos/13-blue-cookies.png",
    "assets/products-packshots/outros/drip-coffee-pratico.png": "assets/produtos-blue-coffee-fotos/capsulas-e-drip/10-blue-drip.png",

    "assets/products-transparent/outros/cappuccino-classico.png": "assets/produtos-blue-coffee-fotos/bebidas-prontas/14-blue-cappuccino-ice.png",
    "assets/products-transparent/outros/cappuccino-chocolate.png": "assets/produtos-blue-coffee-fotos/bebidas-prontas/08-blue-mocha.png",
    "assets/products-transparent/outros/chocolate-premium.png": "assets/produtos-blue-coffee-fotos/cafes-especiais/01-blue-cacao.png",
    "assets/products-transparent/outros/filtros-de-papel.png": "assets/produtos-blue-coffee-fotos/capsulas-e-drip/07-blue-capsules.png",
    "assets/products-transparent/outros/caneca-exclusiva.png": "assets/produtos-blue-coffee-fotos/imagens-apoio/15-copo-blue-coffee-janela.png",
    "assets/products-transparent/outros/brownie-artesanal.png": "assets/produtos-blue-coffee-fotos/acompanhamentos/13-blue-cookies.png",
    "assets/products-transparent/outros/cookies-artesanais.png": "assets/produtos-blue-coffee-fotos/acompanhamentos/13-blue-cookies.png",
    "assets/products-transparent/outros/drip-coffee-pratico.png": "assets/produtos-blue-coffee-fotos/capsulas-e-drip/10-blue-drip.png",
}

changed_files = []

for path in files:
    text = path.read_text(encoding="utf-8")
    original = text

    for old, new in mapping.items():
        text = text.replace(old, new)

    # Troca genérica dos mockups novos .jpeg para fotos limpas .png
    text = re.sub(
        r"assets/produtos-blue-coffee/([^'\"\s)]+)\.(?:jpeg|jpg)",
        r"assets/produtos-blue-coffee-fotos/\1.png",
        text,
    )

    # Troca cardapio-clean, caso ainda esteja em uso
    text = re.sub(
        r"assets/cardapio-clean/([^'\"\s)]+)\.png",
        r"assets/produtos-blue-coffee-fotos/\1.png",
        text,
    )

    if text != original:
        path.write_text(text, encoding="utf-8")
        changed_files.append(str(path))

print("Arquivos atualizados:")
for file in changed_files:
    print("-", file)
