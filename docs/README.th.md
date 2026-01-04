# 🔐 เครื่องมือยืนยันตัวตน SheerID

[![GitHub Stars](https://img.shields.io/github/stars/ThanhNguyxn/SheerID-Verification-Tool?style=social)](https://github.com/ThanhNguyxn/SheerID-Verification-Tool/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

คอลเลกชันเครื่องมือที่ครอบคลุมสำหรับระบบอัตโนมัติเวิร์กโฟลว์การยืนยันตัวตน SheerID สำหรับบริการต่างๆ (Spotify, YouTube, Google One ฯลฯ)

---

## 🛠️ เครื่องมือที่มีอยู่

| เครื่องมือ | ประเภท | เป้าหมาย | คำอธิบาย |
|------|------|--------|-------------|
| [spotify-verify-tool](../spotify-verify-tool/) | 🎵 นักเรียน | Spotify Premium | การยืนยันตัวตนนักศึกษามหาวิทยาลัย |
| [youtube-verify-tool](../youtube-verify-tool/) | 🎬 นักเรียน | YouTube Premium | การยืนยันตัวตนนักศึกษามหาวิทยาลัย |
| [one-verify-tool](../one-verify-tool/) | 🤖 นักเรียน | Gemini Advanced | การยืนยันตัวตน Google One AI Premium |
| [boltnew-verify-tool](../boltnew-verify-tool/) | 👨‍🏫 ครู | Bolt.new | การยืนยันตัวตนครู (มหาวิทยาลัย) |
| [k12-verify-tool](../k12-verify-tool/) | 🏫 K12 | ChatGPT Plus | การยืนยันตัวตนครู K12 (มัธยมศึกษา) |
| [veterans-verify-tool](../veterans-verify-tool/) | 🎖️ ทหาร | ทั่วไป | การยืนยันสถานะทางทหาร |
| [veterans-extension](../veterans-extension/) | 🧩 Chrome | เบราว์เซอร์ | ส่วนขยาย Chrome สำหรับการยืนยันตัวตนทางทหาร |

### 🔗 เครื่องมือภายนอก

| เครื่องมือ | ประเภท | คำอธิบาย |
|------|------|-------------|
| [SheerID VIP Bot](https://t.me/SheerID_VIP_Bot?start=ref_REF001124) | ⚡ Bot | บอท Telegram ทางเลือกที่มีการประมวลผลเร็วกว่า |
| [SheerID VN Bot](https://t.me/sheeridvn_bot?start=invite_7762497789) | 🇻🇳 Bot | บอท Telegram ชุมชนเวียดนาม |
| [Veterans Verify Bot](https://t.me/vgptplusbot?start=ref_7762497789) | 🎖️ Bot | บอทยืนยันตัวตนทางทหาร |
| [Batch 1Key.me](https://batch.1key.me/) | 📦 Web | การยืนยันแบบกลุ่มสำหรับหลาย URL |
| [Student Card Generator](https://thanhnguyxn.github.io/student-card-generator/) | 🎓 Tool | สร้างบัตรนักเรียนสำหรับการยืนยันด้วยตนเอง |
| [Payslip Generator](https://thanhnguyxn.github.io/payslip-generator/) | 💰 Tool | สร้างสลิปเงินเดือนสำหรับการยืนยันตัวตนครู |
| [RoxyBrowser](https://roxybrowser.com?code=01045PFA) | 🦊 Browser | **เบราว์เซอร์ป้องกันการตรวจจับ** — จัดการบัญชีที่ยืนยันแล้วหลายบัญชีอย่างปลอดภัยโดยไม่ถูกแบน |

---

## 🧠 สถาปัตยกรรมหลักและตรรกะ

เครื่องมือ Python ทั้งหมดในที่เก็บนี้ใช้สถาปัตยกรรมร่วมกันที่ได้รับการปรับให้เหมาะสมเพื่ออัตราความสำเร็จสูง

### 1. ขั้นตอนการยืนยัน (The Verification Flow)
เครื่องมือปฏิบัติตามกระบวนการ "Waterfall" ที่เป็นมาตรฐาน:
1.  **การสร้างข้อมูล (Data Generation)**: สร้างตัวตนที่สมจริง (ชื่อ, วันเกิด, อีเมล) ที่ตรงกับกลุ่มประชากรเป้าหมาย
2.  **การส่งข้อมูล (`collectStudentPersonalInfo`)**: ส่งข้อมูลไปยัง SheerID API
3.  **ข้าม SSO (`DELETE /step/sso`)**: ขั้นตอนสำคัญ ข้ามข้อกำหนดในการเข้าสู่ระบบพอร์ทัลโรงเรียน
4.  **อัปโหลดเอกสาร (`docUpload`)**: อัปโหลดเอกสารหลักฐานที่สร้างขึ้น (บัตรนักเรียน, ใบแสดงผลการเรียน หรือบัตรประจำตัวครู)
5.  **เสร็จสิ้น (`completeDocUpload`)**: ส่งสัญญาณไปยัง SheerID ว่าการอัปโหลดเสร็จสิ้นแล้ว

### 2. กลยุทธ์อัจฉริยะ (Intelligent Strategies)

#### 🎓 กลยุทธ์มหาวิทยาลัย (Spotify, YouTube, Gemini)
- **การเลือกแบบถ่วงน้ำหนัก**: ใช้รายการที่คัดสรรแล้วของ **45+ มหาวิทยาลัย** (สหรัฐฯ, เวียดนาม, ญี่ปุ่น, เกาหลี ฯลฯ)
- **การติดตามความสำเร็จ**: มหาวิทยาลัยที่มีอัตราความสำเร็จสูงกว่าจะถูกเลือกบ่อยกว่า
- **การสร้างเอกสาร**: สร้างบัตรนักเรียนที่ดูสมจริงพร้อมชื่อและวันที่แบบไดนามิก

#### 👨‍🏫 กลยุทธ์ครู (Bolt.new)
- **การกำหนดเป้าหมายอายุ**: สร้างตัวตนที่มีอายุมากกว่า (25-55 ปี) เพื่อให้ตรงกับกลุ่มประชากรครู
- **การสร้างเอกสาร**: สร้าง "หนังสือรับรองการทำงาน" แทนบัตรนักเรียน
- **Endpoint**: กำหนดเป้าหมาย `collectTeacherPersonalInfo` แทน endpoint ของนักเรียน

#### 🏫 กลยุทธ์ K12 (ChatGPT Plus)
- **การกำหนดเป้าหมายประเภทโรงเรียน**: กำหนดเป้าหมายโรงเรียนที่มี `type: "K12"` (ไม่ใช่ `HIGH_SCHOOL`) โดยเฉพาะ
- **ตรรกะผ่านอัตโนมัติ (Auto-Pass)**: การยืนยัน K12 มักจะ **ได้รับการอนุมัติโดยอัตโนมัติ** โดยไม่ต้องอัปโหลดเอกสารหากข้อมูลโรงเรียนและครูตรงกัน
- **ทางเลือกสำรอง**: หากจำเป็นต้องอัปโหลด จะสร้างบัตรประจำตัวครู

#### 🎖️ กลยุทธ์ทหารผ่านศึก (ChatGPT Plus)
- **คุณสมบัติที่เข้มงวด**: กำหนดเป้าหมายบุคลากรทางทหารที่ประจำการหรือทหารผ่านศึกที่ปลดประจำการภายใน **12 เดือนที่ผ่านมา**
- **การตรวจสอบที่เชื่อถือได้**: SheerID ตรวจสอบกับฐานข้อมูล DoD/DEERS
- **ตรรกะ**: ใช้ค่าเริ่มต้นเป็นวันที่ปลดประจำการล่าสุดเพื่อเพิ่มโอกาสในการอนุมัติอัตโนมัติสูงสุด

---

## 📋 เริ่มต้นอย่างรวดเร็ว

### ข้อกำหนดเบื้องต้น
- Python 3.8+
- `pip`

### การติดตั้ง

1.  **โคลนที่เก็บ:**
    ```bash
    git clone https://github.com/ThanhNguyxn/SheerID-Verification-Tool.git
    cd SheerID-Verification-Tool
    ```

2.  **ติดตั้งการพึ่งพา:**
    ```bash
    pip install httpx Pillow
    ```

3.  **เรียกใช้เครื่องมือ (เช่น Spotify):**
    ```bash
    cd spotify-verify-tool
    python main.py "YOUR_SHEERID_URL"
    ```

---

## ⚠️ ข้อจำกัดความรับผิดชอบ

โครงการนี้มีไว้เพื่อ **วัตถุประสงค์ทางการศึกษาเท่านั้น** เครื่องมือแสดงให้เห็นว่าระบบการยืนยันทำงานอย่างไรและสามารถทดสอบได้อย่างไร
- ห้ามใช้เพื่อวัตถุประสงค์ในการฉ้อโกง
- ผู้เขียนไม่รับผิดชอบต่อการใช้งานในทางที่ผิด
- เคารพข้อกำหนดในการให้บริการของทุกแพลตฟอร์ม

---

## 🤝 การมีส่วนร่วม

ยินดีต้อนรับการมีส่วนร่วม! โปรดส่ง Pull Request

---

## 🦊 พันธมิตรอย่างเป็นทางการ: RoxyBrowser

🛡 **การป้องกันการตรวจจับ** — ลายนิ้วมือเฉพาะสำหรับแต่ละบัญชี ดูเหมือนอุปกรณ์จริงที่แตกต่างกัน

📉 **ป้องกันการเชื่อมโยง** — หยุด SheerID และแพลตฟอร์มจากการเชื่อมโยงบัญชีของคุณ

🚀 **เหมาะสำหรับผู้ใช้จำนวนมาก** — จัดการบัญชีที่ยืนยันแล้วหลายร้อยบัญชีอย่างปลอดภัย

[![ทดลองใช้ฟรี](https://img.shields.io/badge/ทดลองใช้ฟรี-RoxyBrowser-ff6b35?style=for-the-badge&logo=googlechrome&logoColor=white)](https://roxybrowser.com?code=01045PFA)

---

## ❤️ สนับสนุน

หากคุณพบว่าโครงการนี้มีประโยชน์ โปรดพิจารณาสนับสนุนฉัน:

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-ea4aaa?style=for-the-badge&logo=github)](https://github.com/sponsors/ThanhNguyxn)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/thanhnguyxn)

---

## 🌐 ภาษา

| 🇺🇸 [English](../README.md) | 🇻🇳 [Tiếng Việt](./README.vi.md) | 🇨🇳 [中文](./README.zh.md) | 🇯🇵 [日本語](./README.ja.md) | 🇰🇷 [한국어](./README.ko.md) |
|:---:|:---:|:---:|:---:|:---:|
| 🇪🇸 [Español](./README.es.md) | 🇫🇷 [Français](./README.fr.md) | 🇩🇪 [Deutsch](./README.de.md) | 🇧🇷 [Português](./README.pt-BR.md) | 🇷🇺 [Русский](./README.ru.md) |
| 🇸🇦 [العربية](./README.ar.md) | 🇮🇳 [हिन्दी](./README.hi.md) | 🇹🇭 [ไทย](./README.th.md) | 🇹🇷 [Türkçe](./README.tr.md) | 🇵🇱 [Polski](./README.pl.md) |
| 🇮🇹 [Italiano](./README.it.md) | 🇮🇩 [Bahasa Indonesia](./README.id.md) | | | |
