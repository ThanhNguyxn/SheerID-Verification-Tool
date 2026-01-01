# 🔐 Strumento di Verifica SheerID

[![GitHub Stars](https://img.shields.io/github/stars/ThanhNguyxn/SheerID-Verification-Tool?style=social)](https://github.com/ThanhNguyxn/SheerID-Verification-Tool/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

Una raccolta completa di strumenti per automatizzare i flussi di lavoro di verifica SheerID per vari servizi (Spotify, YouTube, Google One, ecc.).

---

## 🛠️ Strumenti Disponibili

| Strumento | Tipo | Obiettivo | Descrizione |
|------|------|--------|-------------|
| [spotify-verify-tool](../spotify-verify-tool/) | 🎵 Studente | Spotify Premium | Verifica studente universitario |
| [youtube-verify-tool](../youtube-verify-tool/) | 🎬 Studente | YouTube Premium | Verifica studente universitario |
| [one-verify-tool](../one-verify-tool/) | 🤖 Studente | Gemini Advanced | Verifica Google One AI Premium |
| [boltnew-verify-tool](../boltnew-verify-tool/) | 👨‍🏫 Insegnante | Bolt.new | Verifica insegnante (Università) |
| [k12-verify-tool](../k12-verify-tool/) | 🏫 K12 | ChatGPT Plus | Verifica insegnante K12 (Scuola Superiore) |
| [veterans-verify-tool](../veterans-verify-tool/) | 🎖️ Militare | Generale | Verifica stato militare |
| [veterans-extension](../veterans-extension/) | 🧩 Chrome | Browser | Estensione Chrome per verifica militare |

### 🔗 Strumenti Esterni

| Strumento | Tipo | Descrizione |
|------|------|-------------|
| [SheerID VIP Bot](https://t.me/SheerID_VIP_Bot?start=ref_REF001124) | ⚡ Bot | Bot Telegram alternativo con elaborazione più veloce |
| [SheerID VN Bot](https://t.me/sheeridvn_bot?start=invite_7762497789) | 🇻🇳 Bot | Bot Telegram della comunità vietnamita |
| [Veterans Verify Bot](https://t.me/vgptplusbot?start=ref_7762497789) | 🎖️ Bot | Bot di verifica militare |
| [Batch 1Key.me](https://batch.1key.me/) | 📦 Web | Verifica in batch per più URL |
| [Student Card Generator](https://thanhnguyxn.github.io/student-card-generator/) | 🎓 Tool | Crea tessere studentesche per la verifica manuale |
| [Payslip Generator](https://thanhnguyxn.github.io/payslip-generator/) | 💰 Tool | Genera buste paga per la verifica degli insegnanti |

---

## 🧠 Architettura e Logica Principale

Tutti gli strumenti Python in questo repository condividono un'architettura comune ottimizzata per alti tassi di successo.

### 1. Il Flusso di Verifica (The Verification Flow)
Gli strumenti seguono un processo standardizzato a "Cascata":
1.  **Generazione Dati (Data Generation)**: Crea un'identità realistica (Nome, Data di nascita, Email) corrispondente alla demografia target.
2.  **Invio (`collectStudentPersonalInfo`)**: Invia i dati all'API SheerID.
3.  **Salta SSO (`DELETE /step/sso`)**: Passaggio cruciale. Bypassa il requisito di accedere a un portale scolastico.
4.  **Caricamento Documento (`docUpload`)**: Carica un documento di prova generato (Tessera Studente, Trascrizione o Badge Insegnante).
5.  **Completamento (`completeDocUpload`)**: Segnala a SheerID che il caricamento è terminato.

### 2. Strategie Intelligenti (Intelligent Strategies)

#### 🎓 Strategia Universitaria (Spotify, YouTube, Gemini)
- **Selezione Ponderata**: Utilizza un elenco curato di **45+ Università** (USA, VN, JP, KR, ecc.).
- **Tracciamento Successo**: Le università con tassi di successo più elevati vengono selezionate più spesso.
- **Generazione Documenti**: Genera tessere studentesche realistiche con nomi e date dinamici.

#### 👨‍🏫 Strategia Insegnante (Bolt.new)
- **Targeting per Età**: Genera identità più anziane (25-55 anni) per corrispondere alla demografia degli insegnanti.
- **Generazione Documenti**: Crea "Certificati di Impiego" invece di tessere studentesche.
- **Endpoint**: Target `collectTeacherPersonalInfo` invece degli endpoint studenti.

#### 🏫 Strategia K12 (ChatGPT Plus)
- **Targeting Tipo Scuola**: Target specifico scuole con `type: "K12"` (non `HIGH_SCHOOL`).
- **Logica Auto-Pass**: La verifica K12 viene spesso **approvata automaticamente** senza caricamento documenti se le informazioni della scuola e dell'insegnante corrispondono.
- **Fallback**: Se è richiesto il caricamento, genera un Badge Insegnante.

#### 🎖️ Strategia Veterani (ChatGPT Plus)
- **Idoneità Rigorosa**: Target personale militare in servizio attivo o veterani congedati negli **ultimi 12 mesi**.
- **Controllo Autorevole**: SheerID verifica rispetto al database DoD/DEERS.
- **Logica**: Utilizza date di congedo recenti per impostazione predefinita per massimizzare le possibilità di approvazione automatica.

---

## 📋 Avvio Rapido

### Prerequisiti
- Python 3.8+
- `pip`

### Installazione

1.  **Clonare il repository:**
    ```bash
    git clone https://github.com/ThanhNguyxn/SheerID-Verification-Tool.git
    cd SheerID-Verification-Tool
    ```

2.  **Installare le dipendenze:**
    ```bash
    pip install httpx Pillow
    ```

3.  **Eseguire uno strumento (es. Spotify):**
    ```bash
    cd spotify-verify-tool
    python main.py "YOUR_SHEERID_URL"
    ```

---

## ⚠️ Disclaimer

Questo progetto è solo a **scopo educativo**. Gli strumenti dimostrano come funzionano i sistemi di verifica e come possono essere testati.
- Non utilizzare per scopi fraudolenti.
- Gli autori non sono responsabili per qualsiasi uso improprio.
- Rispettare i Termini di Servizio di tutte le piattaforme.

---

## 🤝 Contribuire

I contributi sono benvenuti! Sentiti libero di inviare una Pull Request.
