from pathlib import Path
import re

ts_path = Path("src/app/home/home.ts")
html_path = Path("src/app/home/home.html")

ts = ts_path.read_text(encoding="utf-8")
html = html_path.read_text(encoding="utf-8")

# 1) Tenta descobrir qual signal guarda o CEO aberto.
signal_candidates = re.findall(
    r"(?:readonly\s+)?(\w*(?:Ceo|CEO)\w*)\s*=\s*signal(?:<[^>]+>)?\(null\)",
    ts
)

if not signal_candidates:
    signal_candidates = re.findall(
        r"(?:readonly\s+)?(\w*(?:selected|active|opened|current)\w*)\s*=\s*signal(?:<[^>]+>)?\(null\)",
        ts,
        flags=re.IGNORECASE
    )

if not signal_candidates:
    raise SystemExit(
        "Não consegui identificar automaticamente o signal do CEO aberto. "
        "Rode: grep -nE \"signal\\(|selected|active|opened|current|Ceo|CEO\" src/app/home/home.ts | sed -n '1,220p'"
    )

selected_signal = signal_candidates[0]
print(f"Signal detectado para CEO aberto: {selected_signal}")

# 2) Garante que HostListener está importado.
if "HostListener" not in ts.split("from '@angular/core'")[0]:
    ts = ts.replace(
        "import { ChangeDetectionStrategy, Component, ElementRef,",
        "import { ChangeDetectionStrategy, Component, ElementRef, HostListener,",
        1
    )

# Se o import já tem lista em uma linha diferente, tenta adicionar sem duplicar.
ts = re.sub(
    r"import \{([^}]*?)\} from '@angular/core';",
    lambda m: "import {" + (
        m.group(1) if "HostListener" in m.group(1)
        else m.group(1).rstrip() + ", HostListener"
    ) + "} from '@angular/core';",
    ts,
    count=1
)

# 3) Remove método duplicado antigo se existir.
ts = re.sub(
    r"\n\s*@HostListener\('document:click', \['\$event'\]\)\s*\n\s*onCeoDocumentClick\([^)]*\): void \{[\s\S]*?\n\s*\}\n(?=\s*(?:@HostListener|toggleMenu|closeMenu|goToAnchor|scrollToTop|open|close|select|$))",
    "\n",
    ts
)

# 4) Cria método de clique fora.
method = f"""
  @HostListener('document:click', ['$event'])
  onCeoDocumentClick(event: MouseEvent): void {{
    if (!this.{selected_signal}()) return;

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

    if (clickedInsideCeoCard || clickedInsideCeoDetails || clickedCloseButton) {{
      return;
    }}

    this.{selected_signal}.set(null);
  }}

"""

# Insere antes do primeiro HostListener existente de escape, ou antes do toggleMenu.
if "onCeoDocumentClick" not in ts:
    if "@HostListener('document:keydown.escape')" in ts:
        ts = ts.replace("  @HostListener('document:keydown.escape')", method + "  @HostListener('document:keydown.escape')", 1)
    elif "  toggleMenu(): void {" in ts:
        ts = ts.replace("  toggleMenu(): void {", method + "  toggleMenu(): void {", 1)
    else:
        ts = ts.rstrip().replace("\n}", method + "\n}", 1)

# 5) Melhora o HTML: marca os cards e detalhes de CEO para o clique fora funcionar com segurança.
# Marca botões/cards dentro da seção CEOs, sem depender de nome exato demais.
ceos_match = re.search(r'(<section[^>]+id="ceos"[\s\S]*?</section>)', html)

if ceos_match:
    ceos = ceos_match.group(1)

    # Marca containers comuns de card como data-ceo-card.
    ceos = re.sub(
        r'(<(?:button|article|div)[^>]+class="[^"]*(?:ceo-card|ceos__card|ceo-member|ceo-person)[^"]*"[^>]*)(>)',
        lambda m: m.group(1) if "data-ceo-card" in m.group(1) else m.group(1) + " data-ceo-card" + m.group(2),
        ceos
    )

    # Marca containers comuns de detalhe/modal como data-ceo-details.
    ceos = re.sub(
        r'(<(?:article|div|section)[^>]+class="[^"]*(?:ceo-detail|ceo-details|ceo-modal|ceo-expanded|ceo-profile|ceo-dialog|ceo-overlay)[^"]*"[^>]*)(>)',
        lambda m: m.group(1) if "data-ceo-details" in m.group(1) else m.group(1) + " data-ceo-details" + m.group(2),
        ceos
    )

    html = html[:ceos_match.start()] + ceos + html[ceos_match.end():]
else:
    print("AVISO: não encontrei section id='ceos' para marcar HTML, mas o HostListener ainda foi aplicado.")

ts_path.write_text(ts, encoding="utf-8")
html_path.write_text(html, encoding="utf-8")

print("OK: clique fora do CEO agora fecha o detalhe.")
