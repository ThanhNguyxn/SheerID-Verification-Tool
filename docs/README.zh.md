# 🔐 SheerID 验证工具

[![GitHub Stars](https://img.shields.io/github/stars/ThanhNguyxn/SheerID-Verification-Tool?style=social)](https://github.com/ThanhNguyxn/SheerID-Verification-Tool/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

用于自动化各种服务（Spotify、YouTube、Google One 等）的 SheerID 验证工作流程的综合工具集合。

---

## 🛠️ 可用工具

| 工具 | 类型 | 目标 | 描述 |
|------|------|--------|-------------|
| [spotify-verify-tool](../spotify-verify-tool/) | 🎵 学生 | Spotify Premium | 大学生验证 |
| [youtube-verify-tool](../youtube-verify-tool/) | 🎬 学生 | YouTube Premium | 大学生验证 |
| [one-verify-tool](../one-verify-tool/) | 🤖 学生 | Gemini Advanced | Google One AI Premium 验证 |
| [boltnew-verify-tool](../boltnew-verify-tool/) | 👨‍🏫 教师 | Bolt.new | 教师验证（大学） |
| [k12-verify-tool](../k12-verify-tool/) | 🏫 K12 | ChatGPT Plus | K12 教师验证（高中） |
| [veterans-verify-tool](../veterans-verify-tool/) | 🎖️ 军事 | 通用 | 军人身份验证 |
| [veterans-extension](../veterans-extension/) | 🧩 Chrome | 浏览器 | 用于军人验证的 Chrome 扩展 |

### 🔗 外部工具

| 工具 | 类型 | 描述 |
|------|------|-------------|
| [SheerID VIP Bot](https://t.me/SheerID_VIP_Bot?start=ref_REF001124) | ⚡ Bot | 处理速度更快的替代 Telegram 机器人 |
| [SheerID VN Bot](https://t.me/sheeridvn_bot?start=invite_7762497789) | 🇻🇳 Bot | 越南社区 Telegram 机器人 |
| [Veterans Verify Bot](https://t.me/vgptplusbot?start=ref_7762497789) | 🎖️ Bot | 军事验证机器人 |
| [Batch 1Key.me](https://batch.1key.me/) | 📦 Web | 多个 URL 的批量验证 |
| [Student Card Generator](https://thanhnguyxn.github.io/student-card-generator/) | 🎓 Tool | 创建用于手动验证的学生证 |
| [Payslip Generator](https://thanhnguyxn.github.io/payslip-generator/) | 💰 Tool | 生成用于教师验证的工资单 |
| [RoxyBrowser](https://roxybrowser.com?code=01045PFA) | 🦊 Browser | **反检测浏览器** — 安全管理多个已验证账户而不被封禁 |

---

## 🧠 核心架构与逻辑

此存储库中的所有 Python 工具都共享一个通用的、经过优化的架构，旨在实现高成功率。

### 1. 验证流程 (The Verification Flow)
这些工具遵循标准化的“瀑布”流程：
1.  **数据生成 (Data Generation)**：创建与目标人群匹配的真实身份（姓名、出生日期、电子邮件）。
2.  **提交 (`collectStudentPersonalInfo`)**：将数据提交给 SheerID API。
3.  **跳过 SSO (`DELETE /step/sso`)**：关键步骤。绕过登录学校门户的要求。
4.  **文档上传 (`docUpload`)**：上传生成的证明文件（学生证、成绩单或教师证）。
5.  **完成 (`completeDocUpload`)**：向 SheerID 发出上传完成的信号。

### 2. 智能策略 (Intelligent Strategies)

#### 🎓 大学策略 (Spotify, YouTube, Gemini)
- **加权选择**：使用包含 **45+ 所大学**（美国、越南、日本、韩国等）的精选列表。
- **成功追踪**：成功率较高的大学会被更频繁地选中。
- **文档生成**：生成带有动态姓名和日期的逼真学生证。

#### 👨‍🏫 教师策略 (Bolt.new)
- **年龄定位**：生成年龄较大（25-55 岁）的身份以匹配教师人群。
- **文档生成**：创建“在职证明”而不是学生证。
- **端点**：针对 `collectTeacherPersonalInfo` 而不是学生端点。

#### 🏫 K12 策略 (ChatGPT Plus)
- **学校类型定位**：专门针对 `type: "K12"`（而非 `HIGH_SCHOOL`）的学校。
- **自动通过逻辑 (Auto-Pass)**：如果学校和教师信息匹配，K12 验证通常会**自动批准**，无需上传文档。
- **后备方案**：如果需要上传，它会生成教师证。

#### 🎖️ 退伍军人策略 (ChatGPT Plus)
- **严格资格**：针对现役军人或在**过去 12 个月内**退伍的退伍军人。
- **权威检查**：SheerID 对照 DoD/DEERS 数据库进行验证。
- **逻辑**：默认使用最近的退伍日期，以最大限度地提高自动批准的机会。

---

## 📋 快速开始

### 先决条件
- Python 3.8+
- `pip`

### 安装

1.  **克隆存储库：**
    ```bash
    git clone https://github.com/ThanhNguyxn/SheerID-Verification-Tool.git
    cd SheerID-Verification-Tool
    ```

2.  **安装依赖项：**
    ```bash
    pip install httpx Pillow
    ```

3.  **运行工具（例如：Spotify）：**
    ```bash
    cd spotify-verify-tool
    python main.py "YOUR_SHEERID_URL"
    ```

---

## ⚠️ 免责声明

本项目仅供**教育目的**。这些工具演示了验证系统如何工作以及如何对其进行测试。
- 请勿用于欺诈目的。
- 作者不对任何滥用行为负责。
- 遵守所有平台的服务条款。

---

## 🤝 贡献

欢迎贡献！请随时提交 Pull Request。

---

## 🦊 官方合作伙伴: RoxyBrowser

🛡 **反检测保护** — 每个账户拥有独特的指纹，看起来像在不同的真实设备上。

📉 **防止关联** — 阻止 SheerID 和平台关联您的账户。

🚀 **适合批量用户** — 安全管理数百个已验证账户。

[![免费试用](https://img.shields.io/badge/免费试用-RoxyBrowser-ff6b35?style=for-the-badge&logo=googlechrome&logoColor=white)](https://roxybrowser.com?code=01045PFA)

---

## ❤️ 支持

如果您觉得这个项目有帮助，请考虑支持我：

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-ea4aaa?style=for-the-badge&logo=github)](https://github.com/sponsors/ThanhNguyxn)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/thanhnguyxn)

---

## 🌐 语言

| 🇺🇸 [English](../README.md) | 🇻🇳 [Tiếng Việt](./README.vi.md) | 🇨🇳 [中文](./README.zh.md) | 🇯🇵 [日本語](./README.ja.md) | 🇰🇷 [한국어](./README.ko.md) |
|:---:|:---:|:---:|:---:|:---:|
| 🇪🇸 [Español](./README.es.md) | 🇫🇷 [Français](./README.fr.md) | 🇩🇪 [Deutsch](./README.de.md) | 🇧🇷 [Português](./README.pt-BR.md) | 🇷🇺 [Русский](./README.ru.md) |
| 🇸🇦 [العربية](./README.ar.md) | 🇮🇳 [हिन्दी](./README.hi.md) | 🇹🇭 [ไทย](./README.th.md) | 🇹🇷 [Türkçe](./README.tr.md) | 🇵🇱 [Polski](./README.pl.md) |
| 🇮🇹 [Italiano](./README.it.md) | 🇮🇩 [Bahasa Indonesia](./README.id.md) | | | |
