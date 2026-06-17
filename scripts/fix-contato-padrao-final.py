from pathlib import Path
import re

html_path = Path("src/app/home/home.html")
scss_path = Path("src/app/home/home.scss")

html = html_path.read_text(encoding="utf-8")
scss = scss_path.read_text(encoding="utf-8")

novo_contato = '''  <section id="contato" class="section section--alt">
    <div class="container">
      <div class="section__header">
        <span class="eyebrow">FALE COM A GENTE</span>
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

html, count = re.subn(
    r'  <section id="contato"[\s\S]*?</section>',
    novo_contato,
    html,
    count=1
)

if count == 0:
    raise SystemExit("ERRO: não encontrei a seção id='contato'.")

# Remove patches anteriores do contato
scss = re.sub(r'/\* PATCH — CENTRALIZAR CARDS DE REDES SOCIAIS / CONTATO \*/[\s\S]*?(?=/\*|$)', '', scss)
scss = re.sub(r'/\* PATCH REAL — CONTATO CENTRALIZADO \*/[\s\S]*?(?=/\*|$)', '', scss)
scss = re.sub(r'/\* PATCH — CONTATO: SOMENTE CENTRALIZAR CARDS \*/[\s\S]*?(?=/\*|$)', '', scss)
scss = re.sub(r'/\* PATCH CONTATO[\s\S]*?(?=/\*|$)', '', scss)

scss += r'''

/* PATCH FINAL — CONTATO COM TEXTO PADRÃO E CARDS CENTRALIZADOS */
#contato .section__header {
  text-align: center;
  max-width: 760px;
  margin-left: auto;
  margin-right: auto;
}

#contato .section__header .eyebrow {
  display: inline-block;
  margin-bottom: 0.65rem;
  color: #0b4b84;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.22em;
  text-transform: uppercase;
}

#contato .section__header h2 {
  margin: 0;
  color: #02142c;
  font-family: 'Playfair Display', Georgia, serif;
  font-size: clamp(2.45rem, 4vw, 4.1rem);
  line-height: 1.05;
  font-weight: 700;
}

#contato .section__header p {
  max-width: 680px;
  margin: 1rem auto 0;
  color: #566b8e;
  font-size: 1.05rem;
  line-height: 1.7;
}

#contato .contact-cards-center {
  width: 100%;
  max-width: 620px;
  margin: 3.25rem auto 0;
  display: flex;
  justify-content: center;
  align-items: stretch;
  gap: 1.25rem;
  flex-wrap: wrap;
}

#contato .contact-card-center {
  width: 270px;
  min-height: 108px;
  padding: 1.25rem 1.4rem;
  border-radius: 1rem;
  background: #fff;
  color: #02142c;
  text-decoration: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  box-shadow: 0 18px 45px rgba(2, 20, 44, 0.08);
  transition: transform 180ms ease, box-shadow 180ms ease;
}

#contato .contact-card-center:hover {
  transform: translateY(-3px);
  box-shadow: 0 22px 55px rgba(2, 20, 44, 0.12);
}

#contato .contact-card-center__icon {
  flex: 0 0 auto;
  font-size: 1.7rem;
  line-height: 1;
}

#contato .contact-card-center__content {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-align: left;
}

#contato .contact-card-center__content strong {
  font-weight: 700;
  line-height: 1.2;
}

#contato .contact-card-center__content small {
  color: #566b8e;
  line-height: 1.35;
  overflow-wrap: anywhere;
}

@media (max-width: 640px) {
  #contato .contact-cards-center {
    max-width: 320px;
  }

  #contato .contact-card-center {
    width: 100%;
  }
}
'''

html_path.write_text(html, encoding="utf-8")
scss_path.write_text(scss, encoding="utf-8")

print("OK: contato corrigido com texto padrão e cards centralizados.")
