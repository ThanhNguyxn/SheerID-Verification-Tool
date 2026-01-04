# 🔐 SheerID Verifizierungs-Tool

[![GitHub Stars](https://img.shields.io/github/stars/ThanhNguyxn/SheerID-Verification-Tool?style=social)](https://github.com/ThanhNguyxn/SheerID-Verification-Tool/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

Eine umfassende Sammlung von Tools zur Automatisierung von SheerID-Verifizierungs-Workflows für verschiedene Dienste (Spotify, YouTube, Google One usw.).

---

## 🛠️ Verfügbare Tools

| Tool | Typ | Ziel | Beschreibung |
|------|------|--------|-------------|
| [spotify-verify-tool](../spotify-verify-tool/) | 🎵 Student | Spotify Premium | Studentenverifizierung (Universität) |
| [youtube-verify-tool](../youtube-verify-tool/) | 🎬 Student | YouTube Premium | Studentenverifizierung (Universität) |
| [one-verify-tool](../one-verify-tool/) | 🤖 Student | Gemini Advanced | Google One AI Premium Verifizierung |
| [boltnew-verify-tool](../boltnew-verify-tool/) | 👨‍🏫 Lehrer | Bolt.new | Lehrerverifizierung (Universität) |
| [k12-verify-tool](../k12-verify-tool/) | 🏫 K12 | ChatGPT Plus | K12 Lehrerverifizierung (High School) |
| [veterans-verify-tool](../veterans-verify-tool/) | 🎖️ Militär | Allgemein | Militärstatus-Verifizierung |
| [veterans-extension](../veterans-extension/) | 🧩 Chrome | Browser | Chrome-Erweiterung für Militärverifizierung |

### 🔗 Externe Tools

| Tool | Typ | Beschreibung |
|------|------|-------------|
| [SheerID VIP Bot](https://t.me/SheerID_VIP_Bot?start=ref_REF001124) | ⚡ Bot | Alternativer Telegram-Bot mit schnellerer Verarbeitung |
| [SheerID VN Bot](https://t.me/sheeridvn_bot?start=invite_7762497789) | 🇻🇳 Bot | Telegram-Bot der vietnamesischen Community |
| [Veterans Verify Bot](https://t.me/vgptplusbot?start=ref_7762497789) | 🎖️ Bot | Militär-Verifizierungs-Bot |
| [Batch 1Key.me](https://batch.1key.me/) | 📦 Web | Batch-Verifizierung für mehrere URLs |
| [Student Card Generator](https://thanhnguyxn.github.io/student-card-generator/) | 🎓 Tool | Erstellen von Studentenausweisen für manuelle Verifizierung |
| [Payslip Generator](https://thanhnguyxn.github.io/payslip-generator/) | 💰 Tool | Erstellen von Gehaltsabrechnungen für Lehrerverifizierung |
| [RoxyBrowser](https://roxybrowser.com?code=01045PFA) | 🦊 Browser | **Anti-Erkennungs-Browser** — Mehrere verifizierte Konten ohne Sperrung verwalten |

---

## 🧠 Kernarchitektur & Logik

Alle Python-Tools in diesem Repository teilen eine gemeinsame, optimierte Architektur, die für hohe Erfolgsraten ausgelegt ist.

### 1. Der Verifizierungsablauf (The Verification Flow)
Die Tools folgen einem standardisierten "Wasserfall"-Prozess:
1.  **Datenerzeugung (Data Generation)**: Erstellt eine realistische Identität (Name, Geburtsdatum, E-Mail), die zur Zielgruppe passt.
2.  **Übermittlung (`collectStudentPersonalInfo`)**: Sendet Daten an die SheerID API.
3.  **SSO Überspringen (`DELETE /step/sso`)**: Entscheidender Schritt. Umgeht die Anforderung, sich bei einem Schulportal anzumelden.
4.  **Dokumenten-Upload (`docUpload`)**: Lädt ein generiertes Nachweisdokument hoch (Studentenausweis, Transkript oder Lehrerausweis).
5.  **Abschluss (`completeDocUpload`)**: Signalisert SheerID, dass der Upload abgeschlossen ist.

### 2. Intelligente Strategien (Intelligent Strategies)

#### 🎓 Universitätsstrategie (Spotify, YouTube, Gemini)
- **Gewichtete Auswahl**: Verwendet eine kuratierte Liste von **45+ Universitäten** (USA, VN, JP, KR usw.).
- **Erfolgsverfolgung**: Universitäten mit höheren Erfolgsraten werden häufiger ausgewählt.
- **Dokumentenerzeugung**: Generiert realistisch aussehende Studentenausweise mit dynamischen Namen und Daten.

#### 👨‍🏫 Lehrerstrategie (Bolt.new)
- **Alterszielgruppen**: Generiert ältere Identitäten (25-55 Jahre), um der Lehrerdemografie zu entsprechen.
- **Dokumentenerzeugung**: Erstellt "Beschäftigungsnachweise" anstelle von Studentenausweisen.
- **Endpunkt**: Zielt auf `collectTeacherPersonalInfo` anstelle von Studenten-Endpunkten ab.

#### 🏫 K12 Strategie (ChatGPT Plus)
- **Schultyp-Targeting**: Zielt speziell auf Schulen mit `type: "K12"` (nicht `HIGH_SCHOOL`) ab.
- **Auto-Pass-Logik**: K12-Verifizierung wird oft **automatisch genehmigt**, ohne Dokumenten-Upload, wenn Schul- und Lehrerinformationen übereinstimmen.
- **Fallback**: Wenn ein Upload erforderlich ist, wird ein Lehrerausweis generiert.

#### 🎖️ Veteranenstrategie (ChatGPT Plus)
- **Strenge Berechtigung**: Zielt auf aktives Militärpersonal oder Veteranen ab, die innerhalb der **letzten 12 Monate** ausgeschieden sind.
- **Autoritative Prüfung**: SheerID verifiziert gegen die DoD/DEERS-Datenbank.
- **Logik**: Verwendet standardmäßig aktuelle Entlassungsdaten, um die Chancen auf automatische Genehmigung zu maximieren.

---

## 📋 Schnellstart

### Voraussetzungen
- Python 3.8+
- `pip`

### Installation

1.  **Repository klonen:**
    ```bash
    git clone https://github.com/ThanhNguyxn/SheerID-Verification-Tool.git
    cd SheerID-Verification-Tool
    ```

2.  **Abhängigkeiten installieren:**
    ```bash
    pip install httpx Pillow
    ```

3.  **Tool ausführen (z.B. Spotify):**
    ```bash
    cd spotify-verify-tool
    python main.py "YOUR_SHEERID_URL"
    ```

---

## ⚠️ Haftungsausschluss

Dieses Projekt dient nur zu **Bildungszwecken**. Die Tools zeigen, wie Verifizierungssysteme funktionieren und wie sie getestet werden können.
- Nicht für betrügerische Zwecke verwenden.
- Die Autoren sind nicht verantwortlich für Missbrauch.
- Beachten Sie die Nutzungsbedingungen aller Plattformen.

---

## 🤝 Mitwirken

Beiträge sind willkommen! Bitte zögern Sie nicht, einen Pull Request einzureichen.

---

## 🦊 Offizieller Partner: RoxyBrowser

🛡 **Anti-Erkennungs-Schutz** — Einzigartiger Fingerabdruck für jedes Konto, sieht aus wie verschiedene echte Geräte.

📉 **Verknüpfung Verhindern** — Verhindert, dass SheerID und Plattformen Ihre Konten verknüpfen.

🚀 **Ideal für Großnutzer** — Verwalten Sie sicher hunderte verifizierte Konten.

[![Kostenlos Testen](https://img.shields.io/badge/Kostenlos%20Testen-RoxyBrowser-ff6b35?style=for-the-badge&logo=googlechrome&logoColor=white)](https://roxybrowser.com?code=01045PFA)

---

## ❤️ Unterstützung

Wenn Sie dieses Projekt hilfreich finden, erwägen Sie bitte, mich zu unterstützen:

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-ea4aaa?style=for-the-badge&logo=github)](https://github.com/sponsors/ThanhNguyxn)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/thanhnguyxn)

---

## 🌐 Sprachen

| 🇺🇸 [English](../README.md) | 🇻🇳 [Tiếng Việt](./README.vi.md) | 🇨🇳 [中文](./README.zh.md) | 🇯🇵 [日本語](./README.ja.md) | 🇰🇷 [한국어](./README.ko.md) |
|:---:|:---:|:---:|:---:|:---:|
| 🇪🇸 [Español](./README.es.md) | 🇫🇷 [Français](./README.fr.md) | 🇩🇪 [Deutsch](./README.de.md) | 🇧🇷 [Português](./README.pt-BR.md) | 🇷🇺 [Русский](./README.ru.md) |
| 🇸🇦 [العربية](./README.ar.md) | 🇮🇳 [हिन्दी](./README.hi.md) | 🇹🇭 [ไทย](./README.th.md) | 🇹🇷 [Türkçe](./README.tr.md) | 🇵🇱 [Polski](./README.pl.md) |
| 🇮🇹 [Italiano](./README.it.md) | 🇮🇩 [Bahasa Indonesia](./README.id.md) | | | |
