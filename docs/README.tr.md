# 🔐 SheerID Doğrulama Aracı

[![GitHub Stars](https://img.shields.io/github/stars/ThanhNguyxn/SheerID-Verification-Tool?style=social)](https://github.com/ThanhNguyxn/SheerID-Verification-Tool/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Documentation](https://img.shields.io/badge/Docs-Website-2ea44f?style=flat&logo=github&logoColor=white)](https://thanhnguyxn.github.io/SheerID-Verification-Tool/)

Çeşitli hizmetler (Spotify, YouTube, Google One vb.) için SheerID doğrulama iş akışlarını otomatikleştirmek için kapsamlı araç koleksiyonu.

---

## 🛠️ Mevcut Araçlar

| Araç | Tür | Hedef | Açıklama |
|------|------|--------|-------------|
| [spotify-verify-tool](../spotify-verify-tool/) | 🎵 Öğrenci | Spotify Premium | Üniversite öğrenci doğrulaması |
| [youtube-verify-tool](../youtube-verify-tool/) | 🎬 Öğrenci | YouTube Premium | Üniversite öğrenci doğrulaması |
| [one-verify-tool](../one-verify-tool/) | 🤖 Öğrenci | Gemini Advanced | Google One AI Premium doğrulaması |
| [boltnew-verify-tool](../boltnew-verify-tool/) | 👨‍🏫 Öğretmen | Bolt.new | Öğretmen doğrulaması (Üniversite) |
| [canva-teacher-tool](../canva-teacher-tool/) | 🇬🇧 Öğretmen | Canva Education | UK Öğretmen doğrulaması (K-12) |
| [k12-verify-tool](../k12-verify-tool/) | 🏫 K12 | ChatGPT Plus | K12 öğretmen doğrulaması |
| [veterans-verify-tool](../veterans-verify-tool/) | 🎖️ Askeri | Genel | Askeri durum doğrulaması |
| [veterans-extension](../veterans-extension/) | 🧩 Chrome | Tarayıcı | Askeri doğrulama için Chrome eklentisi |

### 🔗 Harici Araçlar

| Araç | Tür | Açıklama |
|------|------|-------------|
| [RoxyBrowser](https://roxybrowser.com?code=01045PFA) | 🦊 Tarayıcı | **Anti-tespit tarayıcı** — Yasaklanmadan birden fazla doğrulanmış hesabı güvenle yönetin |
| [Check IP](https://ip123.in/en?code=01045PFA) | 🌐 Web | **IP Kontrol** — IP adresinizi ve proxy durumunuzu kontrol edin |
| [SheerID Verification Bot](https://t.me/SheerID_Verification_bot?start=ref_LdPKPES3Ej) | 🤖 Bot | Otomatik Telegram doğrulama botu |
| [GPT Bot](https://t.me/vgptplusbot?start=ref_7762497789) | 🤖 Bot | Otomatik doğrulama botu |
| [Student Card Generator](https://thanhnguyxn.github.io/student-card-generator/) | 🎓 Araç | Manuel doğrulama için öğrenci kartları oluşturun |
| [Payslip Generator](https://thanhnguyxn.github.io/payslip-generator/) | 💰 Araç | Öğretmen doğrulaması için bordro oluşturun |

---

## 🧠 Temel Mimari ve Mantık

Bu depodaki tüm Python araçları, yüksek başarı oranları için optimize edilmiş ortak bir mimariyi paylaşır.

### 1. Doğrulama Akışı
1. **Veri Oluşturma**: Hedef demografiye uyan gerçekçi kimlik oluşturur
2. **Gönderim**: SheerID API'ye veri gönderir
3. **SSO Atlama**: Okul portalına giriş gereksinimini atlar
4. **Belge Yükleme**: Oluşturulan kanıt belgesini yükler
5. **Tamamlama**: Yüklemenin bittiğini SheerID'ye bildirir

### 2. Akıllı Stratejiler

#### 🎓 Üniversite Stratejisi (Spotify, YouTube, Gemini)
- **45+ Üniversite** listesi kullanır
- Başarı oranı yüksek üniversiteler daha sık seçilir
- Gerçekçi öğrenci kimlik kartları oluşturur

#### 👨‍🏫 Öğretmen Stratejisi (Bolt.new)
- 25-55 yaş arası kimlikler oluşturur
- Öğrenci kartları yerine "İstihdam Sertifikası" oluşturur

#### 🏫 K12 Stratejisi (ChatGPT Plus)
- `type: "K12"` olan okulları hedefler
- Genellikle belge yüklemeden otomatik onaylanır

#### 🎖️ Gaziler Stratejisi (ChatGPT Plus)
- Son 12 ay içinde terhis olan askerleri hedefler
- DoD/DEERS veritabanına karşı doğrular

#### 🛡️ Anti-Tespit Modülü
- Rastgele User-Agents (10+ gerçek tarayıcı)
- TLS parmak izi sahteciliği (`curl_cffi`)
- Rastgele gecikmeler
- Gerçekçi e-posta oluşturma

#### 📄 Belge Oluşturma Modülü
- Piksel gürültüsü enjeksiyonu
- 6 farklı renk şeması
- ±3px dinamik konumlandırma

> [!WARNING]
> **API Tabanlı Araçların Doğal Sınırlamaları Var** — Konut proxy'leri + `curl_cffi` kullanın.

> [!IMPORTANT]
> **Gemini/Google One YALNIZCA ABD (Ocak 2026'dan beri)**

---

## 📋 Hızlı Başlangıç

```bash
git clone https://github.com/ThanhNguyxn/SheerID-Verification-Tool.git
cd SheerID-Verification-Tool
pip install httpx Pillow
pip install curl_cffi cloudscraper  # İsteğe bağlı
cd spotify-verify-tool
python main.py "YOUR_SHEERID_URL"
```

---

## 🦊 Resmi Ortak: RoxyBrowser

[![Ücretsiz Dene](https://img.shields.io/badge/Ücretsiz%20Dene-RoxyBrowser-ff6b35?style=for-the-badge&logo=googlechrome&logoColor=white)](https://roxybrowser.com?code=01045PFA)

---

## ⚠️ Sorumluluk Reddi

Bu proje yalnızca **eğitim amaçlıdır**. Dolandırıcılık amaçlı kullanmayın.

---

## ❤️ Destek

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-ea4aaa?style=for-the-badge&logo=github)](https://github.com/sponsors/ThanhNguyxn)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/thanhnguyxn)

---

## 🌐 Diller

| 🇺🇸 [English](../README.md) | 🇻🇳 [Tiếng Việt](./README.vi.md) | 🇨🇳 [中文](./README.zh.md) | 🇯🇵 [日本語](./README.ja.md) | 🇰🇷 [한국어](./README.ko.md) |
|:---:|:---:|:---:|:---:|:---:|
| 🇪🇸 [Español](./README.es.md) | 🇫🇷 [Français](./README.fr.md) | 🇩🇪 [Deutsch](./README.de.md) | 🇧🇷 [Português](./README.pt-BR.md) | 🇷🇺 [Русский](./README.ru.md) |
| 🇸🇦 [العربية](./README.ar.md) | 🇮🇳 [हिन्दी](./README.hi.md) | 🇹🇭 [ไทย](./README.th.md) | 🇹🇷 [Türkçe](./README.tr.md) | 🇵🇱 [Polski](./README.pl.md) |
| 🇮🇹 [Italiano](./README.it.md) | 🇮🇩 [Bahasa Indonesia](./README.id.md) | | | |
