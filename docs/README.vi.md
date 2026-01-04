# 🔐 Công cụ Xác minh SheerID

[![GitHub Stars](https://img.shields.io/github/stars/ThanhNguyxn/SheerID-Verification-Tool?style=social)](https://github.com/ThanhNguyxn/SheerID-Verification-Tool/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

Một bộ công cụ toàn diện để tự động hóa quy trình xác minh SheerID cho các dịch vụ khác nhau (Spotify, YouTube, Google One, v.v.).

---

## 🛠️ Các Công Cụ Có Sẵn

| Công cụ | Loại | Mục tiêu | Mô tả |
|------|------|--------|-------------|
| [spotify-verify-tool](../spotify-verify-tool/) | 🎵 Sinh viên | Spotify Premium | Xác minh sinh viên đại học |
| [youtube-verify-tool](../youtube-verify-tool/) | 🎬 Sinh viên | YouTube Premium | Xác minh sinh viên đại học |
| [one-verify-tool](../one-verify-tool/) | 🤖 Sinh viên | Gemini Advanced | Xác minh Google One AI Premium |
| [boltnew-verify-tool](../boltnew-verify-tool/) | 👨‍🏫 Giáo viên | Bolt.new | Xác minh giáo viên (Đại học) |
| [k12-verify-tool](../k12-verify-tool/) | 🏫 K12 | ChatGPT Plus | Xác minh giáo viên K12 (Trung học) |
| [veterans-verify-tool](../veterans-verify-tool/) | 🎖️ Quân đội | Chung | Xác minh tình trạng quân nhân |
| [veterans-extension](../veterans-extension/) | 🧩 Chrome | Trình duyệt | Tiện ích Chrome xác minh quân nhân |

### 🔗 Công Cụ Bên Ngoài

| Công cụ | Loại | Mô tả |
|------|------|-------------|
| [SheerID VIP Bot](https://t.me/SheerID_VIP_Bot?start=ref_REF001124) | ⚡ Bot | Bot Telegram thay thế với tốc độ xử lý nhanh hơn |
| [SheerID VN Bot](https://t.me/sheeridvn_bot?start=invite_7762497789) | 🇻🇳 Bot | Bot Telegram cộng đồng Việt Nam |
| [Veterans Verify Bot](https://t.me/vgptplusbot?start=ref_7762497789) | 🎖️ Bot | Bot xác minh Quân đội |
| [Batch 1Key.me](https://batch.1key.me/) | 📦 Web | Xác minh hàng loạt cho nhiều URL |
| [Student Card Generator](https://thanhnguyxn.github.io/student-card-generator/) | 🎓 Tool | Tạo thẻ sinh viên để xác minh thủ công |
| [Payslip Generator](https://thanhnguyxn.github.io/payslip-generator/) | 💰 Tool | Tạo phiếu lương cho xác minh giáo viên |
| [RoxyBrowser](https://roxybrowser.com?code=01045PFA) | 🦊 Browser | **Trình duyệt chống phát hiện** — Quản lý nhiều tài khoản đã xác minh mà không bị cấm |

---

## 🧠 Kiến Trúc & Logic Cốt Lõi

Tất cả các công cụ Python trong kho lưu trữ này đều chia sẻ một kiến trúc chung, được tối ưu hóa để đạt tỷ lệ thành công cao.

### 1. Quy Trình Xác Minh (The Verification Flow)
Các công cụ tuân theo quy trình "Thác nước" (Waterfall) tiêu chuẩn:
1.  **Tạo Dữ Liệu (Data Generation)**: Tạo danh tính thực tế (Tên, Ngày sinh, Email) phù hợp với nhân khẩu học mục tiêu.
2.  **Gửi Thông Tin (`collectStudentPersonalInfo`)**: Gửi dữ liệu đến API SheerID.
3.  **Bỏ Qua SSO (`DELETE /step/sso`)**: Bước quan trọng. Bỏ qua yêu cầu đăng nhập vào cổng thông tin trường học.
4.  **Tải Lên Tài Liệu (`docUpload`)**: Tải lên tài liệu bằng chứng đã tạo (Thẻ sinh viên, Bảng điểm hoặc Thẻ giáo viên).
5.  **Hoàn Tất (`completeDocUpload`)**: Báo hiệu cho SheerID rằng quá trình tải lên đã xong.

### 2. Chiến Lược Thông Minh (Intelligent Strategies)

#### 🎓 Chiến Lược Đại Học (Spotify, YouTube, Gemini)
- **Lựa Chọn Có Trọng Số**: Sử dụng danh sách chọn lọc gồm **45+ Trường Đại Học** (Mỹ, VN, Nhật, Hàn, v.v.).
- **Theo Dõi Thành Công**: Các trường có tỷ lệ thành công cao hơn sẽ được chọn thường xuyên hơn.
- **Tạo Tài Liệu**: Tạo thẻ sinh viên trông như thật với tên và ngày tháng động.

#### 👨‍🏫 Chiến Lược Giáo Viên (Bolt.new)
- **Nhắm Mục Tiêu Độ Tuổi**: Tạo danh tính lớn tuổi hơn (25-55 tuổi) để phù hợp với nhân khẩu học giáo viên.
- **Tạo Tài Liệu**: Tạo "Giấy Chứng Nhận Việc Làm" thay vì Thẻ sinh viên.
- **Endpoint**: Nhắm mục tiêu `collectTeacherPersonalInfo` thay vì endpoint sinh viên.

#### 🏫 Chiến Lược K12 (ChatGPT Plus)
- **Nhắm Mục Tiêu Loại Trường**: Cụ thể nhắm vào các trường có `type: "K12"` (không phải `HIGH_SCHOOL`).
- **Logic Tự Động Duyệt (Auto-Pass)**: Xác minh K12 thường **tự động duyệt** mà không cần tải lên tài liệu nếu thông tin trường và giáo viên khớp.
- **Dự Phòng**: Nếu yêu cầu tải lên, nó sẽ tạo Thẻ Giáo Viên.

#### 🎖️ Chiến Lược Cựu Chiến Binh (ChatGPT Plus)
- **Điều Kiện Nghiêm Ngặt**: Nhắm mục tiêu Quân nhân Tại ngũ hoặc Cựu chiến binh đã xuất ngũ trong vòng **12 tháng qua**.
- **Kiểm Tra Chính Thức**: SheerID xác minh dựa trên cơ sở dữ liệu DoD/DEERS.
- **Logic**: Mặc định ngày xuất ngũ gần đây để tối đa hóa cơ hội tự động duyệt.

---

## 📋 Bắt Đầu Nhanh

### Yêu cầu
- Python 3.8+
- `pip`

### Cài đặt

1.  **Clone kho lưu trữ:**
    ```bash
    git clone https://github.com/ThanhNguyxn/SheerID-Verification-Tool.git
    cd SheerID-Verification-Tool
    ```

2.  **Cài đặt các thư viện phụ thuộc:**
    ```bash
    pip install httpx Pillow
    ```

3.  **Chạy công cụ (ví dụ: Spotify):**
    ```bash
    cd spotify-verify-tool
    python main.py "YOUR_SHEERID_URL"
    ```

---

## 🦊 Đối Tác Chính Thức: RoxyBrowser

🛡 **Chống Phát Hiện** — Mỗi tài khoản có fingerprint riêng biệt, trông như trên các thiết bị khác nhau.

📉 **Ngăn Liên Kết** — Ngăn SheerID và các nền tảng liên kết các tài khoản của bạn.

🚀 **Lý Tưởng Cho Người Dùng Số Lượng Lớn** — Quản lý an toàn hàng trăm tài khoản đã xác minh.

[![Dùng thử miễn phí](https://img.shields.io/badge/Dùng%20thử%20miễn%20phí-RoxyBrowser-ff6b35?style=for-the-badge&logo=googlechrome&logoColor=white)](https://roxybrowser.com?code=01045PFA)

---

## ⚠️ Tuyên Bố Miễn Trừ Trách Nhiệm

Dự án này chỉ dành cho **mục đích giáo dục**. Các công cụ minh họa cách hệ thống xác minh hoạt động và cách chúng có thể được kiểm thử.
- Không sử dụng cho mục đích gian lận.
- Các tác giả không chịu trách nhiệm về bất kỳ việc sử dụng sai mục đích nào.
- Tôn trọng Điều khoản Dịch vụ của tất cả các nền tảng.

---

## 🤝 Đóng Góp

Hoan nghênh mọi đóng góp! Vui lòng gửi Pull Request.

---

## ❤️ Ủng Hộ

Nếu bạn thấy dự án này hữu ích, hãy cân nhắc ủng hộ tôi:

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-ea4aaa?style=for-the-badge&logo=github)](https://github.com/sponsors/ThanhNguyxn)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/thanhnguyxn)

---

## 🌐 Ngôn Ngữ

| 🇺🇸 [English](../README.md) | 🇻🇳 [Tiếng Việt](./README.vi.md) | 🇨🇳 [中文](./README.zh.md) | 🇯🇵 [日本語](./README.ja.md) | 🇰🇷 [한국어](./README.ko.md) |
|:---:|:---:|:---:|:---:|:---:|
| 🇪🇸 [Español](./README.es.md) | 🇫🇷 [Français](./README.fr.md) | 🇩🇪 [Deutsch](./README.de.md) | 🇧🇷 [Português](./README.pt-BR.md) | 🇷🇺 [Русский](./README.ru.md) |
| 🇸🇦 [العربية](./README.ar.md) | 🇮🇳 [हिन्दी](./README.hi.md) | 🇹🇭 [ไทย](./README.th.md) | 🇹🇷 [Türkçe](./README.tr.md) | 🇵🇱 [Polski](./README.pl.md) |
| 🇮🇹 [Italiano](./README.it.md) | 🇮🇩 [Bahasa Indonesia](./README.id.md) | | | |
