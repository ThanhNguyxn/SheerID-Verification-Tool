# 🔐 SheerID Verifizierungs-Tool

[![GitHub Stars](https://img.shields.io/github/stars/ThanhNguyxn/SheerID-Verification-Tool?style=social)](https://github.com/ThanhNguyxn/SheerID-Verification-Tool/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Documentation](https://img.shields.io/badge/Docs-Website-2ea44f?style=flat&logo=github&logoColor=white)](https://thanhnguyxn.github.io/SheerID-Verification-Tool/)

Eine umfassende Sammlung von Tools zur Automatisierung von SheerID-Verifizierungs-Workflows für verschiedene Dienste (Spotify, YouTube, Google One usw.).

---

## 🛠️ Verfügbare Tools

| Tool | Typ | Ziel | Beschreibung |
|------|------|--------|-------------|
| [spotify-verify-tool](../spotify-verify-tool/) | 🎵 Student | Spotify Premium | Studentenverifizierung (Universität) |
| [youtube-verify-tool](../youtube-verify-tool/) | 🎬 Student | YouTube Premium | Studentenverifizierung (Universität) |
| [one-verify-tool](../one-verify-tool/) | 🤖 Student | Gemini Advanced | Google One AI Premium Verifizierung |
| [boltnew-verify-tool](../boltnew-verify-tool/) | 👨‍🏫 Lehrer | Bolt.new | Lehrerverifizierung (Universität) |
| [canva-teacher-tool](../canva-teacher-tool/) | 🇬🇧 Lehrer | Canva Education | UK-Lehrerverifizierung (K-12) |
| [k12-verify-tool](../k12-verify-tool/) | 🏫 K12 | ChatGPT Plus | K12 Lehrerverifizierung (High School) |
| [veterans-verify-tool](../veterans-verify-tool/) | 🎖️ Militär | Allgemein | Militärstatus-Verifizierung |
| [veterans-extension](../veterans-extension/) | 🧩 Chrome | Browser | Chrome-Erweiterung für Militärverifizierung |

### 🔗 Externe Tools

| Tool | Typ | Beschreibung |
|------|------|-------------|
| [RoxyBrowser](https://roxybrowser.com?code=01045PFA) | 🦊 Browser | **Anti-Erkennungs-Browser** — Mehrere verifizierte Konten ohne Sperrung verwalten |
| [Check IP](https://ip123.in/en?code=01045PFA) | 🌐 Web | **IP prüfen** — Überprüfen Sie Ihre IP-Adresse und Proxy-Status |
| [SheerID Verification Bot](https://t.me/SheerID_Verification_bot?start=ref_LdPKPES3Ej) | 🤖 Bot | Automatisierter Telegram-Verifizierungsbot |
| [GPT Bot](https://t.me/vgptplusbot?start=ref_7762497789) | 🤖 Bot | Automatisierter Verifizierungs-Bot |
| [Student Card Generator](https://thanhnguyxn.github.io/student-card-generator/) | 🎓 Tool | Erstellen von Studentenausweisen für manuelle Verifizierung |
| [Payslip Generator](https://thanhnguyxn.github.io/payslip-generator/) | 💰 Tool | Erstellen von Gehaltsabrechnungen für Lehrerverifizierung |

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

#### 🛡️ Anti-Erkennungs-Modul
Alle Tools enthalten jetzt `anti_detect.py`, das Folgendes bietet:
- **Zufällige User-Agents**: 10+ echte Browser-UA-Strings (Chrome, Firefox, Edge, Safari)
- **Browser-ähnliche Header**: Korrekte `sec-ch-ua`, `Accept-Language`, usw.
- **TLS-Fingerabdruck-Spoofing**: Verwendet `curl_cffi` um Chromes JA3/JA4-Fingerabdruck zu imitieren
- **Zufällige Verzögerungen**: Gamma-Verteilungs-Timing zur Nachahmung menschlichen Verhaltens
- **Intelligente Sitzung**: Wählt automatisch die beste verfügbare HTTP-Bibliothek (curl_cffi > cloudscraper > httpx > requests)
- **NewRelic-Header**: Erforderliche Tracking-Header für SheerID API-Aufrufe
- **Sitzungsaufwärmung**: Vorab-Verifizierungsanfragen zur Etablierung einer legitimen Browser-Sitzung
- **E-Mail-Generierung**: Erstellt realistische Studenten-E-Mails, die zu Universitätsdomains passen
- **Proxy-Geo-Matching**: Passt den Proxy-Standort an das Land der Universität an für Konsistenz
- **Multi-Browser-Imitation**: Wechselt zwischen Chrome-, Edge- und Safari-Fingerabdrücken

#### 📄 Dokumentenerzeugungsmodul
Das neue `doc_generator.py` bietet Anti-Erkennung für generierte Dokumente:
- **Rauschinjektion**: Zufälliges Pixelrauschen zur Vermeidung von Vorlagenerkennung
- **Farbvariation**: 6 verschiedene Farbschemata für Einzigartigkeit
- **Dynamische Positionierung**: ±3px Varianz bei Elementpositionen
- **Mehrere Typen**: Studentenausweis, Transkript, Lehrerausweis
- **Realistische Details**: Zufällige Barcodes, QR-Codes, Kursnoten

> [!WARNING]
> **API-basierte Tools haben inhärente Einschränkungen**
>
> SheerID verwendet fortgeschrittene Erkennung einschließlich:
> - **TLS-Fingerabdruck**: Python `requests`/`httpx` haben erkennbare Signaturen
> - **Signalaufklärung**: IP-Adresse, Geräteattribute, E-Mail-Altersanalyse
> - **KI-Dokumentenprüfung**: Erkennt gefälschte/Vorlagen-Dokumente
>
> Für beste Ergebnisse: Verwenden Sie **Residential Proxies** + installieren Sie `curl_cffi` für TLS-Spoofing.
> Browser-Erweiterungen haben in der Regel höhere Erfolgsraten als API-Tools.

> [!IMPORTANT]
> **Gemini/Google One ist NUR US (seit Januar 2026)**
>
> Das `one-verify-tool` funktioniert nur mit US-IPs. Internationale Benutzer werden Verifizierungsfehler sehen.

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

3.  **[Optional] Verbesserte Anti-Erkennung:**
    ```bash
    pip install curl_cffi cloudscraper
    ```
    - `curl_cffi`: Spooft TLS-Fingerabdruck (JA3/JA4) um wie echtes Chrome auszusehen
    - `cloudscraper`: Umgeht Cloudflare-Schutz

4.  **Tool ausführen (z.B. Spotify):**
    ```bash
    cd spotify-verify-tool
    python main.py "YOUR_SHEERID_URL"
    ```

---

## 🦊 Offizieller Partner: RoxyBrowser

🛡 **Anti-Erkennungs-Schutz** — Einzigartiger Fingerabdruck für jedes Konto, sieht aus wie verschiedene echte Geräte.

📉 **Verknüpfung Verhindern** — Verhindert, dass SheerID und Plattformen Ihre Konten verknüpfen.

🚀 **Ideal für Großnutzer** — Verwalten Sie sicher hunderte verifizierte Konten.

[![Kostenlos Testen](https://img.shields.io/badge/Kostenlos%20Testen-RoxyBrowser-ff6b35?style=for-the-badge&logo=googlechrome&logoColor=white)](https://roxybrowser.com?code=01045PFA)

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
