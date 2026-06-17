from pathlib import Path
import re

html_path = Path("src/app/home/home.html")
ts_path = Path("src/app/home/home.ts")

html = html_path.read_text(encoding="utf-8")
ts = ts_path.read_text(encoding="utf-8")

# 1) Corrigir video: remover #heroVideo e garantir id
html = html.replace("<video #heroVideo", "<video")
html = re.sub(
    r'<video([^>]*class="hero-video"[^>]*)>',
    lambda m: '<video' + (
        m.group(1) if 'id="hero-video"' in m.group(1) else ' id="hero-video"' + m.group(1)
    ) + '>',
    html,
    count=1
)

# 2) Corrigir click do botão: não passa mais heroVideo
html = html.replace(
    '(click)="toggleHeroVideoAudio(heroVideo)"',
    '(click)="toggleHeroVideoAudio()"'
)

# 3) Garantir signal
if "readonly isHeroVideoMuted = signal(true);" not in ts:
    ts = ts.replace(
        "  readonly isScrolled = signal(false);",
        "  readonly isScrolled = signal(false);\n  readonly isHeroVideoMuted = signal(true);",
        1
    )

# 4) Remover método antigo com parâmetro, se existir
ts = re.sub(
    r"\n  toggleHeroVideoAudio\(video: HTMLVideoElement\): void \{[\s\S]*?\n  \}\n(?=\n  toggleMenu\(\): void \{)",
    "\n",
    ts,
    count=1
)

# 5) Inserir método novo sem parâmetro
if "toggleHeroVideoAudio(): void" not in ts:
    method = """
  toggleHeroVideoAudio(): void {
    const video = document.getElementById('hero-video') as HTMLVideoElement | null;

    if (!video) {
      return;
    }

    const nextMutedState = !this.isHeroVideoMuted();

    video.muted = nextMutedState;
    this.isHeroVideoMuted.set(nextMutedState);

    if (!nextMutedState) {
      video.play().catch(() => {
        video.muted = true;
        this.isHeroVideoMuted.set(true);
      });
    }
  }

"""
    ts = ts.replace("  toggleMenu(): void {", method + "  toggleMenu(): void {", 1)

html_path.write_text(html, encoding="utf-8")
ts_path.write_text(ts, encoding="utf-8")

print("OK: botão de áudio corrigido para usar id do vídeo.")
