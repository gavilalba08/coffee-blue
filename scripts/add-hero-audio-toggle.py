from pathlib import Path
import re

html_path = Path("src/app/home/home.html")
ts_path = Path("src/app/home/home.ts")
scss_path = Path("src/app/home/home.scss")

html = html_path.read_text(encoding="utf-8")
ts = ts_path.read_text(encoding="utf-8")
scss = scss_path.read_text(encoding="utf-8")

# 1) Adiciona estado no TS
if "isHeroVideoMuted" not in ts:
    ts = ts.replace(
        "  readonly isScrolled = signal(false);",
        "  readonly isScrolled = signal(false);\n  readonly isHeroVideoMuted = signal(true);",
        1
    )

# 2) Adiciona método no TS antes do toggleMenu
if "toggleHeroVideoAudio" not in ts:
    method = """
  toggleHeroVideoAudio(video: HTMLVideoElement): void {
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

# 3) Marca o vídeo com #heroVideo e binding muted
html = re.sub(
    r'<video\s+class="hero-video"\s+autoplay\s+muted\s+loop\s+playsinline\s+preload="metadata">',
    '<video #heroVideo class="hero-video" autoplay [muted]="isHeroVideoMuted()" loop playsinline preload="metadata">',
    html,
    count=1
)

# Caso já esteja sem muted em alguma versão
html = re.sub(
    r'<video\s+class="hero-video"\s+autoplay\s+loop\s+playsinline\s+preload="metadata">',
    '<video #heroVideo class="hero-video" autoplay [muted]="isHeroVideoMuted()" loop playsinline preload="metadata">',
    html,
    count=1
)

# 4) Insere o botão logo depois do </video> do hero
button = '''
          <button
            class="hero-video-audio"
            type="button"
            (click)="toggleHeroVideoAudio(heroVideo)"
            [attr.aria-label]="isHeroVideoMuted() ? 'Ativar som do vídeo' : 'Silenciar vídeo'"
          >
            <span aria-hidden="true">{{ isHeroVideoMuted() ? '🔇' : '🔊' }}</span>
            <strong>{{ isHeroVideoMuted() ? 'Ativar som' : 'Silenciar' }}</strong>
          </button>'''

if "hero-video-audio" not in html:
    html = html.replace("</video>", "</video>\n" + button, 1)

# 5) CSS do botão
if "PATCH — BOTAO AUDIO HERO VIDEO" not in scss:
    scss += r'''

/* PATCH — BOTAO AUDIO HERO VIDEO */
.hero-video-card,
.hero__video,
.hero-video-wrapper,
.hero-media,
.hero__media {
  position: relative;
}

.hero-video-audio {
  position: absolute;
  right: 1rem;
  bottom: 1rem;
  z-index: 5;
  min-height: 42px;
  padding: 0.65rem 0.95rem;
  border: 1px solid rgba(227, 182, 75, 0.55);
  border-radius: 999px;
  background: rgba(2, 20, 44, 0.82);
  color: #fffdf8;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font: inherit;
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  backdrop-filter: blur(10px);
  box-shadow: 0 16px 38px rgba(2, 20, 44, 0.28);
  transition: transform 180ms ease, background 180ms ease, border-color 180ms ease;
}

.hero-video-audio:hover {
  transform: translateY(-2px);
  background: rgba(2, 20, 44, 0.94);
  border-color: rgba(227, 182, 75, 0.9);
}

.hero-video-audio span {
  font-size: 1rem;
  line-height: 1;
}

.hero-video-audio strong {
  line-height: 1;
}

@media (max-width: 720px) {
  .hero-video-audio {
    right: 0.75rem;
    bottom: 0.75rem;
    min-height: 38px;
    padding: 0.58rem 0.78rem;
    font-size: 0.68rem;
  }
}
'''

html_path.write_text(html, encoding="utf-8")
ts_path.write_text(ts, encoding="utf-8")
scss_path.write_text(scss, encoding="utf-8")

print("OK: botão de áudio do vídeo adicionado.")
