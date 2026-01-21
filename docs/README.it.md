# 🔐 Strumento di Verifica SheerID

[![GitHub Stars](https://img.shields.io/github/stars/ThanhNguyxn/SheerID-Verification-Tool?style=social)](https://github.com/ThanhNguyxn/SheerID-Verification-Tool/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Documentation](https://img.shields.io/badge/Docs-Website-2ea44f?style=flat&logo=github&logoColor=white)](https://thanhnguyxn.github.io/SheerID-Verification-Tool/)

Una collezione completa di strumenti per automatizzare i workflow di verifica SheerID per vari servizi (Spotify, YouTube, Google One, ecc.).

---

## 🛠️ Strumenti Disponibili

| Strumento | Tipo | Target | Descrizione |
|------|------|--------|-------------|
| [spotify-verify-tool](../spotify-verify-tool/) | 🎵 Studente | Spotify Premium | Verifica studenti universitari |
| [youtube-verify-tool](../youtube-verify-tool/) | 🎬 Studente | YouTube Premium | Verifica studenti universitari |
| [one-verify-tool](../one-verify-tool/) | 🤖 Studente | Gemini Advanced | Verifica Google One AI Premium |
| [boltnew-verify-tool](../boltnew-verify-tool/) | 👨‍🏫 Insegnante | Bolt.new | Verifica insegnanti (Università) |
| [canva-teacher-tool](../canva-teacher-tool/) | 🇬🇧 Insegnante | Canva Education | Verifica insegnanti UK (K-12) |
| [k12-verify-tool](../k12-verify-tool/) | 🏫 K12 | ChatGPT Plus | Verifica insegnanti K12 |
| [veterans-verify-tool](../veterans-verify-tool/) | 🎖️ Militare | Generale | Verifica status militare |
| [veterans-extension](../veterans-extension/) | 🧩 Chrome | Browser | Estensione Chrome per verifica militare |

### 🔗 Strumenti Esterni

| Strumento | Tipo | Descrizione |
|------|------|-------------|
| [RoxyBrowser](https://roxybrowser.com?code=01045PFA) | 🦊 Browser | **Browser anti-rilevamento** — Gestisci più account verificati senza ban |
| [Check IP](https://ip123.in/en?code=01045PFA) | 🌐 Web | **Controlla IP** — Verifica il tuo indirizzo IP e stato proxy |
| [SheerID Verification Bot](https://t.me/SheerID_Verification_bot?start=ref_LdPKPES3Ej) | 🤖 Bot | Bot Telegram automatico |
| [GPT Bot](https://t.me/vgptplusbot?start=ref_7762497789) | 🤖 Bot | Bot di verifica automatico |
| [Student Card Generator](https://thanhnguyxn.github.io/student-card-generator/) | 🎓 Strumento | Creazione tessere studente |
| [Payslip Generator](https://thanhnguyxn.github.io/payslip-generator/) | 💰 Strumento | Generazione buste paga |

---

## 🧠 Architettura e Logica Core

Tutti gli strumenti Python in questo repository condividono un'architettura comune ottimizzata per alti tassi di successo.

### 1. Flusso di Verifica
1. **Generazione Dati**: Crea un'identità realistica
2. **Invio**: Invia dati all'API SheerID
3. **Bypass SSO**: Salta il requisito di login al portale scolastico
4. **Upload Documento**: Carica il documento di prova generato
5. **Completamento**: Segnala a SheerID che l'upload è completato

### 2. Strategie Intelligenti

#### 🎓 Strategia Universitaria (Spotify, YouTube, Gemini)
- Lista di **45+ Università**
- Università con tassi di successo più alti selezionate più frequentemente
- Genera tessere studente realistiche

#### 👨‍🏫 Strategia Insegnante (Bolt.new)
- Genera identità 25-55 anni
- Crea "Certificati di Impiego"

#### 🏫 Strategia K12 (ChatGPT Plus)
- Mira alle scuole `type: "K12"`
- Spesso approvato automaticamente

#### 🎖️ Strategia Veterani (ChatGPT Plus)
- Mira ai veterani congedati negli ultimi 12 mesi
- Verifica con database DoD/DEERS

#### 🛡️ Modulo Anti-Rilevamento
- User-Agents casuali (10+ browser reali)
- Spoofing impronta TLS (`curl_cffi`)
- Ritardi casuali
- Generazione email realistiche

#### 📄 Modulo Generazione Documenti
- Iniezione rumore pixel
- 6 schemi colore diversi
- Posizionamento dinamico ±3px

> [!WARNING]
> **Gli strumenti API hanno limitazioni intrinseche** — Usa proxy residenziali + `curl_cffi`.

> [!IMPORTANT]
> **Gemini/Google One SOLO USA (da gennaio 2026)**

---

## 📋 Avvio Rapido

```bash
git clone https://github.com/ThanhNguyxn/SheerID-Verification-Tool.git
cd SheerID-Verification-Tool
pip install httpx Pillow
pip install curl_cffi cloudscraper  # Opzionale
cd spotify-verify-tool
python main.py "YOUR_SHEERID_URL"
```

---

## 🦊 Partner Ufficiale: RoxyBrowser

[![Prova Gratis](https://img.shields.io/badge/Prova%20Gratis-RoxyBrowser-ff6b35?style=for-the-badge&logo=googlechrome&logoColor=white)](https://roxybrowser.com?code=01045PFA)

---

## ⚠️ Disclaimer

Questo progetto è solo per **scopi educativi**. Non utilizzare per scopi fraudolenti.

---

## ❤️ Supporto

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-ea4aaa?style=for-the-badge&logo=github)](https://github.com/sponsors/ThanhNguyxn)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/thanhnguyxn)

---

## 🌐 Lingue

| 🇺🇸 [English](../README.md) | 🇻🇳 [Tiếng Việt](./README.vi.md) | 🇨🇳 [中文](./README.zh.md) | 🇯🇵 [日本語](./README.ja.md) | 🇰🇷 [한국어](./README.ko.md) |
|:---:|:---:|:---:|:---:|:---:|
| 🇪🇸 [Español](./README.es.md) | 🇫🇷 [Français](./README.fr.md) | 🇩🇪 [Deutsch](./README.de.md) | 🇧🇷 [Português](./README.pt-BR.md) | 🇷🇺 [Русский](./README.ru.md) |
| 🇸🇦 [العربية](./README.ar.md) | 🇮🇳 [हिन्दी](./README.hi.md) | 🇹🇭 [ไทย](./README.th.md) | 🇹🇷 [Türkçe](./README.tr.md) | 🇵🇱 [Polski](./README.pl.md) |
| 🇮🇹 [Italiano](./README.it.md) | 🇮🇩 [Bahasa Indonesia](./README.id.md) | | | |
