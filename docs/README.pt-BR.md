# 🔐 Ferramenta de Verificação SheerID

[![GitHub Stars](https://img.shields.io/github/stars/ThanhNguyxn/SheerID-Verification-Tool?style=social)](https://github.com/ThanhNguyxn/SheerID-Verification-Tool/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Documentation](https://img.shields.io/badge/Docs-Website-2ea44f?style=flat&logo=github&logoColor=white)](https://thanhnguyxn.github.io/SheerID-Verification-Tool/)

Uma coleção abrangente de ferramentas para automatizar fluxos de trabalho de verificação SheerID para vários serviços (Spotify, YouTube, Google One, etc.).

---

## 🛠️ Ferramentas Disponíveis

| Ferramenta | Tipo | Alvo | Descrição |
|------|------|--------|-------------|
| [spotify-verify-tool](../spotify-verify-tool/) | 🎵 Estudante | Spotify Premium | Verificação de estudantes universitários |
| [youtube-verify-tool](../youtube-verify-tool/) | 🎬 Estudante | YouTube Premium | Verificação de estudantes universitários |
| [one-verify-tool](../one-verify-tool/) | 🤖 Estudante | Gemini Advanced | Verificação Google One AI Premium |
| [boltnew-verify-tool](../boltnew-verify-tool/) | 👨‍🏫 Professor | Bolt.new | Verificação de professores (Universidade) |
| [canva-teacher-tool](../canva-teacher-tool/) | 🇬🇧 Professor | Canva Education | Verificação de professores do Reino Unido (K-12) |
| [k12-verify-tool](../k12-verify-tool/) | 🏫 K12 | ChatGPT Plus | Verificação de professores K12 (Ensino Médio) |
| [veterans-verify-tool](../veterans-verify-tool/) | 🎖️ Militar | Geral | Verificação de status militar |
| [veterans-extension](../veterans-extension/) | 🧩 Chrome | Navegador | Extensão Chrome para verificação militar |

### 🔗 Ferramentas Externas

| Ferramenta | Tipo | Descrição |
|------|------|-------------|
| [RoxyBrowser](https://roxybrowser.com?code=01045PFA) | 🦊 Navegador | **Navegador anti-detecção** — Gerencie múltiplas contas verificadas sem ser banido |
| [Check IP](https://ip123.in/en?code=01045PFA) | 🌐 Web | **Verificar IP** — Verifique seu endereço IP e status do proxy |
| [SheerID Verification Bot](https://t.me/SheerID_Verification_bot?start=ref_LdPKPES3Ej) | 🤖 Bot | Bot do Telegram de verificação automatizada |
| [GPT Bot](https://t.me/vgptplusbot?start=ref_7762497789) | 🤖 Bot | Bot de verificação automatizada |
| [Student Card Generator](https://thanhnguyxn.github.io/student-card-generator/) | 🎓 Ferramenta | Criar carteiras de estudante para verificação manual |
| [Payslip Generator](https://thanhnguyxn.github.io/payslip-generator/) | 💰 Ferramenta | Gerar contracheques para verificação de professores |

---

## 🧠 Arquitetura e Lógica Principal

Todas as ferramentas Python neste repositório compartilham uma arquitetura comum otimizada para altas taxas de sucesso.

### 1. O Fluxo de Verificação (The Verification Flow)
As ferramentas seguem um processo padronizado de "Cascata":
1.  **Geração de Dados (Data Generation)**: Cria uma identidade realista (Nome, Data de nascimento, Email) correspondente ao público-alvo.
2.  **Envio (`collectStudentPersonalInfo`)**: Envia dados para a API SheerID.
3.  **Pular SSO (`DELETE /step/sso`)**: Passo crucial. Ignora o requisito de fazer login em um portal escolar.
4.  **Upload de Documento (`docUpload`)**: Faz upload de um documento de prova gerado (ID de estudante, Histórico ou Crachá de professor).
5.  **Conclusão (`completeDocUpload`)**: Sinaliza ao SheerID que o upload foi concluído.

### 2. Estratégias Inteligentes (Intelligent Strategies)

#### 🎓 Estratégia Universitária (Spotify, YouTube, Gemini)
- **Seleção Ponderada**: Usa uma lista curada de **45+ Universidades** (EUA, VN, JP, KR, etc.).
- **Rastreamento de Sucesso**: Universidades com taxas de sucesso mais altas são selecionadas com mais frequência.
- **Geração de Documentos**: Gera carteiras de identificação de estudante realistas com nomes e datas dinâmicos.

#### 👨‍🏫 Estratégia de Professor (Bolt.new)
- **Segmentação por Idade**: Gera identidades mais velhas (25-55 anos) para corresponder à demografia dos professores.
- **Geração de Documentos**: Cria "Certificados de Emprego" em vez de IDs de estudante.
- **Endpoint**: Direciona para `collectTeacherPersonalInfo` em vez de endpoints de estudantes.

#### 🏫 Estratégia K12 (ChatGPT Plus)
- **Segmentação por Tipo de Escola**: Direciona especificamente para escolas com `type: "K12"` (não `HIGH_SCHOOL`).
- **Lógica de Auto-Aprovação (Auto-Pass)**: A verificação K12 geralmente é **automaticamente aprovada** sem upload de documentos se as informações da escola e do professor corresponderem.
- **Fallback**: Se o upload for necessário, gera um Crachá de Professor.

#### 🎖️ Estratégia de Veteranos (ChatGPT Plus)
- **Elegibilidade Estrita**: Direciona para militares da ativa ou veteranos separados nos **últimos 12 meses**.
- **Verificação Oficial**: SheerID verifica contra o banco de dados DoD/DEERS.
- **Lógica**: Usa por padrão datas de baixa recentes para maximizar as chances de auto-aprovação.

#### 🛡️ Módulo Anti-Detecção
Todas as ferramentas agora incluem `anti_detect.py` que fornece:
- **User-Agents Aleatórios**: 10+ strings UA de navegadores reais (Chrome, Firefox, Edge, Safari)
- **Headers Tipo Navegador**: `sec-ch-ua`, `Accept-Language` apropriados, etc.
- **Spoofing de Impressão Digital TLS**: Usa `curl_cffi` para imitar a impressão digital JA3/JA4 do Chrome
- **Atrasos Aleatórios**: Temporização de distribuição gamma para imitar comportamento humano
- **Sessão Inteligente**: Seleciona automaticamente a melhor biblioteca HTTP disponível (curl_cffi > cloudscraper > httpx > requests)
- **Headers NewRelic**: Headers de rastreamento necessários para chamadas da API SheerID
- **Aquecimento de Sessão**: Requisições pré-verificação para estabelecer uma sessão de navegador legítima
- **Geração de Email**: Cria emails de estudantes realistas correspondentes aos domínios universitários
- **Correspondência Geográfica de Proxy**: Corresponde a localização do proxy ao país da universidade para consistência
- **Imitação Multi-Navegador**: Alterna entre impressões digitais Chrome, Edge e Safari

#### 📄 Módulo de Geração de Documentos
O novo `doc_generator.py` fornece anti-detecção para documentos gerados:
- **Injeção de Ruído**: Ruído de pixels aleatório para evitar detecção de templates
- **Variação de Cor**: 6 esquemas de cores diferentes para unicidade
- **Posicionamento Dinâmico**: Variação de ±3px nas posições dos elementos
- **Múltiplos Tipos**: ID de Estudante, Histórico, Crachá de Professor
- **Detalhes Realistas**: Códigos de barras, códigos QR, notas de cursos aleatórios

> [!WARNING]
> **Ferramentas Baseadas em API Têm Limitações Inerentes**
>
> SheerID usa detecção avançada incluindo:
> - **Impressão Digital TLS**: Python `requests`/`httpx` têm assinaturas detectáveis
> - **Inteligência de Sinais**: Endereço IP, atributos do dispositivo, análise de idade do email
> - **Revisão de Documentos por IA**: Detecta documentos falsificados/de template
>
> Para melhores resultados: Use **proxies residenciais** + instale `curl_cffi` para spoofing TLS.
> Extensões de navegador geralmente têm taxas de sucesso mais altas que ferramentas API.

> [!IMPORTANT]
> **Gemini/Google One é APENAS EUA (desde janeiro 2026)**
>
> O `one-verify-tool` só funciona com IPs dos EUA. Usuários internacionais verão falhas de verificação.

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

3.  **[Opcional] Anti-Detecção Aprimorada:**
    ```bash
    pip install curl_cffi cloudscraper
    ```
    - `curl_cffi`: Falsifica impressão digital TLS (JA3/JA4) para parecer Chrome real
    - `cloudscraper`: Bypassa proteção Cloudflare

4.  **Executar uma ferramenta (ex: Spotify):**
    ```bash
    cd spotify-verify-tool
    python main.py "YOUR_SHEERID_URL"
    ```

---

## 🦊 Parceiro Oficial: RoxyBrowser

🛡 **Proteção Anti-Detecção** — Impressão digital única para cada conta, parecem dispositivos reais diferentes.

📉 **Prevenir Vinculação** — Impede que SheerID e plataformas vinculem suas contas.

🚀 **Ideal para Usuários em Massa** — Gerencie com segurança centenas de contas verificadas.

[![Teste Grátis](https://img.shields.io/badge/Teste%20Grátis-RoxyBrowser-ff6b35?style=for-the-badge&logo=googlechrome&logoColor=white)](https://roxybrowser.com?code=01045PFA)

---

## ⚠️ Aviso Legal

Este projeto é apenas para **fins educacionais**. As ferramentas demonstram como os sistemas de verificação funcionam e como podem ser testados.
- Não use para fins fraudulentos.
- Os autores não são responsáveis por qualquer uso indevido.
- Respeite os Termos de Serviço de todas as plataformas.

---

## 🤝 Contribuir

Contribuições são bem-vindas! Sinta-se à vontade para enviar um Pull Request.

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
