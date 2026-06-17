import { NgOptimizedImage } from '@angular/common';
import { ChangeDetectionStrategy, Component, ElementRef, HostListener, afterNextRender, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

interface NavLink {
  readonly label: string;
  readonly href?: string;
  readonly routerLink?: string;
}

interface ClassicCoffee {
  readonly name: string;
  readonly description: string;
  readonly price: string;
  readonly image: string;
  readonly intensity: number;
}

interface SpecialCoffee {
  readonly name: string;
  readonly description: string;
  readonly price: string;
  readonly image: string;
  readonly badge: string;
}

interface Edition {
  readonly name: string;
  readonly description: string;
  readonly image: string;
  readonly badge: string;
}

interface Product {
  readonly name: string;
  readonly description: string;
  readonly price: string;
  readonly image: string;
}

interface DifferentialItem {
  readonly icon: string;
  readonly title: string;
  readonly description: string;
}

interface ContactLink {
  readonly icon: string;
  readonly label: string;
  readonly value: string;
  readonly href: string;
}

interface CardapioStep {
  readonly number: number;
  readonly title: string;
  readonly description: string;
}

interface CeoMember {
  readonly name: string;
  readonly nickname: string;
  readonly role: string;
  readonly description: string;
  readonly temperament: string;
  readonly image: string;
  readonly previewPosition: string;
  readonly detailImageSide: 'left' | 'right';
}

@Component({
  selector: 'app-home',
  imports: [NgOptimizedImage, RouterLink],
  templateUrl: './home.html',
  styleUrl: './home.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: {
    '(window:scroll)': 'onWindowScroll()',
  },
})
export class Home {
  private readonly elementRef: ElementRef<HTMLElement> = inject(ElementRef);

  readonly isMenuOpen = signal(false);
  readonly isScrolled = signal(false);
  readonly isHeroVideoMuted = signal(true);

  readonly navLinks: readonly NavLink[] = [
    { label: 'Início', href: '#hero' },
    { label: 'CEOs', href: '#ceos' },
    { label: 'Nossos Cafés', href: '#cafes' },
    { label: 'Bebidas Prontas', href: '#produtos' },
    { label: 'Cardápio Digital', href: '#cardapio-digital' },
    { label: 'Cafeteria', href: '#cafeteria' },
    { label: 'Diferenciais', href: '#diferenciais' },
    { label: 'Contato', href: '#contato' },
  ];

  readonly intensityLevels: readonly number[] = [1, 2, 3];

  readonly classicCoffees: readonly ClassicCoffee[] = [
    {
      name: 'Blue Light',
      description:
        'Blend suave com acidez delicada e notas florais. Perfeito para começar o dia com leveza e aroma envolvente.',
      price: 'R$ 34,90',
      image: 'assets/produtos-blue-coffee-fotos/cafes-classicos/18-blue-light.png',
      intensity: 1,
    },
    {
      name: 'Blue Classic',
      description:
        'O blend clássico da Blue Coffee, encorpado e aromático com finalização persistente e caráter marcante.',
      price: 'R$ 36,90',
      image: 'assets/produtos-blue-coffee-fotos/cafes-classicos/29-blue-classic.png',
      intensity: 2,
    },
    {
      name: 'Blue Gourmet',
      description:
        'Seleção de grãos especiais com complexidade e equilíbrio excepcionais. Notas aromáticas inconfundíveis.',
      price: 'R$ 42,90',
      image: 'assets/produtos-blue-coffee-fotos/cafes-classicos/20-blue-gourmet.png',
      intensity: 2,
    },
    {
      name: 'Blue Intense',
      description:
        'Torra escura intensa para os apreciadores de um café potente e marcante do primeiro ao último gole.',
      price: 'R$ 46,90',
      image: 'assets/produtos-blue-coffee-fotos/cafes-classicos/06-blue-intense.png',
      intensity: 3,
    },
  ];

