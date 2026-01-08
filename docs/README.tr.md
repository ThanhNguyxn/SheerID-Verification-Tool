# 🔐 SheerID Doğrulama Aracı

[![GitHub Stars](https://img.shields.io/github/stars/ThanhNguyxn/SheerID-Verification-Tool?style=social)](https://github.com/ThanhNguyxn/SheerID-Verification-Tool/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

Çeşitli hizmetler (Spotify, YouTube, Google One vb.) için SheerID doğrulama iş akışlarını otomatikleştirmek için kapsamlı bir araç koleksiyonu.

---

## 🛠️ Mevcut Araçlar

| Araç | Tür | Hedef | Açıklama |
|------|------|--------|-------------|
| [spotify-verify-tool](../spotify-verify-tool/) | 🎵 Öğrenci | Spotify Premium | Üniversite öğrencisi doğrulaması |
| [youtube-verify-tool](../youtube-verify-tool/) | 🎬 Öğrenci | YouTube Premium | Üniversite öğrencisi doğrulaması |
| [one-verify-tool](../one-verify-tool/) | 🤖 Öğrenci | Gemini Advanced | Google One AI Premium doğrulaması |
| [boltnew-verify-tool](../boltnew-verify-tool/) | 👨‍🏫 Öğretmen | Bolt.new | Öğretmen doğrulaması (Üniversite) |
| [k12-verify-tool](../k12-verify-tool/) | 🏫 K12 | ChatGPT Plus | K12 Öğretmen doğrulaması (Lise) |
| [veterans-verify-tool](../veterans-verify-tool/) | 🎖️ Askeri | Genel | Askeri durum doğrulaması |
| [veterans-extension](../veterans-extension/) | 🧩 Chrome | Tarayıcı | Askeri doğrulama için Chrome uzantısı |

### 🔗 Harici Araçlar

| Araç | Tür | Açıklama |
|------|------|-------------|
| [RoxyBrowser](https://roxybrowser.com?code=01045PFA) | 🦊 Browser | **Anti-tespit tarayıcı** — Yasaklanmadan birden fazla doğrulanmış hesabı güvenle yönetin |
| [SheerID Auto Verify](https://ip123.in/sheerid/?code=01045PFA) | 🔐 Web | **Otomatik doğrulama aracı** — Hızlı otomatik SheerID doğrulaması |
| [SheerID Verification Bot](https://t.me/SheerID_Verification_bot?start=ref_LdPKPES3Ej) | 🤖 Bot | Vietnam topluluğu Telegram botu |
| [Auto SheerID Bot](https://t.me/auto_sheerid_bot?start=7762497789) | 🤖 Bot | Otomatik doğrulama botu |
| [Student Card Generator](https://thanhnguyxn.github.io/student-card-generator/) | 🎓 Tool | Manuel doğrulama için öğrenci kimlik kartları oluşturun |
| [Payslip Generator](https://thanhnguyxn.github.io/payslip-generator/) | 💰 Tool | Öğretmen doğrulaması için maaş bordroları oluşturun |

---

## 🧠 Temel Mimari ve Mantık

Bu depodaki tüm Python araçları, yüksek başarı oranları için optimize edilmiş ortak bir mimariyi paylaşır.

### 1. Doğrulama Akışı (The Verification Flow)
Araçlar standartlaştırılmış bir "Şelale" sürecini izler:
1.  **Veri Oluşturma (Data Generation)**: Hedef demografiye uygun gerçekçi bir kimlik (İsim, Doğum Tarihi, E-posta) oluşturur.
2.  **Gönderim (`collectStudentPersonalInfo`)**: Verileri SheerID API'sine gönderir.
3.  **SSO Atlama (`DELETE /step/sso`)**: Kritik adım. Bir okul portalına giriş yapma gereksinimini atlar.
4.  **Belge Yükleme (`docUpload`)**: Oluşturulan bir kanıt belgesini (Öğrenci Kimliği, Transkript veya Öğretmen Rozeti) yükler.
5.  **Tamamlama (`completeDocUpload`)**: Yüklemenin bittiğini SheerID'ye bildirir.

### 2. Akıllı Stratejiler (Intelligent Strategies)

#### 🎓 Üniversite Stratejisi (Spotify, YouTube, Gemini)
- **Ağırlıklı Seçim**: **45+ Üniversite** (ABD, VN, JP, KR vb.) içeren küratörlü bir liste kullanır.
- **Başarı Takibi**: Daha yüksek başarı oranlarına sahip üniversiteler daha sık seçilir.
- **Belge Oluşturma**: Dinamik isimler ve tarihlerle gerçekçi görünen Öğrenci Kimlik kartları oluşturur.

#### 👨‍🏫 Öğretmen Stratejisi (Bolt.new)
- **Yaş Hedefleme**: Öğretmen demografisine uyması için daha yaşlı kimlikler (25-55 yaş) oluşturur.
- **Belge Oluşturma**: Öğrenci Kimlikleri yerine "İstihdam Sertifikaları" oluşturur.
- **Uç Nokta**: Öğrenci uç noktaları yerine `collectTeacherPersonalInfo` hedeflenir.

#### 🏫 K12 Stratejisi (ChatGPT Plus)
- **Okul Türü Hedefleme**: Özellikle `type: "K12"` ( `HIGH_SCHOOL` değil) olan okulları hedefler.
- **Otomatik Geçiş Mantığı (Auto-Pass)**: Okul ve öğretmen bilgileri eşleşirse, K12 doğrulaması genellikle belge yüklemesi olmadan **otomatik olarak onaylanır**.
- **Yedek**: Yükleme gerekirse, bir Öğretmen Rozeti oluşturur.

#### 🎖️ Gaziler Stratejisi (ChatGPT Plus)
- **Sıkı Uygunluk**: Muvazzaf Askeri Personeli veya **son 12 ay** içinde terhis olan Gazileri hedefler.
- **Yetkili Kontrol**: SheerID, DoD/DEERS veritabanına karşı doğrular.
- **Mantık**: Otomatik onay şansını en üst düzeye çıkarmak için varsayılan olarak yakın tarihli terhis tarihlerini kullanır.

---

## 📋 Hızlı Başlangıç

### Önkoşullar
- Python 3.8+
- `pip`

### Kurulum

1.  **Depoyu klonlayın:**
    ```bash
    git clone https://github.com/ThanhNguyxn/SheerID-Verification-Tool.git
    cd SheerID-Verification-Tool
    ```

2.  **Bağımlılıkları yükleyin:**
    ```bash
    pip install httpx Pillow
    ```

3.  **Bir aracı çalıştırın (ör. Spotify):**
    ```bash
    cd spotify-verify-tool
    python main.py "YOUR_SHEERID_URL"
    ```

---

## ⚠️ Sorumluluk Reddi

Bu proje sadece **eğitim amaçlıdır**. Araçlar, doğrulama sistemlerinin nasıl çalıştığını ve nasıl test edilebileceğini gösterir.
- Dolandırıcılık amacıyla kullanmayın.
- Yazarlar herhangi bir kötüye kullanımdan sorumlu değildir.
- Tüm platformların Hizmet Şartlarına saygı gösterin.

---

## 🤝 Katkıda Bulunma

Katkılar memnuniyetle karşılanır! Lütfen bir Pull Request göndermekten çekinmeyin.

---

## 🦊 Resmi Ortak: RoxyBrowser

🛡 **Anti-Tespit Koruması** — Her hesap için benzersiz parmak izi, farklı gerçek cihazlar gibi görünür.

📉 **Bağlantıyı Önle** — SheerID ve platformların hesaplarınızı bağlamasını engeller.

🚀 **Toplu Kullanıcılar için İdeal** — Yüzlerce doğrulanmış hesabı güvenle yönetin.

[![Ücretsiz Dene](https://img.shields.io/badge/Ücretsiz%20Dene-RoxyBrowser-ff6b35?style=for-the-badge&logo=googlechrome&logoColor=white)](https://roxybrowser.com?code=01045PFA)

---

## ❤️ Destek

Bu projeyi yararlı bulduysanız, beni desteklemeyi düşünün:

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-ea4aaa?style=for-the-badge&logo=github)](https://github.com/sponsors/ThanhNguyxn)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/thanhnguyxn)

---

## 🌐 Diller

| 🇺🇸 [English](../README.md) | 🇻🇳 [Tiếng Việt](./README.vi.md) | 🇨🇳 [中文](./README.zh.md) | 🇯🇵 [日本語](./README.ja.md) | 🇰🇷 [한국어](./README.ko.md) |
|:---:|:---:|:---:|:---:|:---:|
| 🇪🇸 [Español](./README.es.md) | 🇫🇷 [Français](./README.fr.md) | 🇩🇪 [Deutsch](./README.de.md) | 🇧🇷 [Português](./README.pt-BR.md) | 🇷🇺 [Русский](./README.ru.md) |
| 🇸🇦 [العربية](./README.ar.md) | 🇮🇳 [हिन्दी](./README.hi.md) | 🇹🇭 [ไทย](./README.th.md) | 🇹🇷 [Türkçe](./README.tr.md) | 🇵🇱 [Polski](./README.pl.md) |
| 🇮🇹 [Italiano](./README.it.md) | 🇮🇩 [Bahasa Indonesia](./README.id.md) | | | |
