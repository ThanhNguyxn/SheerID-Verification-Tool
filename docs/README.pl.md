# 🔐 Narzędzie Weryfikacji SheerID

[![GitHub Stars](https://img.shields.io/github/stars/ThanhNguyxn/SheerID-Verification-Tool?style=social)](https://github.com/ThanhNguyxn/SheerID-Verification-Tool/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

Kompleksowy zestaw narzędzi do automatyzacji przepływów pracy weryfikacji SheerID dla różnych usług (Spotify, YouTube, Google One itp.).

---

## 🛠️ Dostępne Narzędzia

| Narzędzie | Typ | Cel | Opis |
|------|------|--------|-------------|
| [spotify-verify-tool](../spotify-verify-tool/) | 🎵 Student | Spotify Premium | Weryfikacja studenta uniwersytetu |
| [youtube-verify-tool](../youtube-verify-tool/) | 🎬 Student | YouTube Premium | Weryfikacja studenta uniwersytetu |
| [one-verify-tool](../one-verify-tool/) | 🤖 Student | Gemini Advanced | Weryfikacja Google One AI Premium |
| [boltnew-verify-tool](../boltnew-verify-tool/) | 👨‍🏫 Nauczyciel | Bolt.new | Weryfikacja nauczyciela (Uniwersytet) |
| [k12-verify-tool](../k12-verify-tool/) | 🏫 K12 | ChatGPT Plus | Weryfikacja nauczyciela K12 (Szkoła średnia) |
| [veterans-verify-tool](../veterans-verify-tool/) | 🎖️ Wojsko | Ogólne | Weryfikacja statusu wojskowego |
| [veterans-extension](../veterans-extension/) | 🧩 Chrome | Przeglądarka | Rozszerzenie Chrome do weryfikacji wojskowej |

### 🔗 Narzędzia Zewnętrzne

| Narzędzie | Typ | Opis |
|------|------|-------------|
| [SheerID VIP Bot](https://t.me/SheerID_VIP_Bot?start=ref_REF001124) | ⚡ Bot | Alternatywny bot Telegram z szybszym przetwarzaniem |
| [SheerID VN Bot](https://t.me/sheeridvn_bot?start=invite_7762497789) | 🇻🇳 Bot | Bot Telegram społeczności wietnamskiej |
| [Veterans Verify Bot](https://t.me/vgptplusbot?start=ref_7762497789) | 🎖️ Bot | Bot weryfikacji wojskowej |
| [Batch 1Key.me](https://batch.1key.me/) | 📦 Web | Weryfikacja wsadowa dla wielu adresów URL |
| [Student Card Generator](https://thanhnguyxn.github.io/student-card-generator/) | 🎓 Tool | Tworzenie legitymacji studenckich do weryfikacji ręcznej |
| [Payslip Generator](https://thanhnguyxn.github.io/payslip-generator/) | 💰 Tool | Generowanie odcinków wypłat do weryfikacji nauczycieli |
| [RoxyBrowser](https://roxybrowser.com?code=01045PFA) | 🦊 Browser | **Przeglądarka antywykrywania** — Bezpiecznie zarządzaj wieloma zweryfikowanymi kontami bez bana |

---

## 🧠 Podstawowa Architektura i Logika

Wszystkie narzędzia Python w tym repozytorium dzielą wspólną, zoptymalizowaną architekturę zaprojektowaną dla wysokich wskaźników sukcesu.

### 1. Przepływ Weryfikacji (The Verification Flow)
Narzędzia postępują zgodnie ze standardowym procesem "Wodospadu" (Waterfall):
1.  **Generowanie Danych (Data Generation)**: Tworzy realistyczną tożsamość (Imię, Data urodzenia, Email) pasującą do docelowej grupy demograficznej.
2.  **Przesłanie (`collectStudentPersonalInfo`)**: Przesyła dane do API SheerID.
3.  **Pominięcie SSO (`DELETE /step/sso`)**: Kluczowy krok. Pomija wymóg logowania się do portalu szkolnego.
4.  **Przesłanie Dokumentu (`docUpload`)**: Przesyła wygenerowany dokument dowodowy (Legitymacja studencka, Transkrypt lub Odznaka nauczyciela).
5.  **Zakończenie (`completeDocUpload`)**: Sygnalizuje SheerID, że przesyłanie zostało zakończone.

### 2. Inteligentne Strategie (Intelligent Strategies)

#### 🎓 Strategia Uniwersytecka (Spotify, YouTube, Gemini)
- **Wybór Ważony**: Używa wyselekcjonowanej listy **45+ Uniwersytetów** (USA, VN, JP, KR itp.).
- **Śledzenie Sukcesu**: Uniwersytety z wyższymi wskaźnikami sukcesu są wybierane częściej.
- **Generowanie Dokumentów**: Generuje realistycznie wyglądające legitymacje studenckie z dynamicznymi nazwiskami i datami.

#### 👨‍🏫 Strategia Nauczycielska (Bolt.new)
- **Targetowanie Wiekowe**: Generuje starsze tożsamości (25-55 lat), aby pasowały do demografii nauczycieli.
- **Generowanie Dokumentów**: Tworzy "Zaświadczenia o Zatrudnieniu" zamiast legitymacji studenckich.
- **Punkt Końcowy**: Celuje w `collectTeacherPersonalInfo` zamiast punktów końcowych dla studentów.

#### 🏫 Strategia K12 (ChatGPT Plus)
- **Targetowanie Typu Szkoły**: Specjalnie celuje w szkoły z `type: "K12"` (nie `HIGH_SCHOOL`).
- **Logika Automatycznego Przejścia (Auto-Pass)**: Weryfikacja K12 jest często **automatycznie zatwierdzana** bez przesyłania dokumentów, jeśli informacje o szkole i nauczycielu są zgodne.
- **Rezerwa**: Jeśli wymagane jest przesłanie, generuje Odznakę Nauczyciela.

#### 🎖️ Strategia Weteranów (ChatGPT Plus)
- **Ścisła Kwalifikowalność**: Celuje w czynny personel wojskowy lub weteranów zwolnionych w ciągu **ostatnich 12 miesięcy**.
- **Autorytatywne Sprawdzenie**: SheerID weryfikuje w bazie danych DoD/DEERS.
- **Logika**: Domyślnie używa niedawnych dat zwolnienia, aby zmaksymalizować szanse na automatyczne zatwierdzenie.

---

## 📋 Szybki Start

### Wymagania wstępne
- Python 3.8+
- `pip`

### Instalacja

1.  **Sklonuj repozytorium:**
    ```bash
    git clone https://github.com/ThanhNguyxn/SheerID-Verification-Tool.git
    cd SheerID-Verification-Tool
    ```

2.  **Zainstaluj zależności:**
    ```bash
    pip install httpx Pillow
    ```

3.  **Uruchom narzędzie (np. Spotify):**
    ```bash
    cd spotify-verify-tool
    python main.py "YOUR_SHEERID_URL"
    ```

---

## ⚠️ Zrzeczenie się Odpowiedzialności

Ten projekt służy wyłącznie do **celów edukacyjnych**. Narzędzia pokazują, jak działają systemy weryfikacji i jak można je testować.
- Nie używać do celów oszukańczych.
- Autorzy nie ponoszą odpowiedzialności za jakiekolwiek niewłaściwe użycie.
- Przestrzegaj Warunków Świadczenia Usług wszystkich platform.

---

## 🤝 Współpraca

Wkład jest mile widziany! Zapraszam do przesłania Pull Request.

---

## 🦊 Oficjalny Partner: RoxyBrowser

🛡 **Ochrona Przed Wykryciem** — Unikalny odcisk palca dla każdego konta, wygląda jak różne prawdziwe urządzenia.

📉 **Zapobiegaj Łączeniu** — Blokuje SheerID i platformy przed łączeniem Twoich kont.

🚀 **Idealny dla Użytkowników Masowych** — Bezpiecznie zarządzaj setkami zweryfikowanych kont.

[![Wypróbuj Za Darmo](https://img.shields.io/badge/Wypróbuj%20Za%20Darmo-RoxyBrowser-ff6b35?style=for-the-badge&logo=googlechrome&logoColor=white)](https://roxybrowser.com?code=01045PFA)

---

## ❤️ Wsparcie

Jeśli uważasz ten projekt za przydatny, rozważ wsparcie mnie:

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-ea4aaa?style=for-the-badge&logo=github)](https://github.com/sponsors/ThanhNguyxn)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/thanhnguyxn)

---

## 🌐 Języki

| 🇺🇸 [English](../README.md) | 🇻🇳 [Tiếng Việt](./README.vi.md) | 🇨🇳 [中文](./README.zh.md) | 🇯🇵 [日本語](./README.ja.md) | 🇰🇷 [한국어](./README.ko.md) |
|:---:|:---:|:---:|:---:|:---:|
| 🇪🇸 [Español](./README.es.md) | 🇫🇷 [Français](./README.fr.md) | 🇩🇪 [Deutsch](./README.de.md) | 🇧🇷 [Português](./README.pt-BR.md) | 🇷🇺 [Русский](./README.ru.md) |
| 🇸🇦 [العربية](./README.ar.md) | 🇮🇳 [हिन्दी](./README.hi.md) | 🇹🇭 [ไทย](./README.th.md) | 🇹🇷 [Türkçe](./README.tr.md) | 🇵🇱 [Polski](./README.pl.md) |
| 🇮🇹 [Italiano](./README.it.md) | 🇮🇩 [Bahasa Indonesia](./README.id.md) | | | |
