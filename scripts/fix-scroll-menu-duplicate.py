from pathlib import Path
import re

ts_path = Path("src/app/home/home.ts")
html_path = Path("src/app/home/home.html")

# =========================================================
# 1) HOME.TS — remover TODAS as versões de scrollToSection
#    e inserir apenas uma versão correta.
# =========================================================

def remove_method(text: str, method_name: str) -> str:
    pattern = re.compile(
        rf"\n\s{{2}}{method_name}\s*\([^)]*\)\s*:\s*void\s*\{{",
        re.MULTILINE,
    )

    while True:
        match = pattern.search(text)
        if not match:
            break

        start = match.start()
        brace_start = text.find("{", match.end() - 1)
        if brace_start == -1:
            raise SystemExit(f"Não encontrei abertura do método {method_name}")

        depth = 0
        end = None

        for i in range(brace_start, len(text)):
            char = text[i]
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break

        if end is None:
            raise SystemExit(f"Não encontrei fechamento do método {method_name}")

        text = text[:start] + text[end:]

    return text


ts = ts_path.read_text(encoding="utf-8")
ts = remove_method(ts, "scrollToSection")

new_method = """
  scrollToSection(target: string | undefined | null, event?: Event): void {
    if (!target) {
      this.closeMenu();
      return;
    }

    if (target.startsWith('#')) {
      event?.preventDefault();

      const element = document.querySelector<HTMLElement>(target);

      if (element) {
        element.scrollIntoView({
          behavior: 'smooth',
          block: 'start',
        });

        history.replaceState(null, '', target);
      }

      this.closeMenu();
      return;
    }

    this.closeMenu();
  }

"""

# Insere antes do scrollToTop, se existir; senão, antes do fechamento da classe.
if "  scrollToTop(): void" in ts:
    ts = ts.replace("  scrollToTop(): void", new_method + "  scrollToTop(): void", 1)
else:
    idx = ts.rfind("\n}")
    if idx == -1:
        raise SystemExit("Não encontrei fechamento da classe Home.")
    ts = ts[:idx] + new_method + ts[idx:]

ts_path.write_text(ts, encoding="utf-8")

# =========================================================
# 2) HOME.HTML — remover clicks duplicados e corrigir ordem.
# =========================================================

html = html_path.read_text(encoding="utf-8")

# RouterLink deve apenas fechar menu.
html = html.replace(
    '(click)="closeMenu()" (click)="link.href ? scrollToSection($event, link.href) : closeMenu()"',
    '(click)="closeMenu()"',
)

# Link de âncora deve chamar target primeiro e event segundo.
html = html.replace(
    '(click)="scrollToSection(link.href, $event); closeMenu()" (click)="link.href ? scrollToSection($event, link.href) : closeMenu()"',
    '(click)="scrollToSection(link.href, $event)"',
)

# Caso tenha sobrado chamada invertida.
html = html.replace(
    '(click)="link.href ? scrollToSection($event, link.href) : closeMenu()"',
    '(click)="link.href ? scrollToSection(link.href, $event) : closeMenu()"',
)

# Links externos de contato não devem chamar scrollToSection.
html = html.replace(
    ' target="_blank" rel="noopener" (click)="scrollToSection(link.href, $event)"',
    ' target="_blank" rel="noopener"',
)

html_path.write_text(html, encoding="utf-8")

print("OK: removida duplicidade de scrollToSection e corrigidos clicks do menu.")
