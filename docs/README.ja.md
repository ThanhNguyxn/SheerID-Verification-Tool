# 🔐 SheerID認証ツール

[![GitHub Stars](https://img.shields.io/github/stars/ThanhNguyxn/SheerID-Verification-Tool?style=social)](https://github.com/ThanhNguyxn/SheerID-Verification-Tool/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

Spotify、YouTube、Google OneなどのSheerID認証ワークフローを自動化するための包括的なツールコレクション。

---

## 🛠️ 利用可能なツール

| ツール | タイプ | ターゲット | 説明 |
|------|------|--------|-------------|
| [spotify-verify-tool](../spotify-verify-tool/) | 🎵 学生 | Spotify Premium | 大学生認証 |
| [youtube-verify-tool](../youtube-verify-tool/) | 🎬 学生 | YouTube Premium | 大学生認証 |
| [one-verify-tool](../one-verify-tool/) | 🤖 学生 | Gemini Advanced | Google One AI Premium認証 |
| [boltnew-verify-tool](../boltnew-verify-tool/) | 👨‍🏫 教師 | Bolt.new | 教師認証（大学） |
| [k12-verify-tool](../k12-verify-tool/) | 🏫 K12 | ChatGPT Plus | K12教師認証（高校） |
| [veterans-verify-tool](../veterans-verify-tool/) | 🎖️ 軍隊 | 一般 | 軍人ステータス認証 |
| [veterans-extension](../veterans-extension/) | 🧩 Chrome | ブラウザ | 軍人認証用Chrome拡張機能 |

### 🔗 外部ツール

| ツール | タイプ | 説明 |
|------|------|-------------|
| [RoxyBrowser](https://roxybrowser.com?code=01045PFA) | 🦊 Browser | **アンチ検出ブラウザ** — 複数の認証済みアカウントをBANなしで安全に管理 |
| [SheerID Auto Verify](https://ip123.in/sheerid/?code=01045PFA) | 🔐 Web | **自動認証ツール** — 高速自動SheerID認証 |
| [SheerID Verification Bot](https://t.me/SheerID_Verification_bot?start=ref_LdPKPES3Ej) | 🤖 Bot | ベトナムコミュニティTelegramボット |
| [Auto SheerID Bot](https://t.me/auto_sheerid_bot?start=7762497789) | 🤖 Bot | 自動検証ボット |
| [Student Card Generator](https://thanhnguyxn.github.io/student-card-generator/) | 🎓 Tool | 手動認証用の学生証を作成 |
| [Payslip Generator](https://thanhnguyxn.github.io/payslip-generator/) | 💰 Tool | 教師認証用の給与明細を作成 |


---

## 🧠 コアアーキテクチャとロジック

このリポジトリ内のすべてのPythonツールは、高い成功率を実現するために最適化された共通のアーキテクチャを共有しています。

### 1. 認証フロー (The Verification Flow)
ツールは標準化された「ウォーターフォール」プロセスに従います：
1.  **データ生成 (Data Generation)**: ターゲット層に一致する現実的なID（名前、生年月日、メール）を作成します。
2.  **送信 (`collectStudentPersonalInfo`)**: データをSheerID APIに送信します。
3.  **SSOスキップ (`DELETE /step/sso`)**: 重要なステップ。学校のポータルにログインする要件を回避します。
4.  **ドキュメントアップロード (`docUpload`)**: 生成された証明書（学生証、成績証明書、または教師バッジ）をアップロードします。
5.  **完了 (`completeDocUpload`)**: アップロードが完了したことをSheerIDに通知します。

### 2. インテリジェント戦略 (Intelligent Strategies)

#### 🎓 大学戦略 (Spotify, YouTube, Gemini)
- **重み付き選択**: **45以上の大学**（米国、ベトナム、日本、韓国など）の厳選されたリストを使用します。
- **成功追跡**: 成功率の高い大学がより頻繁に選択されます。
- **ドキュメント生成**: 動的な名前と日付を持つリアルな学生証を生成します。

#### 👨‍🏫 教師戦略 (Bolt.new)
- **年齢ターゲティング**: 教師の人口統計に合わせて、より高い年齢（25〜55歳）のIDを生成します。
- **ドキュメント生成**: 学生証の代わりに「雇用証明書」を作成します。
- **エンドポイント**: 学生のエンドポイントではなく `collectTeacherPersonalInfo` をターゲットにします。

#### 🏫 K12戦略 (ChatGPT Plus)
- **学校タイプターゲティング**: `type: "K12"`（`HIGH_SCHOOL`ではない）の学校を具体的にターゲットにします。
- **自動パスロジック (Auto-Pass)**: 学校と教師の情報が一致する場合、K12認証はドキュメントのアップロードなしで**自動承認**されることがよくあります。
- **フォールバック**: アップロードが必要な場合は、教師バッジを生成します。

#### 🎖️ 退役軍人戦略 (ChatGPT Plus)
- **厳格な資格**: 現役軍人または**過去12か月以内**に除隊した退役軍人をターゲットにします。
- **権威あるチェック**: SheerIDはDoD/DEERSデータベースと照合して検証します。
- **ロジック**: 自動承認の可能性を最大化するために、デフォルトで最近の除隊日を使用します。

---

## 📋 クイックスタート

### 前提条件
- Python 3.8+
- `pip`

### インストール

1.  **リポジトリをクローン:**
    ```bash
    git clone https://github.com/ThanhNguyxn/SheerID-Verification-Tool.git
    cd SheerID-Verification-Tool
    ```

2.  **依存関係をインストール:**
    ```bash
    pip install httpx Pillow
    ```

3.  **ツールを実行 (例: Spotify):**
    ```bash
    cd spotify-verify-tool
    python main.py "YOUR_SHEERID_URL"
    ```

---

## ⚠️ 免責事項

このプロジェクトは**教育目的のみ**です。これらのツールは、認証システムがどのように機能し、どのようにテストできるかを示しています。
- 詐欺目的で使用しないでください。
- 作成者は誤用について一切の責任を負いません。
- すべてのプラットフォームの利用規約を尊重してください。

---

## 🤝 貢献

貢献は大歓迎です！プルリクエストを送信してください。

---

## 🦊 公式パートナー: RoxyBrowser

🛡 **アンチ検出保護** — 各アカウントに固有のフィンガープリントを持ち、異なる実際のデバイスのように見えます。

📉 **リンケージ防止** — SheerIDやプラットフォームがアカウントを関連付けることを阻止します。

🚀 **大量ユーザーに最適** — 数百の認証済みアカウントを安全に管理できます。

[![無料トライアル](https://img.shields.io/badge/無料トライアル-RoxyBrowser-ff6b35?style=for-the-badge&logo=googlechrome&logoColor=white)](https://roxybrowser.com?code=01045PFA)

---

## ⚠️ 免責事項

このプロジェクトは**教育目的のみ**です。これらのツールは、認証システムがどのように機能し、どのようにテストできるかを示しています。
- 詐欺目的で使用しないでください。
- 作成者は誤用について一切の責任を負いません。
- すべてのプラットフォームの利用規約を尊重してください。

---

## ❤️ サポート

このプロジェクトが役に立った場合は、サポートをご検討ください：

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-ea4aaa?style=for-the-badge&logo=github)](https://github.com/sponsors/ThanhNguyxn)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/thanhnguyxn)

---

## 🌐 言語

| 🇺🇸 [English](../README.md) | 🇻🇳 [Tiếng Việt](./README.vi.md) | 🇨🇳 [中文](./README.zh.md) | 🇯🇵 [日本語](./README.ja.md) | 🇰🇷 [한국어](./README.ko.md) |
|:---:|:---:|:---:|:---:|:---:|
| 🇪🇸 [Español](./README.es.md) | 🇫🇷 [Français](./README.fr.md) | 🇩🇪 [Deutsch](./README.de.md) | 🇧🇷 [Português](./README.pt-BR.md) | 🇷🇺 [Русский](./README.ru.md) |
| 🇸🇦 [العربية](./README.ar.md) | 🇮🇳 [हिन्दी](./README.hi.md) | 🇹🇭 [ไทย](./README.th.md) | 🇹🇷 [Türkçe](./README.tr.md) | 🇵🇱 [Polski](./README.pl.md) |
| 🇮🇹 [Italiano](./README.it.md) | 🇮🇩 [Bahasa Indonesia](./README.id.md) | | | |
