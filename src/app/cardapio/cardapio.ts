import { ChangeDetectionStrategy, Component, computed, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

type CategoryId = 'cafes' | 'edicoes' | 'bebidas' | 'produtos';

interface Category {
  readonly id: CategoryId;
  readonly label: string;
  readonly subtitle: string;
}

interface Product {
  readonly id: string;
  readonly category: CategoryId;
  readonly name: string;
  readonly description: string;
  readonly price: number;
  readonly image: string;
}

@Component({
  selector: 'app-cardapio',
  imports: [RouterLink],
  templateUrl: './cardapio.html',
  styleUrl: './cardapio.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Cardapio {
  readonly activeCategory = signal<CategoryId>('cafes');
  readonly quantities = signal<Record<string, number>>({});

  readonly categories: readonly Category[] = [
    {
      id: 'cafes',
      label: 'Cafés',
      subtitle: 'Blends clássicos da Blue Coffee',
    },
    {
      id: 'edicoes',
      label: 'Edições Especiais',
      subtitle: 'Sabores temáticos e coleções limitadas',
    },
    {
      id: 'bebidas',
      label: 'Bebidas e Doces',
      subtitle: 'Prontos para consumir e acompanhar',
    },
    {
      id: 'produtos',
      label: 'Produtos',
      subtitle: 'Kits, cápsulas, drip e experiências',
    },
  ];

  readonly products: readonly Product[] = [
    {
      id: 'blue-light',
      category: 'cafes',
      name: 'Blue Light',
      description: 'Blend suave, delicado e aromático para o dia a dia.',
      price: 34.9,
      image: 'assets/produtos-blue-coffee-fotos/cafes-classicos/18-blue-light.png',
    },
    {
      id: 'blue-classic',
      category: 'cafes',
      name: 'Blue Classic',
      description: 'Café clássico, equilibrado e marcante.',
      price: 36.9,
      image: 'assets/produtos-blue-coffee-fotos/cafes-classicos/29-blue-classic.png',
    },
    {
      id: 'blue-gourmet',
      category: 'cafes',
      name: 'Blue Gourmet',
      description: 'Grãos especiais com sabor sofisticado.',
      price: 39.9,
      image: 'assets/produtos-blue-coffee-fotos/cafes-classicos/20-blue-gourmet.png',
    },
    {
      id: 'blue-intense',
      category: 'cafes',
      name: 'Blue Intense',
      description: 'Torra intensa, corpo marcante e final persistente.',
      price: 36.9,
      image: 'assets/produtos-blue-coffee-fotos/cafes-classicos/06-blue-intense.png',
    },

    {
      id: 'festa-junina',
      category: 'edicoes',
      name: 'Festa Junina',
      description: 'Notas aconchegantes inspiradas nas festas juninas.',
      price: 38.9,
      image: 'assets/produtos-blue-coffee-fotos/cafes-edicoes/16-festa-junina.png',
    },
    {
      id: 'copa-do-mundo',
      category: 'edicoes',
      name: 'Copa do Mundo',
      description: 'Edição comemorativa para torcer com sabor.',
      price: 38.9,
      image: 'assets/produtos-blue-coffee-fotos/cafes-edicoes/05-copa-do-mundo.png',
    },
    {
      id: 'dia-dos-namorados',
      category: 'edicoes',
      name: 'Dia dos Namorados',
      description: 'Blend romântico para momentos especiais.',
      price: 38.9,
      image: 'assets/produtos-blue-coffee-fotos/cafes-edicoes/12-dia-dos-namorados.png',
    },
    {
      id: 'natal',
      category: 'edicoes',
      name: 'Natal',
      description: 'Aroma acolhedor e toque de celebração.',
      price: 38.9,
      image: 'assets/produtos-blue-coffee-fotos/cafes-edicoes/26-natal.png',
    },

    {
      id: 'blue-oat-latte',
      category: 'bebidas',
      name: 'Blue Oat Latte',
      description: 'Latte com aveia, leve e cremoso.',
      price: 13.9,
      image: 'assets/produtos-blue-coffee-fotos/bebidas-prontas/02-blue-oat-latte.png',
    },
    {
      id: 'blue-cold-brew-zero',
      category: 'bebidas',
      name: 'Blue Cold Brew Zero',
      description: 'Cold brew refrescante, sem açúcar.',
      price: 14.9,
      image: 'assets/produtos-blue-coffee-fotos/bebidas-prontas/03-blue-cold-brew-zero.png',
    },
    {
      id: 'blue-mocha',
      category: 'bebidas',
      name: 'Blue Mocha',
      description: 'Café com chocolate em versão cremosa.',
      price: 15.9,
      image: 'assets/produtos-blue-coffee-fotos/bebidas-prontas/08-blue-mocha.png',
    },
    {
      id: 'blue-coconut-latte',
      category: 'bebidas',
      name: 'Blue Coconut Latte',
      description: 'Latte com toque tropical de coco.',
      price: 15.9,
      image: 'assets/produtos-blue-coffee-fotos/bebidas-prontas/11-blue-coconut-latte.png',
    },
    {
      id: 'blue-cappuccino-ice',
      category: 'bebidas',
      name: 'Blue Cappuccino Ice',
      description: 'Cappuccino gelado pronto para beber.',
      price: 14.9,
      image: 'assets/produtos-blue-coffee-fotos/bebidas-prontas/14-blue-cappuccino-ice.png',
    },
    {
      id: 'blue-latte',
      category: 'bebidas',
      name: 'Blue Latte',
      description: 'Latte clássico, equilibrado e suave.',
      price: 13.9,
      image: 'assets/produtos-blue-coffee-fotos/bebidas-prontas/17-blue-latte.png',
    },
    {
      id: 'blue-vanilla-latte',
      category: 'bebidas',
      name: 'Blue Vanilla Latte',
      description: 'Latte com aroma delicado de baunilha.',
      price: 15.9,
      image: 'assets/produtos-blue-coffee-fotos/bebidas-prontas/21-blue-vanilla-latte.png',
    },
    {
      id: 'blue-hazelnut',
      category: 'bebidas',
      name: 'Blue Hazelnut',
      description: 'Café com notas de avelã.',
      price: 15.9,
      image: 'assets/produtos-blue-coffee-fotos/bebidas-prontas/23-blue-hazelnut.png',
    },
    {
      id: 'blue-double-expresso',
      category: 'bebidas',
      name: 'Blue Double Expresso',
      description: 'Dose dupla de intensidade.',
      price: 12.9,
      image: 'assets/produtos-blue-coffee-fotos/bebidas-prontas/25-blue-double-expresso.png',
    },
    {
      id: 'blue-caramel-latte',
      category: 'bebidas',
      name: 'Blue Caramel Latte',
      description: 'Latte com toque de caramelo.',
      price: 15.9,
      image: 'assets/produtos-blue-coffee-fotos/bebidas-prontas/27-blue-caramel-latte.png',
    },
    {
      id: 'blue-cookies',
      category: 'bebidas',
      name: 'Blue Cookies',
      description: 'Cookies crocantes para acompanhar seu café.',
      price: 9.9,
      image: 'assets/produtos-blue-coffee-fotos/acompanhamentos/13-blue-cookies.png',
    },

    {
      id: 'blue-cacao',
      category: 'produtos',
      name: 'Blue Cacao',
      description: 'Produto especial com notas intensas de cacau.',
      price: 29.9,
      image: 'assets/produtos-blue-coffee-fotos/cafes-especiais/01-blue-cacao.png',
    },
    {
      id: 'blue-reserve',
      category: 'produtos',
      name: 'Blue Reserve',
      description: 'Seleção premium para uma experiência exclusiva.',
      price: 44.9,
      image: 'assets/produtos-blue-coffee-fotos/cafes-especiais/04-blue-reserve.png',
    },
    {
      id: 'blue-capsules',
      category: 'produtos',
      name: 'Blue Capsules',
      description: 'Cápsulas práticas para o café perfeito.',
      price: 32.9,
      image: 'assets/produtos-blue-coffee-fotos/capsulas-e-drip/07-blue-capsules.png',
    },
    {
      id: 'blue-drip',
      category: 'produtos',
      name: 'Blue Drip',
      description: 'Café coado na hora, onde você estiver.',
      price: 24.9,
      image: 'assets/produtos-blue-coffee-fotos/capsulas-e-drip/10-blue-drip.png',
    },
    {
      id: 'blue-cold-brew',
      category: 'produtos',
      name: 'Blue Cold Brew',
      description: 'Café extraído a frio, refrescante e aromático.',
      price: 18.9,
      image: 'assets/produtos-blue-coffee-fotos/cold-brew/24-blue-cold-brew.png',
    },
    {
      id: 'blue-ritual-kit',
      category: 'produtos',
      name: 'Blue Ritual Kit',
      description: 'Kit completo para transformar o café em ritual.',
      price: 89.9,
      image: 'assets/produtos-blue-coffee-fotos/kits/09-blue-ritual-kit.png',
    },
    {
      id: 'blue-gift-box',
      category: 'produtos',
      name: 'Blue Gift Box',
      description: 'Caixa presente elegante para amantes de café.',
      price: 99.9,
      image: 'assets/produtos-blue-coffee-fotos/kits/22-blue-gift-box.png',
    },
    {
      id: 'blue-selection',
      category: 'produtos',
      name: 'Blue Selection',
      description: 'Seleção especial com os favoritos da marca.',
      price: 119.9,
      image: 'assets/produtos-blue-coffee-fotos/kits/28-blue-selection.png',
    },
  ];

  readonly activeCategoryData = computed(() => {
    return this.categories.find((category) => category.id === this.activeCategory()) ?? this.categories[0];
  });

  readonly filteredProducts = computed(() => {
    return this.products.filter((product) => product.category === this.activeCategory());
  });

  readonly cartItems = computed(() => {
    const quantities = this.quantities();

    return this.products
      .map((product) => ({
        product,
        quantity: quantities[product.id] ?? 0,
      }))
      .filter((item) => item.quantity > 0);
  });

  readonly cartTotal = computed(() => {
    return this.cartItems().reduce((total, item) => total + item.product.price * item.quantity, 0);
  });

  setCategory(category: CategoryId): void {
    this.activeCategory.set(category);
  }

  quantityOf(productId: string): number {
    return this.quantities()[productId] ?? 0;
  }

  increase(productId: string): void {
    this.quantities.update((current) => ({
      ...current,
      [productId]: (current[productId] ?? 0) + 1,
    }));
  }

  decrease(productId: string): void {
    this.quantities.update((current) => {
      const nextQuantity = Math.max((current[productId] ?? 0) - 1, 0);
      const next = { ...current };

      if (nextQuantity === 0) {
        delete next[productId];
      } else {
        next[productId] = nextQuantity;
      }

      return next;
    });
  }

  clearCart(): void {
    this.quantities.set({});
  }

  formatPrice(value: number): string {
    return value.toLocaleString('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    });
  }
}