  readonly specialCoffees: readonly SpecialCoffee[] = [
    {
      name: 'Blue Cacao',
      description:
        'Blend especial com notas de cacau tropical e toque adocicado. Uma experiência sensorial única que combina o melhor do café com o exótico do cacau.',
      price: 'R$ 52,90',
      image: 'assets/produtos-blue-coffee-fotos/cafes-especiais/01-blue-cacao.png',
      badge: 'Café Especial',
    },
    {
      name: 'Blue Reserve',
      description:
        'Nossa mais alta seleção. Grãos de origem controlada com perfil aromático exclusivo e raro, para os paladares mais exigentes.',
      price: 'R$ 64,90',
      image: 'assets/produtos-blue-coffee-fotos/cafes-especiais/04-blue-reserve.png',
      badge: 'Reserva Premium',
    },
  ];

  readonly specialEditions: readonly Edition[] = [
    {
      name: 'Copa do Mundo',
      description:
        'Embalagem comemorativa para torcer com sabor, unindo a paixão pelo futebol ao melhor café.',
      image: 'assets/produtos-blue-coffee-fotos/cafes-edicoes/05-copa-do-mundo.png',
      badge: 'Edição limitada',
    },
    {
      name: 'Dia dos Namorados',
      description:
        'Blend exclusivo em embalagem romântica, com notas adocicadas perfeitas para compartilhar.',
      image: 'assets/produtos-blue-coffee-fotos/cafes-edicoes/12-dia-dos-namorados.png',
      badge: 'Edição limitada',
    },
    {
      name: 'Festa Junina',
      description:
        'Blend especial com toque de canela e rapadura, inspirado nas tradições e fogueiras de junho.',
      image: 'assets/produtos-blue-coffee-fotos/cafes-edicoes/16-festa-junina.png',
      badge: 'Edição limitada',
    },
    {
      name: 'Natal',
      description:
        'Blend aromático natalino em embalagem dourada, perfeito para presentear e celebrar.',
      image: 'assets/produtos-blue-coffee-fotos/cafes-edicoes/26-natal.png',
      badge: 'Edição limitada',
    },
  ];

  readonly readyDrinks: readonly Product[] = [
    {
      name: 'Blue Oat Latte',
      description: 'Espresso cremoso com leite de aveia. Suave e levemente adocicado.',
      price: 'R$ 18,90',
      image: 'assets/produtos-blue-coffee-fotos/bebidas-prontas/02-blue-oat-latte.png',
    },
    {
      name: 'Blue Cold Brew Zero',
      description: 'Cold brew zero açúcar com perfil limpo e refrescante.',
      price: 'R$ 16,90',
      image: 'assets/produtos-blue-coffee-fotos/bebidas-prontas/03-blue-cold-brew-zero.png',
    },
    {
      name: 'Blue Mocha',
      description: 'Espresso com chocolate belga e leite vaporizado cremoso.',
      price: 'R$ 19,90',
      image: 'assets/produtos-blue-coffee-fotos/bebidas-prontas/08-blue-mocha.png',
    },
    {
      name: 'Blue Coconut Latte',
      description: 'Latte tropical com leite de coco e toque exótico irresistível.',
      price: 'R$ 18,90',
      image: 'assets/produtos-blue-coffee-fotos/bebidas-prontas/11-blue-coconut-latte.png',
    },
    {
      name: 'Blue Cappuccino Ice',
      description: 'Cappuccino gelado com espuma densa e refrescante.',
      price: 'R$ 17,90',
      image: 'assets/produtos-blue-coffee-fotos/bebidas-prontas/14-blue-cappuccino-ice.png',
    },
    {
      name: 'Blue Latte',
      description: 'O clássico latte Blue Coffee, equilibrado e cremoso.',
      price: 'R$ 16,90',
      image: 'assets/produtos-blue-coffee-fotos/bebidas-prontas/17-blue-latte.png',
    },
    {
      name: 'Blue Vanilla Latte',
      description: 'Latte com extrato natural de baunilha e espuma sedosa.',
      price: 'R$ 18,90',
      image: 'assets/produtos-blue-coffee-fotos/bebidas-prontas/21-blue-vanilla-latte.png',
    },
    {
      name: 'Blue Hazelnut',
      description: 'Espresso com avelã torrada e leite cremoso irresistível.',
      price: 'R$ 19,90',
      image: 'assets/produtos-blue-coffee-fotos/bebidas-prontas/23-blue-hazelnut.png',
    },
    {
      name: 'Blue Double Espresso',
      description: 'Duplo shot intenso para quem não abre mão da cafeína.',
      price: 'R$ 14,90',
      image: 'assets/produtos-blue-coffee-fotos/bebidas-prontas/25-blue-double-expresso.png',
    },
    {
      name: 'Blue Caramel Latte',
      description: 'Latte com caramelo artesanal, doce e sofisticado.',
      price: 'R$ 19,90',
      image: 'assets/produtos-blue-coffee-fotos/bebidas-prontas/27-blue-caramel-latte.png',
    },
  ];

