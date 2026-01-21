# 🔐 Alat Verifikasi SheerID

[![GitHub Stars](https://img.shields.io/github/stars/ThanhNguyxn/SheerID-Verification-Tool?style=social)](https://github.com/ThanhNguyxn/SheerID-Verification-Tool/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Documentation](https://img.shields.io/badge/Docs-Website-2ea44f?style=flat&logo=github&logoColor=white)](https://thanhnguyxn.github.io/SheerID-Verification-Tool/)

Koleksi lengkap alat untuk mengotomatisasi alur kerja verifikasi SheerID untuk berbagai layanan (Spotify, YouTube, Google One, dll.).

---

## 🛠️ Alat yang Tersedia

| Alat | Tipe | Target | Deskripsi |
|------|------|--------|-------------|
| [spotify-verify-tool](../spotify-verify-tool/) | 🎵 Mahasiswa | Spotify Premium | Verifikasi mahasiswa universitas |
| [youtube-verify-tool](../youtube-verify-tool/) | 🎬 Mahasiswa | YouTube Premium | Verifikasi mahasiswa universitas |
| [one-verify-tool](../one-verify-tool/) | 🤖 Mahasiswa | Gemini Advanced | Verifikasi Google One AI Premium |
| [boltnew-verify-tool](../boltnew-verify-tool/) | 👨‍🏫 Guru | Bolt.new | Verifikasi guru (Universitas) |
| [canva-teacher-tool](../canva-teacher-tool/) | 🇬🇧 Guru | Canva Education | Verifikasi guru UK (K-12) |
| [k12-verify-tool](../k12-verify-tool/) | 🏫 K12 | ChatGPT Plus | Verifikasi guru K12 |
| [veterans-verify-tool](../veterans-verify-tool/) | 🎖️ Militer | Umum | Verifikasi status militer |
| [veterans-extension](../veterans-extension/) | 🧩 Chrome | Browser | Ekstensi Chrome untuk verifikasi militer |

### 🔗 Alat Eksternal

| Alat | Tipe | Deskripsi |
|------|------|-------------|
| [RoxyBrowser](https://roxybrowser.com?code=01045PFA) | 🦊 Browser | **Browser anti-deteksi** — Kelola beberapa akun terverifikasi dengan aman tanpa banned |
| [Check IP](https://ip123.in/en?code=01045PFA) | 🌐 Web | **Cek IP** — Periksa alamat IP dan status proxy Anda |
| [SheerID Verification Bot](https://t.me/SheerID_Verification_bot?start=ref_LdPKPES3Ej) | 🤖 Bot | Bot Telegram verifikasi otomatis |
| [GPT Bot](https://t.me/vgptplusbot?start=ref_7762497789) | 🤖 Bot | Bot verifikasi otomatis |
| [Student Card Generator](https://thanhnguyxn.github.io/student-card-generator/) | 🎓 Alat | Buat kartu mahasiswa untuk verifikasi manual |
| [Payslip Generator](https://thanhnguyxn.github.io/payslip-generator/) | 💰 Alat | Buat slip gaji untuk verifikasi guru |

---

## 🧠 Arsitektur dan Logika Inti

Semua alat Python di repositori ini berbagi arsitektur umum yang dioptimalkan untuk tingkat keberhasilan tinggi.

### 1. Alur Verifikasi
1. **Pembuatan Data**: Membuat identitas realistis yang cocok dengan demografi target
2. **Pengiriman**: Mengirim data ke API SheerID
3. **Bypass SSO**: Melewati persyaratan login ke portal sekolah
4. **Upload Dokumen**: Mengunggah dokumen bukti yang dihasilkan
5. **Penyelesaian**: Memberi sinyal ke SheerID bahwa upload selesai

### 2. Strategi Cerdas

#### 🎓 Strategi Universitas (Spotify, YouTube, Gemini)
- Menggunakan daftar **45+ Universitas**
- Universitas dengan tingkat keberhasilan lebih tinggi dipilih lebih sering
- Menghasilkan kartu mahasiswa yang realistis

#### 👨‍🏫 Strategi Guru (Bolt.new)
- Menghasilkan identitas usia 25-55 tahun
- Membuat "Surat Keterangan Kerja"

#### 🏫 Strategi K12 (ChatGPT Plus)
- Menargetkan sekolah `type: "K12"`
- Sering disetujui secara otomatis

#### 🎖️ Strategi Veteran (ChatGPT Plus)
- Menargetkan veteran yang diberhentikan dalam 12 bulan terakhir
- Memverifikasi dengan database DoD/DEERS

#### 🛡️ Modul Anti-Deteksi
- User-Agents acak (10+ browser asli)
- Spoofing sidik jari TLS (`curl_cffi`)
- Penundaan acak
- Pembuatan email realistis

#### 📄 Modul Pembuatan Dokumen
- Injeksi noise piksel
- 6 skema warna berbeda
- Posisi dinamis ±3px

> [!WARNING]
> **Alat berbasis API memiliki keterbatasan bawaan** — Gunakan proxy residensial + `curl_cffi`.

> [!IMPORTANT]
> **Gemini/Google One HANYA AS (sejak Januari 2026)**

---

## 📋 Mulai Cepat

```bash
git clone https://github.com/ThanhNguyxn/SheerID-Verification-Tool.git
cd SheerID-Verification-Tool
pip install httpx Pillow
pip install curl_cffi cloudscraper  # Opsional
cd spotify-verify-tool
python main.py "YOUR_SHEERID_URL"
```

---

## 🦊 Partner Resmi: RoxyBrowser

[![Coba Gratis](https://img.shields.io/badge/Coba%20Gratis-RoxyBrowser-ff6b35?style=for-the-badge&logo=googlechrome&logoColor=white)](https://roxybrowser.com?code=01045PFA)

---

## ⚠️ Penafian

Proyek ini hanya untuk **tujuan pendidikan**. Jangan gunakan untuk tujuan penipuan.

---

## ❤️ Dukungan

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-ea4aaa?style=for-the-badge&logo=github)](https://github.com/sponsors/ThanhNguyxn)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/thanhnguyxn)

---

## 🌐 Bahasa

| 🇺🇸 [English](../README.md) | 🇻🇳 [Tiếng Việt](./README.vi.md) | 🇨🇳 [中文](./README.zh.md) | 🇯🇵 [日本語](./README.ja.md) | 🇰🇷 [한국어](./README.ko.md) |
|:---:|:---:|:---:|:---:|:---:|
| 🇪🇸 [Español](./README.es.md) | 🇫🇷 [Français](./README.fr.md) | 🇩🇪 [Deutsch](./README.de.md) | 🇧🇷 [Português](./README.pt-BR.md) | 🇷🇺 [Русский](./README.ru.md) |
| 🇸🇦 [العربية](./README.ar.md) | 🇮🇳 [हिन्दी](./README.hi.md) | 🇹🇭 [ไทย](./README.th.md) | 🇹🇷 [Türkçe](./README.tr.md) | 🇵🇱 [Polski](./README.pl.md) |
| 🇮🇹 [Italiano](./README.it.md) | 🇮🇩 [Bahasa Indonesia](./README.id.md) | | | |
