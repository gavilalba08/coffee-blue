from pathlib import Path
import re

ts_path = Path("src/app/home/home.ts")
html_path = Path("src/app/home/home.html")
scss_path = Path("src/app/home/home.scss")

ts = ts_path.read_text(encoding="utf-8")
html = html_path.read_text(encoding="utf-8")
scss = scss_path.read_text(encoding="utf-8")

# 1) Descobrir signal do CEO selecionado.
candidates = re.findall(
    r"(?:readonly\s+)?(\w*(?:Ceo|CEO)\w*)\s*=\s*signal(?:<[^>]+>)?\(null\)",
    ts
)

if not candidates:
    candidates = re.findall(
        r"(?:readonly\s+)?(\w*(?:selected|active|opened|current)\w*)\s*=\s*signal(?:<[^>]+>)?\(null\)",
        ts,
        flags=re.IGNORECASE
    )

if not candidates:
    raise SystemExit(
        "Não consegui detectar o signal do CEO aberto. Rode:\n"
        "grep -nE \"Ceo|CEO|selected|active|opened|current|signal\" src/app/home/home.ts | sed -n '1,240p'"
    )

selected_signal = candidates[0]
print("Signal CEO aberto:", selected_signal)

# 2) Adicionar signal de fechamento.
if "isCeoClosing = signal(false)" not in ts and "isCeoClosing=signal(false)" not in ts:
    ts = ts.replace(
        f"  readonly {selected_signal}",
        "  readonly isCeoClosing = signal(false);\n  readonly " + selected_signal,
        1
    )

# 3) Criar método closeSelectedCeo com delay de animação.
close_method = f"""
  closeSelectedCeo(): void {{
    if (!this.{selected_signal}() || this.isCeoClosing()) return;

    this.isCeoClosing.set(true);

    window.setTimeout(() => {{
      this.{selected_signal}.set(null);
      this.isCeoClosing.set(false);
    }}, 360);
  }}

"""

if "closeSelectedCeo(): void" not in ts:
    if "  toggleMenu(): void {" in ts:
        ts = ts.replace("  toggleMenu(): void {", close_method + "  toggleMenu(): void {", 1)
    elif "  goToAnchor(" in ts:
        ts = ts.replace("  goToAnchor(", close_method + "  goToAnchor(", 1)
    else:
        ts = ts.rstrip().replace("\n}", close_method + "\n}", 1)

# 4) Toda ação de abrir CEO deve cancelar estado de fechamento.
# Procura métodos que recebem CEO e fazem selected.set(ceo).
set_pattern = rf"(this\.{selected_signal}\.set\((?!null)[^)]+\);)"
ts = re.sub(
    set_pattern,
    "this.isCeoClosing.set(false);\n    " + r"\1",
    ts
)

# Remove duplicações caso rode mais de uma vez.
ts = re.sub(
    r"(this\.isCeoClosing\.set\(false\);\n\s*){2,}",
    "this.isCeoClosing.set(false);\n    ",
    ts
)

# 5) Trocar fechamento imediato por fechamento animado.
# Só troca set(null) do CEO por closeSelectedCeo(), exceto dentro do próprio método closeSelectedCeo.
parts = ts.split("closeSelectedCeo(): void")
if len(parts) == 2:
    before, after = parts
    before = re.sub(
        rf"this\.{selected_signal}\.set\(null\);",
        "this.closeSelectedCeo();",
        before
    )

    # preserva o set(null) dentro do método closeSelectedCeo
    method_body, *rest = after.split("  toggleMenu(): void", 1)
    if rest:
        rest_text = "  toggleMenu(): void" + rest[0]
        rest_text = re.sub(
            rf"this\.{selected_signal}\.set\(null\);",
            "this.closeSelectedCeo();",
            rest_text
        )
        ts = before + "closeSelectedCeo(): void" + method_body + rest_text
    else:
        ts = before + "closeSelectedCeo(): void" + after
else:
    ts = re.sub(
        rf"this\.{selected_signal}\.set\(null\);",
        "this.closeSelectedCeo();",
        ts
    )

# Garante que dentro do closeSelectedCeo continuou com set(null), não virou recursão.
ts = re.sub(
    rf"(closeSelectedCeo\(\): void \{{[\s\S]*?window\.setTimeout\(\(\) => \{{[\s\S]*?)this\.closeSelectedCeo\(\);",
    rf"\1this.{selected_signal}.set(null);",
    ts,
    count=1
)

ts_path.write_text(ts, encoding="utf-8")

# 6) HTML: adicionar classe de abertura/fechamento no container de detalhe do CEO.
# Primeiro tenta achar containers conhecidos.
classes = [
    "ceo-detail",
    "ceo-details",
    "ceo-modal",
    "ceo-expanded",
    "ceo-profile",
    "ceo-dialog",
    "ceo-overlay",
]

for cls in classes:
    pattern = rf'(<(?:article|div|section)[^>]*class="[^"]*\b{cls}\b[^"]*"[^>]*)(>)'
    if re.search(pattern, html):
        html = re.sub(
            pattern,
            lambda m: m.group(1)
            if "ceo-detail--closing" in m.group(1)
            else m.group(1) + ' [class.ceo-detail--closing]="isCeoClosing()" [class.ceo-detail--opening]="!isCeoClosing()"' + m.group(2),
            html,
            count=1
        )
        break