  readonly capsuleDripProducts: readonly Product[] = [
    {
      name: 'Blue Capsules',
      description: 'Cápsulas compatíveis com máquinas Nespresso®. Praticidade e intensidade em casa.',
      price: 'R$ 29,90',
      image: 'assets/produtos-blue-coffee-fotos/capsulas-e-drip/07-blue-capsules.png',
    },
    {
      name: 'Blue Drip',
      description: 'Café coado perfeito em qualquer lugar, sem equipamento especial. 10 unidades.',
      price: 'R$ 22,90',
      image: 'assets/produtos-blue-coffee-fotos/capsulas-e-drip/10-blue-drip.png',
    },
    {
      name: 'Blue Cold Brew',
      description: 'Cold brew artesanal em garrafa premium. Refrescante, encorpado e pronto para beber.',
      price: 'R$ 24,90',
      image: 'assets/produtos-blue-coffee-fotos/cold-brew/24-blue-cold-brew.png',
    },
  ];

  readonly kitsProducts: readonly Product[] = [
    {
      name: 'Blue Ritual Kit',
      description:
        'Kit completo para o ritual do café: blend selecionado, drip e guia de preparo artesanal.',
      price: 'R$ 89,90',
      image: 'assets/produtos-blue-coffee-fotos/kits/09-blue-ritual-kit.png',
    },
    {
      name: 'Blue Gift Box',
      description: 'Caixa presente elegante com curadoria de produtos Blue Coffee. Ideal para presentear.',
      price: 'R$ 129,90',
      image: 'assets/produtos-blue-coffee-fotos/kits/22-blue-gift-box.png',
    },
    {
      name: 'Blue Selection',
      description:
        'Seleção premium com os melhores produtos da linha Blue Coffee em embalagem exclusiva.',
      price: 'R$ 159,90',
      image: 'assets/produtos-blue-coffee-fotos/kits/28-blue-selection.png',
    },
    {
      name: 'Blue Cookies',
      description: 'Cookies artesanais crocantes com gotas de chocolate. 6 unidades por embalagem.',
      price: 'R$ 18,90',
      image: 'assets/produtos-blue-coffee-fotos/acompanhamentos/13-blue-cookies.png',
    },
  ];

  readonly otherProducts = [
    ...this.readyDrinks,
    ...this.capsuleDripProducts,
    ...this.kitsProducts,
  ];

  readonly menuItems = [
    {
      name: 'Café expresso',
      description: 'Extração intensa, crema dourada e aroma marcante.',
      price: 'R$ 8,00',
    },
    {
      name: 'Cappuccino',
      description: 'Espresso, leite vaporizado e espuma cremosa.',
      price: 'R$ 12,00',
    },
    {
      name: 'Brownie artesanal',
      description: 'Chocolate intenso, textura úmida e finalização premium.',
      price: 'R$ 14,90',
    },
    {
      name: 'Cookies Blue Coffee',
      description: 'Cookies crocantes por fora e macios por dentro.',
      price: 'R$ 9,90',
    },
    {
      name: 'Bebidas especiais',
      description: 'Latte, mocha, cold brew e receitas exclusivas da casa.',
      price: 'A partir de R$ 13,90',
    },
  ];

  readonly differentials: readonly DifferentialItem[] = [
    {
      icon: '🌱',
      title: 'Grãos Selecionados',
      description: 'Origem certificada e torra artesanal para garantir sabor superior em cada xícara.',
    },
    {
      icon: '🎉',
      title: 'Cafés Temáticos',
      description: 'Edições especiais que celebram datas e momentos únicos do calendário.',
    },
    {
      icon: '💙',
      title: 'Experiência Personalizada',
      description: 'Atendimento exclusivo para harmonizar o café perfeito com o seu paladar.',
    },
    {
      icon: '🏬',
      title: 'Loja Física e Online',
      description: 'Compre onde for mais conveniente, com a mesma qualidade Blue Coffee.',
    },
    {
      icon: '📦',
      title: 'Produtos para Todo Ano',
      description: 'Do café da manhã às festas de fim de ano, sempre há um Blue Coffee ideal.',
    },
  ];

