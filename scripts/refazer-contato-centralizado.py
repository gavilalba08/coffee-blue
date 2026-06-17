from pathlib import Path
import re

html_path = Path("src/app/home/home.html")
scss_path = Path("src/app/home/home.scss")

html = html_path.read_text(encoding="utf-8")
scss = scss_path.read_text(encoding="utf-8")

novo_contato = '''  <section id="contato" class="section section--alt contact-section">
    <div class="container">
      <div class="section__header contact-section__header">
        <span class="eyebrow">Fale com a gente</span>
        <h2>Redes Sociais &amp; Contato</h2>
        <p>Estamos por perto — siga, mande mensagem ou envie um e-mail.</p>
      </div>

      <div class="contact-cards-center" aria-label="Redes sociais e contato da Blue Coffee">
        <a
          class="contact-card-center"
          href="https://www.instagram.com/coffeee_blue?utm_source=qr"
          target="_blank"
          rel="noopener noreferrer"
          aria-label="Abrir Instagram da Blue Coffee"
        >
          <span class="contact-card-center__icon">📸</span>
          <span class="contact-card-center__content">
            <strong>Instagram</strong>
            <small>@coffeee_blue</small>
          </span>
        </a>

        <a
          class="contact-card-center"
          href="mailto:contato@coffeeblue.com.br"
          aria-label="Enviar e-mail para a Blue Coffee"
        >
          <span class="contact-card-center__icon">✉️</span>
          <span class="contact-card-center__content">
            <strong>E-mail</strong>
            <small>contato@coffeeblue.com.br</small>
          </span>
        </a>
      </div>
    </div>
  </section>'''

# Substitui somente a seção real de contato
html, count = re.subn(
    r'  <section id="contato"[\s\S]*?</section>',
    novo_contato,
    html,
    count=1
)

if count == 0:
    raise SystemExit("ERRO: não encontrei a seção id='contato' para substituir.")

css_patch = r'''

/* PATCH REAL — CONTATO CENTRALIZADO */
#contato.contact-section {
  text-align: center;
}

#contato .contact-section__header {
  text-align: center;
  margin-left: auto;
  margin-right: auto;
}

#contato .contact-cards-center {
  width: min(560px, 100%);
  margin: 3rem auto 0;
  display: grid;
  grid-template-columns: repeat(2, minmax(220px, 1fr));
  gap: 1.25rem;
  justify-content: center;
  align-items: stretch;
}

#contato .contact-card-center {
  min-height: 108px;
  padding: 1.35rem 1.5rem;
  border-radius: 1rem;
  background: #fff;
  color: #02142c;
  text-decoration: none;
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 1rem;
  align-items: center;
  justify-content: center;
  box-shadow: 0 18px 45px rgba(2, 20, 44, 0.08);
  transition: transform 180ms ease, box-shadow 180ms ease;
}

#contato .contact-card-center:hover {
  transform: translateY(-3px);
  box-shadow: 0 22px 55px rgba(2, 20, 44, 0.12);
}

#contato .contact-card-center__icon {
  font-size: 1.8rem;
  line-height: 1;
}

#contato .contact-card-center__content {
  display: grid;
  gap: 0.25rem;
  text-align: left;
}

#contato .contact-card-center__content strong {
  font-weight: 700;
}

#contato .contact-card-center__content small {
  color: #566b8e;
  line-height: 1.35;
  overflow-wrap: anywhere;
}

@media (max-width: 640px) {
  #contato .contact-cards-center {
    width: min(320px, 100%);
    grid-template-columns: 1fr;
  }

  #contato .contact-card-center {
    grid-template-columns: 1fr;
    text-align: center;
  }

  #contato .contact-card-center__content {
    text-align: center;
  }
}
'''

# Remove patch antigo se tiver duplicado e adiciona o novo no final
scss = re.sub(r'/\* PATCH — CENTRALIZAR CARDS DE REDES SOCIAIS / CONTATO \*/[\s\S]*?(?=/\*|$)', '', scss)
scss = re.sub(r'/\* PATCH REAL — CONTATO CENTRALIZADO \*/[\s\S]*?(?=/\*|$)', '', scss)

scss += css_patch

html_path.write_text(html, encoding="utf-8")
scss_path.write_text(scss, encoding="utf-8")

print("OK: seção de contato refeita e centralizada.")
