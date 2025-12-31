# 🔐 Alat Verifikasi SheerID

[![GitHub Stars](https://img.shields.io/github/stars/ThanhNguyxn/SheerID-Verification-Tool?style=social)](https://github.com/ThanhNguyxn/SheerID-Verification-Tool/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

Koleksi alat komprehensif untuk mengotomatiskan alur kerja verifikasi SheerID untuk berbagai layanan (Spotify, YouTube, Google One, dll.).

---

## 🛠️ Alat yang Tersedia

| Alat | Tipe | Target | Deskripsi |
|------|------|--------|-------------|
| [spotify-verify-tool](../spotify-verify-tool/) | 🎵 Mahasiswa | Spotify Premium | Verifikasi mahasiswa universitas |
| [youtube-verify-tool](../youtube-verify-tool/) | 🎬 Mahasiswa | YouTube Premium | Verifikasi mahasiswa universitas |
| [one-verify-tool](../one-verify-tool/) | 🤖 Mahasiswa | Gemini Advanced | Verifikasi Google One AI Premium |
| [boltnew-verify-tool](../boltnew-verify-tool/) | 👨‍🏫 Guru | Bolt.new | Verifikasi guru (Universitas) |
| [k12-verify-tool](../k12-verify-tool/) | 🏫 K12 | ChatGPT Plus | Verifikasi guru K12 (Sekolah Menengah) |
| [veterans-verify-tool](../veterans-verify-tool/) | 🎖️ Militer | Umum | Verifikasi status militer |
| [veterans-extension](../veterans-extension/) | 🧩 Chrome | Browser | Ekstensi Chrome untuk verifikasi militer |

### 🔗 Alat Eksternal

| Alat | Tipe | Deskripsi |
|------|------|-------------|
| [SheerID VIP Bot](https://t.me/SheerID_VIP_Bot?start=ref_REF001124) | ⚡ Bot | Bot Telegram alternatif dengan pemrosesan lebih cepat |
| [SheerID VN Bot](https://t.me/sheeridvn_bot?start=invite_7762497789) | 🇻🇳 Bot | Bot Telegram komunitas Vietnam |
| [Veterans Verify Bot](https://t.me/Veriyferbot?start=ref_7762497789) | 🎖️ Bot | Bot verifikasi militer |
| [Batch 1Key.me](https://batch.1key.me/) | 📦 Web | Verifikasi batch untuk beberapa URL |
| [Student Card Generator](https://thanhnguyxn.github.io/student-card-generator/) | 🎓 Tool | Buat kartu mahasiswa untuk verifikasi manual |
| [Payslip Generator](https://thanhnguyxn.github.io/payslip-generator/) | 💰 Tool | Hasilkan slip gaji untuk verifikasi guru |

---

## 🧠 Arsitektur & Logika Inti

Semua alat Python di repositori ini berbagi arsitektur umum yang dioptimalkan untuk tingkat keberhasilan yang tinggi.

### 1. Alur Verifikasi (The Verification Flow)
Alat-alat ini mengikuti proses "Air Terjun" (Waterfall) standar:
1.  **Pembuatan Data (Data Generation)**: Membuat identitas realistis (Nama, Tanggal Lahir, Email) yang sesuai dengan demografi target.
2.  **Pengiriman (`collectStudentPersonalInfo`)**: Mengirimkan data ke API SheerID.
3.  **Lewati SSO (`DELETE /step/sso`)**: Langkah krusial. Melewati persyaratan untuk masuk ke portal sekolah.
4.  **Unggah Dokumen (`docUpload`)**: Mengunggah dokumen bukti yang dibuat (Kartu Mahasiswa, Transkrip, atau Lencana Guru).
5.  **Penyelesaian (`completeDocUpload`)**: Memberi sinyal ke SheerID bahwa pengunggahan selesai.

### 2. Strategi Cerdas (Intelligent Strategies)

#### 🎓 Strategi Universitas (Spotify, YouTube, Gemini)
- **Seleksi Tertimbang**: Menggunakan daftar kurasi dari **45+ Universitas** (AS, VN, JP, KR, dll.).
- **Pelacakan Keberhasilan**: Universitas dengan tingkat keberhasilan lebih tinggi dipilih lebih sering.
- **Pembuatan Dokumen**: Menghasilkan kartu identitas mahasiswa yang tampak realistis dengan nama dan tanggal dinamis.

#### 👨‍🏫 Strategi Guru (Bolt.new)
- **Penargetan Usia**: Menghasilkan identitas yang lebih tua (25-55 tahun) agar sesuai dengan demografi guru.
- **Pembuatan Dokumen**: Membuat "Sertifikat Kerja" alih-alih Kartu Mahasiswa.
- **Endpoint**: Menargetkan `collectTeacherPersonalInfo` alih-alih endpoint mahasiswa.

#### 🏫 Strategi K12 (ChatGPT Plus)
- **Penargetan Tipe Sekolah**: Secara khusus menargetkan sekolah dengan `type: "K12"` (bukan `HIGH_SCHOOL`).
- **Logika Lulus Otomatis (Auto-Pass)**: Verifikasi K12 sering kali **disetujui secara otomatis** tanpa unggah dokumen jika informasi sekolah dan guru cocok.
- **Cadangan**: Jika unggahan diperlukan, ini menghasilkan Lencana Guru.

#### 🎖️ Strategi Veteran (ChatGPT Plus)
- **Kelayakan Ketat**: Menargetkan Personel Militer Aktif atau Veteran yang diberhentikan dalam **12 bulan terakhir**.
- **Pemeriksaan Otoritatif**: SheerID memverifikasi terhadap database DoD/DEERS.
- **Logika**: Secara default menggunakan tanggal pemberhentian baru-baru ini untuk memaksimalkan peluang persetujuan otomatis.

---

## 📋 Mulai Cepat

### Prasyarat
- Python 3.8+
- `pip`

### Instalasi

1.  **Kloning repositori:**
    ```bash
    git clone https://github.com/ThanhNguyxn/SheerID-Verification-Tool.git
    cd SheerID-Verification-Tool
    ```

2.  **Instal dependensi:**
    ```bash
    pip install httpx Pillow
    ```

3.  **Jalankan alat (misalnya, Spotify):**
    ```bash
    cd spotify-verify-tool
    python main.py "YOUR_SHEERID_URL"
    ```

---

## ⚠️ Penafian

Proyek ini hanya untuk **tujuan pendidikan**. Alat-alat ini menunjukkan cara kerja sistem verifikasi dan cara pengujiannya.
- Jangan gunakan untuk tujuan penipuan.
- Penulis tidak bertanggung jawab atas penyalahgunaan apa pun.
- Hormati Ketentuan Layanan semua platform.

---

## 🤝 Berkontribusi

Kontribusi dipersilakan! Jangan ragu untuk mengirimkan Pull Request.
