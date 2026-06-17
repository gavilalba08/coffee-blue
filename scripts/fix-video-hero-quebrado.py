from pathlib import Path
import re

html_path = Path("src/app/home/home.html")
ts_path = Path("src/app/home/home.ts")

html = html_path.read_text(encoding="utf-8")
ts = ts_path.read_text(encoding="utf-8")

source = 'assets/videos/blue-coffee-hero-video-web.mp4'

# 1) Remove botões de áudio antigos/duplicados
html = re.sub(
    r'\n\s*<button\b(?=[^>]*class="hero-video-audio")[\s\S]*?</button>',
    '',
    html
)

# 2) Remove aria-label de áudio que caiu em outros botões por engano
html = re.sub(
    r'\s+\[attr\.aria-label\]="isHeroVideoMuted\(\) \? \'Ativar som do vídeo\' : \'Silenciar vídeo\'"',
    '',
    html
)

# 3) Reescreve o bloco do vídeo corretamente
src_pos = html.find(source)
if src_pos == -1:
    raise SystemExit("ERRO: não encontrei o source do vídeo hero.")

video_start = html.rfind("<video", 0, src_pos)
video_end = html.find("</video>", src_pos)

if video_start == -1 or video_end == -1:
    raise SystemExit("ERRO: não encontrei o bloco <video>...</video>.")

video_end += len("</video>")

line_start = html.rfind("\n", 0, video_start) + 1
indent = html[line_start:video_start]

video_block = f'''{indent}<video id="hero-video" class="hero-video" autoplay muted loop playsinline preload="metadata">
{indent}  <source src="{source}" type="video/mp4" />
{indent}  Seu navegador não suporta vídeos HTML5.
{indent}</video>
{indent}<button
{indent}  class="hero-video-audio"
{indent}  type="button"
{indent}  (click)="toggleHeroVideoAudio()"
{indent}  [attr.aria-label]="isHeroVideoMuted() ? 'Ativar som do vídeo' : 'Silenciar vídeo'"
{indent}>
{indent}  <span aria-hidden="true">{{{{ isHeroVideoMuted() ? '🔇' : '🔊' }}}}</span>
{indent}  <strong>{{{{ isHeroVideoMuted() ? 'Ativar som' : 'Silenciar' }}}}</strong>
{indent}</button>'''

html = html[:video_start] + video_block + html[video_end:]

# 4) Estado inicial: vídeo começa mudo para autoplay funcionar
ts = re.sub(
    r'\n\s*readonly isHeroVideoMuted = signal\((true|false)\);',
    '',
    ts
)

ts = ts.replace(
    "  readonly isScrolled = signal(false);",
    "  readonly isScrolled = signal(false);\n  readonly isHeroVideoMuted = signal(true);",
    1
)

# 5) Remove método antigo
ts = re.sub(
    r"\n  toggleHeroVideoAudio\([^)]*\): void \{[\s\S]*?\n  \}\n(?=\n  toggleMenu\(\): void \{)",
    "\n",
    ts,
    count=1
)

# 6) Insere método funcional
method = """
  toggleHeroVideoAudio(): void {
    const video = document.getElementById('hero-video') as HTMLVideoElement | null;

    if (!video) {
      return;
    }

    const nextMutedState = !this.isHeroVideoMuted();

    video.muted = nextMutedState;
    video.defaultMuted = nextMutedState;
    video.volume = nextMutedState ? 0 : 1;

    this.isHeroVideoMuted.set(nextMutedState);

    if (!nextMutedState) {
      video.play().catch(() => {
        video.muted = true;
        video.defaultMuted = true;
        video.volume = 0;
        this.isHeroVideoMuted.set(true);
      });
    }
  }

"""

ts = ts.replace("  toggleMenu(): void {", method + "  toggleMenu(): void {", 1)

html_path.write_text(html, encoding="utf-8")
ts_path.write_text(ts, encoding="utf-8")

print("OK: bloco do vídeo hero e botão de áudio corrigidos.")
