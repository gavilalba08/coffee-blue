from pathlib import Path
import re

html_path = Path("src/app/home/home.html")
ts_path = Path("src/app/home/home.ts")
scss_path = Path("src/app/home/home.scss")

html = html_path.read_text(encoding="utf-8")
ts = ts_path.read_text(encoding="utf-8")
scss = scss_path.read_text(encoding="utf-8")

# 1) Vídeo começa com som ligado.
# Remove binding [muted] e atributo muted.
html = html.replace(' [muted]="isHeroVideoMuted()"', '')
html = html.replace(' muted ', ' ')
html = html.replace(' muted', '')

# Garante id no vídeo
html = re.sub(
    r'<video([^>]*class="hero-video"[^>]*)>',
    lambda m: '<video' + (
        m.group(1) if 'id="hero-video"' in m.group(1) else ' id="hero-video"' + m.group(1)
    ) + '>',
    html,
    count=1
)

# Garante autoplay loop playsinline preload
html = re.sub(
    r'<video([^>]*)>',
    lambda m: (
        '<video' +
        re.sub(r'\s+', ' ', m.group(1)
               .replace('autoplay', '')
               .replace('loop', '')
               .replace('playsinline', '')
               .replace('preload="metadata"', '')
               .strip()
        ) +
        ' autoplay loop playsinline preload="metadata">'
    ),
    html,
    count=1
)

# 2) Botão com texto correto: começa como "Silenciar"
html = re.sub(
    r'\[attr\.aria-label\]="[^"]*"',
    '[attr.aria-label]="isHeroVideoMuted() ? \'Ativar som do vídeo\' : \'Silenciar vídeo\'"',
    html
)

html = re.sub(
    r"<span aria-hidden=\"true\">\{\{ isHeroVideoMuted\(\) \? '[^']*' : '[^']*' \}\}</span>",
    "<span aria-hidden=\"true\">{{ isHeroVideoMuted() ? '🔇' : '🔊' }}</span>",
    html
)

html = re.sub(
    r"<strong>\{\{ isHeroVideoMuted\(\) \? '[^']*' : '[^']*' \}\}</strong>",
    "<strong>{{ isHeroVideoMuted() ? 'Ativar som' : 'Silenciar' }}</strong>",
    html
)

# 3) Estado inicial agora é false = vídeo com som ligado
ts = ts.replace(
    "readonly isHeroVideoMuted = signal(true);",
    "readonly isHeroVideoMuted = signal(false);"
)

if "readonly isHeroVideoMuted = signal(false);" not in ts:
    ts = ts.replace(
        "  readonly isScrolled = signal(false);",
        "  readonly isScrolled = signal(false);\n  readonly isHeroVideoMuted = signal(false);",
        1
    )

# 4) Remove versões antigas do método
ts = re.sub(
    r"\n  toggleHeroVideoAudio\([^)]*\): void \{[\s\S]*?\n  \}\n(?=\n  toggleMenu\(\): void \{)",
    "\n",
    ts,
    count=1
)

# 5) Método novo e direto: alterna muted, defaultMuted e volume
method = """
  toggleHeroVideoAudio(): void {
    const video = document.getElementById('hero-video') as HTMLVideoElement | null;

    if (!video) {
      return;
    }

    const shouldMute = !video.muted;

    video.muted = shouldMute;
    video.defaultMuted = shouldMute;
    video.volume = shouldMute ? 0 : 1;

    this.isHeroVideoMuted.set(shouldMute);

    if (!shouldMute) {
      video.play().catch(() => {
        video.muted = true;
        video.defaultMuted = true;
        video.volume = 0;
        this.isHeroVideoMuted.set(true);
      });
    }
  }

"""

if "toggleHeroVideoAudio(): void" not in ts:
    ts = ts.replace("  toggleMenu(): void {", method + "  toggleMenu(): void {", 1)
else:
    ts = re.sub(
        r"\n  toggleHeroVideoAudio\(\): void \{[\s\S]*?\n  \}\n(?=\n  toggleMenu\(\): void \{)",
        "\n" + method,
        ts,
        count=1
    )

# 6) Deixa o botão com cara de controle simples
scss += r'''

/* PATCH FINAL — BOTÃO AUDIO FUNCIONAL */
.hero-video-audio {
  right: 1rem !important;
  bottom: 1rem !important;
  z-index: 20 !important;
  pointer-events: auto !important;
}
'''

html_path.write_text(html, encoding="utf-8")
ts_path.write_text(ts, encoding="utf-8")
scss_path.write_text(scss, encoding="utf-8")

print("OK: áudio do hero corrigido. Vídeo inicia com som; botão silencia/ativa.")
