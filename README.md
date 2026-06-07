# 🔐 SecureCheck

> Ferramenta de auditoria de segurança web que analisa headers HTTP e certificados SSL de qualquer site, gerando um relatório técnico em PDF.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📋 Sobre

**SecureCheck** é uma aplicação web que realiza auditoria de segurança em sites públicos. A ferramenta verifica a presença de headers HTTP de segurança críticos, valida o certificado SSL e gera um relatório completo em PDF — pronto para uso em pentests básicos, code reviews e validação de boas práticas OWASP.

Projeto desenvolvido como aplicação prática dos certificados **Google Cybersecurity** e **Google Crash Course on Python**.

---

## ✨ Funcionalidades

- ✅ Análise de **7 verificações de segurança**
- ✅ Validação de **certificado SSL** (expiração, validade)
- ✅ Detecção de **headers HTTP** ausentes (XSS, Clickjacking, MIME sniffing)
- ✅ **Score geral** de segurança (0–100)
- ✅ **Relatório PDF** profissional exportável
- ✅ Interface web responsiva

---

## 🔎 Verificações realizadas

| Verificação | Risco mitigado |
|---|---|
| HTTPS Ativo | Tráfego em texto claro |
| Certificado SSL | Man-in-the-Middle, certificado expirado |
| Content-Security-Policy | Cross-Site Scripting (XSS) |
| Strict-Transport-Security | Downgrade Attack (HTTPS → HTTP) |
| X-Frame-Options | Clickjacking |
| X-Content-Type-Options | MIME Sniffing |
| Referrer-Policy | Vazamento de informação via referer |

---

## 🛠️ Stack

- **Python 3.10+**
- **Streamlit** — interface web
- **Requests** — chamadas HTTP
- **SSL / Socket** — validação de certificado (lib nativa)
- **ReportLab** — geração de PDF

---

## 🚀 Como rodar localmente

### Pré-requisitos
- Python 3.10 ou superior
- pip

### Instalação

```bash
# Clone o repositório
git clone https://github.com/DavMarinho/securecheck.git
cd securecheck

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
streamlit run app.py
```

A aplicação abrirá em `http://localhost:8501`.

---

## 📖 Como usar

1. Acesse a aplicação no navegador
2. Cole a URL do site a ser auditado (ex: `google.com`)
3. Clique em **Analisar**
4. Visualize o resultado de cada verificação
5. Baixe o relatório PDF completo

---

## 📂 Estrutura do projeto

```
securecheck/
├── app.py              # Interface Streamlit
├── scanner.py          # Lógica de verificação de segurança
├── report.py           # Geração do relatório PDF
├── requirements.txt    # Dependências
└── README.md
```

---

## 🧠 Conceitos aplicados

- **Cybersecurity:** Headers de segurança HTTP, OWASP Best Practices, TLS/SSL
- **Python:** Bibliotecas nativas (socket, ssl), tratamento de exceções, modularização
- **Engenharia de Software:** Separação de responsabilidades (scanner / report / UI)
- **UX:** Visualização clara com sistema semafórico (✅ ⚠️ ❌)

---

## 🌐 Demo

> 🔗 [Acesse a aplicação ao vivo](#) *(adicione o link do Streamlit Cloud após o deploy)*

---

## 📌 Próximas evoluções

- [ ] Verificação de cookies (HttpOnly, Secure, SameSite)
- [ ] Análise de redirecionamento HTTP → HTTPS
- [ ] Detecção de tecnologias usadas (versões expostas)
- [ ] Histórico de auditorias por URL
- [ ] Versão API REST com FastAPI

---

## 👤 Autor

**Davi Marinho**

- 🐙 GitHub: [@DavMarinho](https://github.com/DavMarinho)
- 💼 LinkedIn: [davi-marinho-476958223](https://linkedin.com/in/davi-marinho-476958223)
- 📍 São Paulo, SP

---

## 📜 Licença

Distribuído sob licença MIT. Veja `LICENSE` para mais informações.