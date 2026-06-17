from pathlib import Path
import re

html_path = Path("src/app/home/home.html")
ts_path = Path("src/app/home/home.ts")

html = html_path.read_text(encoding="utf-8")
ts = ts_path.read_text(encoding="utf-8")

source = "assets/videos/blue-coffee-hero-video-web.mp4"

# Remove botões de áudio antigos
html = re.sub(
    r'\n\s*<button\b(?=[^>]*class="hero-video-audio")[\s\S]*?</button>',
    '',
    html
)

# Reescreve o bloco do vídeo corretamente, iniciando SEMPRE mudo
src_pos = html.find(source)
if src_pos == -1:
    raise SystemExit("ERRO: não encontrei o vídeo hero no HTML.")

video_start = html.rfind("<video", 0, src_pos)
video_end = html.find("</video>", src_pos)

if video_start == -1 or video_end == -1:
    raise SystemExit("ERRO: não encontrei o bloco <video>...</video>.")

video_end += len("</video>")
line_start = html.rfind("\n", 0, video_start) + 1
indent = html[line_start:video_start]

video_block = f'''{indent}<video
{indent}  id="hero-video"
{indent}  class="hero-video"
{indent}  autoplay
{indent}  muted
{indent}  loop
{indent}  playsinline
{indent}  preload="metadata"
{indent}  (loadedmetadata)="forceHeroVideoMuted($event)"
{indent}>
{indent}  <source src="{source}" type="video/mp4" />
{indent}  Seu navegador não suporta vídeos HTML5.
{indent}</video>
{indent}<button
{indent}  class="hero-video-audio"
{indent}  type="button"
{indent}  (click)="toggleHeroVideoAudio()"
{indent}  [attr.aria-label]="isHeroVideoMuted() ? 'Abrir áudio do vídeo' : 'Silenciar vídeo'"
{indent}>
{indent}  <span aria-hidden="true">{{{{ isHeroVideoMuted() ? '🔇' : '🔊' }}}}</span>
{indent}  <strong>{{{{ isHeroVideoMuted() ? 'Abrir áudio' : 'Silenciar' }}}}</strong>
{indent}</button>'''

html = html[:video_start] + video_block + html[video_end:]

# Remove signal antigo e recria iniciando true
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

# Remove métodos antigos
ts = re.sub(
    r"\n  forceHeroVideoMuted\([^)]*\): void \{[\s\S]*?\n  \}\n(?=\n  toggleHeroVideoAudio\(\): void \{|\n  toggleMenu\(\): void \{)",
    "\n",
    ts,
    count=1
)

ts = re.sub(
    r"\n  toggleHeroVideoAudio\([^)]*\): void \{[\s\S]*?\n  \}\n(?=\n  toggleMenu\(\): void \{)",
    "\n",
    ts,
    count=1
)

# Insere métodos novos
methods = """
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

"""

ts = ts.replace("  toggleMenu(): void {", methods + "  toggleMenu(): void {", 1)

html_path.write_text(html, encoding="utf-8")
ts_path.write_text(ts, encoding="utf-8")

print("OK: vídeo agora inicia mudo e só abre áudio ao clicar.")
