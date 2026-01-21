# 🔐 Narzędzie Weryfikacji SheerID

[![GitHub Stars](https://img.shields.io/github/stars/ThanhNguyxn/SheerID-Verification-Tool?style=social)](https://github.com/ThanhNguyxn/SheerID-Verification-Tool/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Documentation](https://img.shields.io/badge/Docs-Website-2ea44f?style=flat&logo=github&logoColor=white)](https://thanhnguyxn.github.io/SheerID-Verification-Tool/)

Kompleksowa kolekcja narzędzi do automatyzacji workflow weryfikacji SheerID dla różnych usług (Spotify, YouTube, Google One itp.).

---

## 🛠️ Dostępne Narzędzia

| Narzędzie | Typ | Cel | Opis |
|------|------|--------|-------------|
| [spotify-verify-tool](../spotify-verify-tool/) | 🎵 Student | Spotify Premium | Weryfikacja studentów uniwersytetu |
| [youtube-verify-tool](../youtube-verify-tool/) | 🎬 Student | YouTube Premium | Weryfikacja studentów uniwersytetu |
| [one-verify-tool](../one-verify-tool/) | 🤖 Student | Gemini Advanced | Weryfikacja Google One AI Premium |
| [boltnew-verify-tool](../boltnew-verify-tool/) | 👨‍🏫 Nauczyciel | Bolt.new | Weryfikacja nauczycieli (Uniwersytet) |
| [canva-teacher-tool](../canva-teacher-tool/) | 🇬🇧 Nauczyciel | Canva Education | Weryfikacja nauczycieli UK (K-12) |
| [k12-verify-tool](../k12-verify-tool/) | 🏫 K12 | ChatGPT Plus | Weryfikacja nauczycieli K12 |
| [veterans-verify-tool](../veterans-verify-tool/) | 🎖️ Wojsko | Ogólne | Weryfikacja statusu wojskowego |
| [veterans-extension](../veterans-extension/) | 🧩 Chrome | Przeglądarka | Rozszerzenie Chrome do weryfikacji wojskowej |

### 🔗 Narzędzia Zewnętrzne

| Narzędzie | Typ | Opis |
|------|------|-------------|
| [RoxyBrowser](https://roxybrowser.com?code=01045PFA) | 🦊 Przeglądarka | **Przeglądarka anty-detekcyjna** — Bezpiecznie zarządzaj wieloma zweryfikowanymi kontami |
| [Check IP](https://ip123.in/en?code=01045PFA) | 🌐 Web | **Sprawdź IP** — Sprawdź swój adres IP i status proxy |
| [SheerID Verification Bot](https://t.me/SheerID_Verification_bot?start=ref_LdPKPES3Ej) | 🤖 Bot | Automatyczny bot Telegram |
| [GPT Bot](https://t.me/vgptplusbot?start=ref_7762497789) | 🤖 Bot | Automatyczny bot weryfikacyjny |
| [Student Card Generator](https://thanhnguyxn.github.io/student-card-generator/) | 🎓 Narzędzie | Tworzenie legitymacji studenckich |
| [Payslip Generator](https://thanhnguyxn.github.io/payslip-generator/) | 💰 Narzędzie | Generowanie odcinków wypłaty |

---

## 🧠 Główna Architektura i Logika

Wszystkie narzędzia Python w tym repozytorium współdzielą wspólną architekturę zoptymalizowaną pod wysoki wskaźnik sukcesu.

### 1. Przepływ Weryfikacji
1. **Generowanie Danych**: Tworzy realistyczną tożsamość
2. **Wysyłanie**: Wysyła dane do API SheerID
3. **Pominięcie SSO**: Omija wymóg logowania do portalu szkolnego
4. **Przesyłanie Dokumentu**: Przesyła wygenerowany dokument dowodowy
5. **Zakończenie**: Sygnalizuje SheerID zakończenie przesyłania

### 2. Inteligentne Strategie

#### 🎓 Strategia Uniwersytecka (Spotify, YouTube, Gemini)
- Lista **45+ Uniwersytetów**
- Uniwersytety z wyższym wskaźnikiem sukcesu wybierane częściej
- Generuje realistyczne legitymacje studenckie

#### 👨‍🏫 Strategia Nauczyciela (Bolt.new)
- Generuje tożsamości 25-55 lat
- Tworzy "Zaświadczenia o Zatrudnieniu"

#### 🏫 Strategia K12 (ChatGPT Plus)
- Celuje w szkoły `type: "K12"`
- Często automatycznie zatwierdzane

#### 🎖️ Strategia Weteranów (ChatGPT Plus)
- Celuje w weteranów zwolnionych w ciągu ostatnich 12 miesięcy
- Weryfikuje z bazy DoD/DEERS

#### 🛡️ Moduł Anty-Detekcji
- Losowe User-Agents (10+ prawdziwych przeglądarek)
- Spoofing odcisku TLS (`curl_cffi`)
- Losowe opóźnienia
- Generowanie realistycznych e-maili

#### 📄 Moduł Generowania Dokumentów
- Wstrzykiwanie szumu pikselowego
- 6 różnych schematów kolorów
- Dynamiczne pozycjonowanie ±3px

> [!WARNING]
> **Narzędzia API mają naturalne ograniczenia** — Użyj residential proxy + `curl_cffi`.

> [!IMPORTANT]
> **Gemini/Google One TYLKO USA (od stycznia 2026)**

---

## 📋 Szybki Start

```bash
git clone https://github.com/ThanhNguyxn/SheerID-Verification-Tool.git
cd SheerID-Verification-Tool
pip install httpx Pillow
pip install curl_cffi cloudscraper  # Opcjonalnie
cd spotify-verify-tool
python main.py "YOUR_SHEERID_URL"
```

---

## 🦊 Oficjalny Partner: RoxyBrowser

[![Wypróbuj Za Darmo](https://img.shields.io/badge/Wypróbuj%20Za%20Darmo-RoxyBrowser-ff6b35?style=for-the-badge&logo=googlechrome&logoColor=white)](https://roxybrowser.com?code=01045PFA)

---

## ⚠️ Wyłączenie Odpowiedzialności

Ten projekt jest przeznaczony wyłącznie do **celów edukacyjnych**. Nie używaj do celów oszukańczych.

---

## ❤️ Wsparcie

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-ea4aaa?style=for-the-badge&logo=github)](https://github.com/sponsors/ThanhNguyxn)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/thanhnguyxn)

---

## 🌐 Języki

| 🇺🇸 [English](../README.md) | 🇻🇳 [Tiếng Việt](./README.vi.md) | 🇨🇳 [中文](./README.zh.md) | 🇯🇵 [日本語](./README.ja.md) | 🇰🇷 [한국어](./README.ko.md) |
|:---:|:---:|:---:|:---:|:---:|
| 🇪🇸 [Español](./README.es.md) | 🇫🇷 [Français](./README.fr.md) | 🇩🇪 [Deutsch](./README.de.md) | 🇧🇷 [Português](./README.pt-BR.md) | 🇷🇺 [Русский](./README.ru.md) |
| 🇸🇦 [العربية](./README.ar.md) | 🇮🇳 [हिन्दी](./README.hi.md) | 🇹🇭 [ไทย](./README.th.md) | 🇹🇷 [Türkçe](./README.tr.md) | 🇵🇱 [Polski](./README.pl.md) |
| 🇮🇹 [Italiano](./README.it.md) | 🇮🇩 [Bahasa Indonesia](./README.id.md) | | | |