  readonly contactLinks: readonly ContactLink[] = [
    {
      icon: '📸',
      label: 'Instagram',
      value: '@coffeee_blue',
      href: 'https://www.instagram.com/coffeee_blue?utm_source=qr',
    },
    {
      icon: '✉️',
      label: 'E-mail',
      value: 'contato@coffeeblue.com.br',
      href: 'mailto:contato@coffeeblue.com.br',
    },
  ];

  readonly cardapioSteps: readonly CardapioStep[] = [
    { number: 1, title: 'Ler QR Code', description: 'Acesse o cardápio direto pelo celular.' },
    {
      number: 2,
      title: 'Escolher produtos',
      description: 'Cafés, bebidas, doces e produtos organizados por categoria.',
    },
    {
      number: 3,
      title: 'Conferir resumo',
      description: 'Veja itens, quantidades e valor total antes de finalizar.',
    },
    {
      number: 4,
      title: 'Informar telefone',
      description: 'O pedido fica associado ao número do cliente.',
    },
    {
      number: 5,
      title: 'Finalizar pedido',
      description: 'A equipe Blue Coffee recebe a solicitação para atendimento.',
    },
  ];

  constructor() {
    afterNextRender(() => this.observeRevealElements());
  }


  goToAnchor(href: string | undefined, event?: Event): void {
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










  forceHeroVideoMuted(event: Event): void {
    const video = event.target as HTMLVideoElement | null;

    if (!video) {
      return;
    }

    video.muted = true;
    video.defaultMuted = true;
    video.volume = 0;
    this.isHeroVideoMuted.set(true);

    video.play().catch(() => undefined);
  }

  toggleHeroVideoAudio(): void {
    const video = document.getElementById('hero-video') as HTMLVideoElement | null;

    if (!video) {
      return;
    }

    const shouldOpenAudio = this.isHeroVideoMuted();

    if (shouldOpenAudio) {
      video.muted = false;
      video.defaultMuted = false;
      video.volume = 1;
      this.isHeroVideoMuted.set(false);

      video.play().catch(() => {
        video.muted = true;
        video.defaultMuted = true;
        video.volume = 0;
        this.isHeroVideoMuted.set(true);
      });

      return;
    }

    video.muted = true;
    video.defaultMuted = true;
    video.volume = 0;
    this.isHeroVideoMuted.set(true);
  }


  closeSelectedCeo(): void {
    if (!this.selectedCeo() || this.isCeoClosing()) return;

    this.isCeoClosing.set(true);

    window.setTimeout(() => {
      this.selectedCeo.set(null);
      this.isCeoClosing.set(false);
    }, 360);
  }


  @HostListener('document:click', ['$event'])
  onMobileMenuDocumentClick(event: MouseEvent): void {
    if (!this.isMenuOpen()) return;

    const target = event.target as HTMLElement | null;
    if (!target) return;

    const clickedInsideHeader = target.closest('.header');
    const clickedInsideNav = target.closest('.nav');
    const clickedToggle = target.closest('.menu-toggle');

    if (clickedInsideNav || clickedToggle || clickedInsideHeader) {
      return;
    }

    this.closeMenu();
  }

  toggleMenu(): void {
    this.isMenuOpen.update((open) => !open);
  }

  closeMenu(): void {
    this.isMenuOpen.set(false);
  }

  onWindowScroll(): void {
    this.isScrolled.set(window.scrollY > 12);
  }

  private observeRevealElements(): void {
    const elements = this.elementRef.nativeElement.querySelectorAll<HTMLElement>('.reveal');

    if (typeof IntersectionObserver === 'undefined') {
      elements.forEach((el) => el.classList.add('reveal--visible'));
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            entry.target.classList.add('reveal--visible');
            observer.unobserve(entry.target);
          }
        }
      },
      { threshold: 0.15, rootMargin: '0px 0px -40px 0px' },
    );

    elements.forEach((el) => observer.observe(el));
  }

  readonly ceoMembers: readonly CeoMember[] = [
    {
      name: 'BEATRIZ VALMINI',
      nickname: 'Bia',
      role: 'Cofundadora e Diretora de Marketing',
      description:
        'Bia é responsável pela área de marketing da Coffee Blue. Participou da construção da identidade da marca e criou o perfil oficial da empresa nas redes sociais, contribuindo para a divulgação do projeto e para a conexão da marca com seu público.',
      temperament: 'Melancólico',
      image: 'assets/team/ceos/beatriz-valmini-bia.jpeg',
      previewPosition: '48% 30%',
      detailImageSide: 'left',
    },
    {
      name: 'MATEUS DE OLIVEIRA',
      nickname: 'Mateus',
      role: 'Cofundador e Desenvolvedor de Produtos',
      description:
        'Mateus participou da criação de ideias para a Coffee Blue e contribui para o desenvolvimento dos produtos da marca, colaborando com a construção das experiências oferecidas aos clientes.',
      temperament: 'Colérico',
      image: 'assets/team/ceos/mateus-de-oliveira-mateus.jpeg',
      previewPosition: '55% 22%',
      detailImageSide: 'left',
    },
    {
      name: 'RAFAEL CRUZ',
      nickname: 'Rafa',
      role: 'Fundador e Diretor Executivo',
      description:
        'Rafa participou da idealização da Coffee Blue e acompanha o desenvolvimento do projeto desde sua criação. Sua atuação está ligada ao planejamento da empresa e à construção da proposta que deu origem à marca.',
      temperament: 'Melancólico',
      image: 'assets/team/ceos/rafael-cruz-rafa.jpeg',
      previewPosition: '48% 22%',
      detailImageSide: 'left',
    },
    {
      name: 'MARCELO MATOS',
      nickname: 'Martcelito',
      role: 'Cofundador e Colaborador de Projetos',
      description:
        'Marcelo integra a equipe da Coffee Blue e acompanha o desenvolvimento do projeto, contribuindo para as diferentes etapas de construção da marca e apoiando as atividades da equipe.',
      temperament: 'Fleumático',
      image: 'assets/team/ceos/marcelo-matos-martcelito.jpeg',
      previewPosition: '50% 24%',
      detailImageSide: 'right',
    },
    {
      name: 'VALENTINA SCARAZZATI',
      nickname: 'Valen',
      role: 'Cofundadora e Diretora Criativa',
      description:
        'Valen participou da construção do conceito da Coffee Blue, da identidade visual da marca e do desenvolvimento de ideias para produtos e experiências. Seu trabalho contribuiu para transformar a proposta da empresa em uma marca com identidade própria.',
      temperament: 'Sanguíneo',
      image: 'assets/team/ceos/valentina-scarazzati-valen.jpeg',
      previewPosition: '48% 30%',
      detailImageSide: 'right',
    },
  ];

  readonly isCeoClosing = signal(false);
  readonly selectedCeo = signal<CeoMember | null>(null);

  selectCeo(member: CeoMember): void {
    this.isCeoClosing.set(false);
    this.selectedCeo.set(member);
  }

  closeCeo(): void {
    this.selectedCeo.set(null);
  }


  @HostListener('document:click', ['$event'])
  onCeoDocumentClick(event: MouseEvent): void {
    if (!this.selectedCeo()) return;

    const target = event.target as HTMLElement | null;
    if (!target) return;

    const clickedInsideCeoCard = target.closest(
      '.ceo-card, .ceos__card, .ceo-member, .ceo-profile-card, .ceo-person, [data-ceo-card]'
    );

    const clickedInsideCeoDetails = target.closest(
      '.ceo-detail, .ceo-details, .ceo-modal, .ceo-expanded, .ceo-profile, .ceo-dialog, .ceo-overlay, [data-ceo-details]'
    );

    const clickedCloseButton = target.closest(
      'button, a, [role="button"]'
    );

    if (clickedInsideCeoCard || clickedInsideCeoDetails || clickedCloseButton) {
      return;
    }

    this.closeSelectedCeo();
  }

  @HostListener('document:keydown.escape')
  closeCeoOnEscape(): void {
    this.closeMenu();
    this.closeCeo();
  }



  scrollToTop(): void {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }






}
