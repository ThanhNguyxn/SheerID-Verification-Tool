# 🔐 Ferramenta de Verificação SheerID

[![GitHub Stars](https://img.shields.io/github/stars/ThanhNguyxn/SheerID-Verification-Tool?style=social)](https://github.com/ThanhNguyxn/SheerID-Verification-Tool/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

Uma coleção abrangente de ferramentas para automatizar fluxos de trabalho de verificação SheerID para vários serviços (Spotify, YouTube, Google One, etc.).

---

## 🛠️ Ferramentas Disponíveis

| Ferramenta | Tipo | Alvo | Descrição |
|------|------|--------|-------------|
| [spotify-verify-tool](../spotify-verify-tool/) | 🎵 Estudante | Spotify Premium | Verificação de estudante universitário |
| [youtube-verify-tool](../youtube-verify-tool/) | 🎬 Estudante | YouTube Premium | Verificação de estudante universitário |
| [one-verify-tool](../one-verify-tool/) | 🤖 Estudante | Gemini Advanced | Verificação Google One AI Premium |
| [boltnew-verify-tool](../boltnew-verify-tool/) | 👨‍🏫 Professor | Bolt.new | Verificação de professor (Universidade) |
| [k12-verify-tool](../k12-verify-tool/) | 🏫 K12 | ChatGPT Plus | Verificação de professor K12 (Ensino Médio) |
| [veterans-verify-tool](../veterans-verify-tool/) | 🎖️ Militar | Geral | Verificação de status militar |
| [veterans-extension](../veterans-extension/) | 🧩 Chrome | Navegador | Extensão do Chrome para verificação militar |

### 🔗 Ferramentas Externas

| Ferramenta | Tipo | Descrição |
|------|------|-------------|
| [RoxyBrowser](https://roxybrowser.com?code=01045PFA) | 🦊 Browser | **Navegador anti-detecção** — Gerencie múltiplas contas verificadas sem ser banido |
| [SheerID Auto Verify](https://ip123.in/sheerid/?code=01045PFA) | 🔐 Web | **Ferramenta de verificação automática** — Verificação SheerID rápida e automática |
| [SheerID Verification Bot](https://t.me/SheerID_Verification_bot?start=ref_LdPKPES3Ej) | 🤖 Bot | Bot do Telegram da comunidade vietnamita |
| [Auto SheerID Bot](https://t.me/auto_sheerid_bot?start=7762497789) | 🤖 Bot | Bot de verificação automatizado |
| [Student Card Generator](https://thanhnguyxn.github.io/student-card-generator/) | 🎓 Tool | Criar carteiras de estudante para verificação manual |
| [Payslip Generator](https://thanhnguyxn.github.io/payslip-generator/) | 💰 Tool | Gerar contracheques para verificação de professores |

---

## 🧠 Arquitetura e Lógica Principal

Todas as ferramentas Python neste repositório compartilham uma arquitetura comum otimizada para altas taxas de sucesso.

### 1. O Fluxo de Verificação (The Verification Flow)
As ferramentas seguem um processo padronizado de "Cascata" (Waterfall):
1.  **Geração de Dados (Data Generation)**: Cria uma identidade realista (Nome, Data de Nascimento, Email) correspondente à demografia alvo.
2.  **Envio (`collectStudentPersonalInfo`)**: Envia dados para a API SheerID.
3.  **Pular SSO (`DELETE /step/sso`)**: Passo crucial. Ignora a exigência de fazer login em um portal escolar.
4.  **Upload de Documento (`docUpload`)**: Faz upload de um documento de prova gerado (Carteira de Estudante, Histórico Escolar ou Crachá de Professor).
5.  **Conclusão (`completeDocUpload`)**: Sinaliza para a SheerID que o upload foi concluído.

### 2. Estratégias Inteligentes (Intelligent Strategies)

#### 🎓 Estratégia Universitária (Spotify, YouTube, Gemini)
- **Seleção Ponderada**: Usa uma lista curada de **45+ Universidades** (EUA, VN, JP, KR, etc.).
- **Rastreamento de Sucesso**: Universidades com taxas de sucesso mais altas são selecionadas com mais frequência.
- **Geração de Documentos**: Gera carteiras de estudante realistas com nomes e datas dinâmicos.

#### 👨‍🏫 Estratégia de Professor (Bolt.new)
- **Segmentação por Idade**: Gera identidades mais velhas (25-55 anos) para corresponder à demografia dos professores.
- **Geração de Documentos**: Cria "Certificados de Emprego" em vez de carteiras de estudante.
- **Endpoint**: Alvo `collectTeacherPersonalInfo` em vez de endpoints de estudante.

#### 🏫 Estratégia K12 (ChatGPT Plus)
- **Segmentação por Tipo de Escola**: Alvo especificamente escolas com `type: "K12"` (não `HIGH_SCHOOL`).
- **Lógica de Aprovação Automática (Auto-Pass)**: A verificação K12 é frequentemente **aprovada automaticamente** sem upload de documento se as informações da escola e do professor corresponderem.
- **Fallback**: Se o upload for necessário, gera um Crachá de Professor.

#### 🎖️ Estratégia de Veteranos (ChatGPT Plus)
- **Elegibilidade Estrita**: Alvo militares da ativa ou veteranos dispensados nos **últimos 12 meses**.
- **Verificação Autorizada**: A SheerID verifica no banco de dados DoD/DEERS.
- **Lógica**: Usa datas de dispensa recentes por padrão para maximizar as chances de aprovação automática.

---

## 📋 Início Rápido

### Pré-requisitos
- Python 3.8+
- `pip`

### Instalação

1.  **Clonar o repositório:**
    ```bash
    git clone https://github.com/ThanhNguyxn/SheerID-Verification-Tool.git
    cd SheerID-Verification-Tool
    ```

2.  **Instalar dependências:**
    ```bash
    pip install httpx Pillow
    ```

3.  **Executar uma ferramenta (ex: Spotify):**
    ```bash
    cd spotify-verify-tool
    python main.py "YOUR_SHEERID_URL"
    ```

---

## ⚠️ Isenção de Responsabilidade

Este projeto é apenas para **fins educacionais**. As ferramentas demonstram como os sistemas de verificação funcionam e como podem ser testados.
- Não use para fins fraudulentos.
- Os autores não são responsáveis por qualquer uso indevido.
- Respeite os Termos de Serviço de todas as plataformas.

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para enviar um Pull Request.

---

## 🦊 Parceiro Oficial: RoxyBrowser

🛡 **Proteção Anti-Detecção** — Impressão digital única para cada conta, parece dispositivos reais diferentes.

📉 **Prevenir Vinculação** — Impede que SheerID e plataformas vinculem suas contas.

🚀 **Ideal para Usuários em Massa** — Gerencie com segurança centenas de contas verificadas.

[![Teste Grátis](https://img.shields.io/badge/Teste%20Grátis-RoxyBrowser-ff6b35?style=for-the-badge&logo=googlechrome&logoColor=white)](https://roxybrowser.com?code=01045PFA)

---

## ❤️ Apoio

Se você achar este projeto útil, considere me apoiar:

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-ea4aaa?style=for-the-badge&logo=github)](https://github.com/sponsors/ThanhNguyxn)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/thanhnguyxn)

---

## 🌐 Idiomas

| 🇺🇸 [English](../README.md) | 🇻🇳 [Tiếng Việt](./README.vi.md) | 🇨🇳 [中文](./README.zh.md) | 🇯🇵 [日本語](./README.ja.md) | 🇰🇷 [한국어](./README.ko.md) |
|:---:|:---:|:---:|:---:|:---:|
| 🇪🇸 [Español](./README.es.md) | 🇫🇷 [Français](./README.fr.md) | 🇩🇪 [Deutsch](./README.de.md) | 🇧🇷 [Português](./README.pt-BR.md) | 🇷🇺 [Русский](./README.ru.md) |
| 🇸🇦 [العربية](./README.ar.md) | 🇮🇳 [हिन्दी](./README.hi.md) | 🇹🇭 [ไทย](./README.th.md) | 🇹🇷 [Türkçe](./README.tr.md) | 🇵🇱 [Polski](./README.pl.md) |
| 🇮🇹 [Italiano](./README.it.md) | 🇮🇩 [Bahasa Indonesia](./README.id.md) | | | |