# Se já foi marcado anteriormente com data-ceo-details, usa esse seletor.
if "ceo-detail--closing" not in html:
    html = re.sub(
        r'(<(?:article|div|section)[^>]*data-ceo-details[^>]*)(>)',
        lambda m: m.group(1) + ' [class.ceo-detail--closing]="isCeoClosing()" [class.ceo-detail--opening]="!isCeoClosing()"' + m.group(2),
        html,
        count=1
    )

# Botão X: garantir fechamento animado.
html = re.sub(
    r'\(click\)="[^"]*(?:close|Close|selected|Ceo|CEO)[^"]*"',
    '(click)="closeSelectedCeo()"',
    html,
    count=1
)

html_path.write_text(html, encoding="utf-8")

# 7) SCSS: animações de abrir e fechar.
scss = re.sub(
    r"/\* PATCH FINAL — ANIMACAO CEO ABRIR FECHAR \*/[\s\S]*$",
    "",
    scss
).rstrip()

patch = r'''

/* PATCH FINAL — ANIMACAO CEO ABRIR FECHAR */
@keyframes ceoDetailOpen {
  0% {
    opacity: 0;
    transform: translateY(28px) scale(0.94);
    filter: blur(8px);
  }

  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
    filter: blur(0);
  }
}

@keyframes ceoDetailClose {
  0% {
    opacity: 1;
    transform: translateY(0) scale(1);
    filter: blur(0);
  }

  100% {
    opacity: 0;
    transform: translateY(26px) scale(0.94);
    filter: blur(8px);
  }
}

@keyframes ceoPhotoOpen {
  0% {
    opacity: 0;
    transform: translateX(-34px) scale(0.96);
  }

  100% {
    opacity: 1;
    transform: translateX(0) scale(1);
  }
}

@keyframes ceoTextOpen {
  0% {
    opacity: 0;
    transform: translateX(34px);
  }

  100% {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes ceoPhotoClose {
  0% {
    opacity: 1;
    transform: translateX(0) scale(1);
  }

  100% {
    opacity: 0;
    transform: translateX(-30px) scale(0.96);
  }
}

@keyframes ceoTextClose {
  0% {
    opacity: 1;
    transform: translateX(0);
  }

  100% {
    opacity: 0;
    transform: translateX(30px);
  }
}

.ceo-detail,
.ceo-details,
.ceo-modal,
.ceo-expanded,
.ceo-profile,
.ceo-dialog,
.ceo-overlay,
[data-ceo-details] {
  transform-origin: center center;
  will-change: opacity, transform, filter;
}

.ceo-detail--opening {
  animation: ceoDetailOpen 360ms cubic-bezier(0.22, 1, 0.36, 1) both;
}

.ceo-detail--closing {
  pointer-events: none !important;
  animation: ceoDetailClose 320ms cubic-bezier(0.64, 0, 0.78, 0) both;
}

.ceo-detail--opening img,
.ceo-detail--opening .ceo-detail__image,
.ceo-detail--opening .ceo-profile__image,
.ceo-detail--opening .ceo-modal__image {
  animation: ceoPhotoOpen 420ms cubic-bezier(0.22, 1, 0.36, 1) both;
}

.ceo-detail--opening .ceo-detail__content,
.ceo-detail--opening .ceo-profile__content,
.ceo-detail--opening .ceo-modal__content,
.ceo-detail--opening .ceo-info,
.ceo-detail--opening .ceo-text {
  animation: ceoTextOpen 420ms cubic-bezier(0.22, 1, 0.36, 1) 60ms both;
}

.ceo-detail--closing img,
.ceo-detail--closing .ceo-detail__image,
.ceo-detail--closing .ceo-profile__image,
.ceo-detail--closing .ceo-modal__image {
  animation: ceoPhotoClose 280ms cubic-bezier(0.64, 0, 0.78, 0) both;
}

.ceo-detail--closing .ceo-detail__content,
.ceo-detail--closing .ceo-profile__content,
.ceo-detail--closing .ceo-modal__content,
.ceo-detail--closing .ceo-info,
.ceo-detail--closing .ceo-text {
  animation: ceoTextClose 260ms cubic-bezier(0.64, 0, 0.78, 0) both;
}

@media (prefers-reduced-motion: reduce) {
  .ceo-detail--opening,
  .ceo-detail--closing,
  .ceo-detail--opening img,
  .ceo-detail--closing img,
  .ceo-detail--opening .ceo-detail__content,
  .ceo-detail--closing .ceo-detail__content,
  .ceo-detail--opening .ceo-profile__content,
  .ceo-detail--closing .ceo-profile__content,
  .ceo-detail--opening .ceo-modal__content,
  .ceo-detail--closing .ceo-modal__content {
    animation: none !important;
  }
}
'''

scss += "\n" + patch + "\n"
scss_path.write_text(scss, encoding="utf-8")

print("OK: animação de abrir/sumir fechando aplicada.")
