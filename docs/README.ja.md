# 🔐 SheerID認証ツール

[![GitHub Stars](https://img.shields.io/github/stars/ThanhNguyxn/SheerID-Verification-Tool?style=social)](https://github.com/ThanhNguyxn/SheerID-Verification-Tool/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Documentation](https://img.shields.io/badge/Docs-Website-2ea44f?style=flat&logo=github&logoColor=white)](https://thanhnguyxn.github.io/SheerID-Verification-Tool/)

Spotify、YouTube、Google OneなどのSheerID認証ワークフローを自動化するための包括的なツールコレクション。

---

## 🛠️ 利用可能なツール

| ツール | タイプ | ターゲット | 説明 |
|------|------|--------|-------------|
| [spotify-verify-tool](../spotify-verify-tool/) | 🎵 学生 | Spotify Premium | 大学生認証 |
| [youtube-verify-tool](../youtube-verify-tool/) | 🎬 学生 | YouTube Premium | 大学生認証 |
| [one-verify-tool](../one-verify-tool/) | 🤖 学生 | Gemini Advanced | Google One AI Premium認証 |
| [boltnew-verify-tool](../boltnew-verify-tool/) | 👨‍🏫 教師 | Bolt.new | 教師認証（大学） |
| [canva-teacher-tool](../canva-teacher-tool/) | 🇬🇧 教師 | Canva Education | 英国教師認証 (K-12) |
| [k12-verify-tool](../k12-verify-tool/) | 🏫 K12 | ChatGPT Plus | K12教師認証（高校） |
| [veterans-verify-tool](../veterans-verify-tool/) | 🎖️ 軍隊 | 一般 | 軍人ステータス認証 |
| [veterans-extension](../veterans-extension/) | 🧩 Chrome | ブラウザ | 軍人認証用Chrome拡張機能 |

### 🔗 外部ツール

| ツール | タイプ | 説明 |
|------|------|-------------|
| [RoxyBrowser](https://roxybrowser.com?code=01045PFA) | 🦊 ブラウザ | **アンチ検出ブラウザ** — 複数の認証済みアカウントをBANなしで安全に管理 |
| [Check IP](https://ip123.in/en?code=01045PFA) | 🌐 ウェブ | **IP確認** — IPアドレスとプロキシステータスを確認 |
| [SheerID Verification Bot](https://t.me/SheerID_Verification_bot?start=ref_LdPKPES3Ej) | 🤖 ボット | 自動検証Telegramボット |
| [GPT Bot](https://t.me/vgptplusbot?start=ref_7762497789) | 🤖 ボット | 自動検証ボット |
| [Student Card Generator](https://thanhnguyxn.github.io/student-card-generator/) | 🎓 ツール | 手動認証用の学生証を作成 |
| [Payslip Generator](https://thanhnguyxn.github.io/payslip-generator/) | 💰 ツール | 教師認証用の給与明細を作成 |

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

#### 🛡️ アンチ検出モジュール
すべてのツールに `anti_detect.py` が含まれ、以下を提供します：
- **ランダムユーザーエージェント**: 10以上の実際のブラウザUA文字列（Chrome、Firefox、Edge、Safari）
- **ブラウザライクなヘッダー**: 適切な `sec-ch-ua`、`Accept-Language` など
- **TLSフィンガープリントスプーフィング**: `curl_cffi` を使用してChromeのJA3/JA4フィンガープリントを模倣
- **ランダム遅延**: 人間の行動を模倣するガンマ分布タイミング
- **スマートセッション**: 最適なHTTPライブラリを自動選択（curl_cffi > cloudscraper > httpx > requests）
- **NewRelicヘッダー**: SheerID API呼び出しに必要な追跡ヘッダー
- **セッションウォーミング**: 正当なブラウザセッションを確立するための事前認証リクエスト
- **メール生成**: 大学ドメインに一致するリアルな学生メールを作成
- **プロキシジオマッチング**: 一貫性のためにプロキシの場所を大学の国に合わせる
- **マルチブラウザ偽装**: Chrome、Edge、Safariのフィンガープリント間でローテーション

#### 📄 ドキュメント生成モジュール
新しい `doc_generator.py` は生成されたドキュメントのアンチ検出を提供します：
- **ノイズ注入**: テンプレート検出を避けるためのランダムピクセルノイズ
- **カラーバリエーション**: ユニークさのための6つの異なる配色
- **動的ポジショニング**: 要素位置の±3pxの変化
- **複数タイプ**: 学生証、成績証明書、教師バッジ
- **リアルな詳細**: ランダムなバーコード、QRコード、コースの成績

> [!WARNING]
> **APIベースのツールには固有の制限があります**
>
> SheerIDは以下を含む高度な検出を使用します：
> - **TLSフィンガープリンティング**: Python `requests`/`httpx` は検出可能な署名を持っています
> - **シグナルインテリジェンス**: IPアドレス、デバイス属性、メールの年齢分析
> - **AIドキュメントレビュー**: 偽造/テンプレートドキュメントを検出
>
> 最良の結果を得るには：**住宅用プロキシ** + TLSスプーフィング用の `curl_cffi` をインストールしてください。
> ブラウザ拡張機能は一般的にAPIツールよりも成功率が高いです。

> [!IMPORTANT]
> **Gemini/Google Oneは米国のみ（2026年1月以降）**
>
> `one-verify-tool` は米国のIPでのみ動作します。海外ユーザーは認証失敗が表示されます。

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

3.  **[オプション] 強化されたアンチ検出:**
    ```bash
    pip install curl_cffi cloudscraper
    ```
    - `curl_cffi`: TLSフィンガープリント（JA3/JA4）を偽装して本物のChromeのように見せる
    - `cloudscraper`: Cloudflare保護をバイパス

4.  **ツールを実行 (例: Spotify):**
    ```bash
    cd spotify-verify-tool
    python main.py "YOUR_SHEERID_URL"
    ```

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

## 🤝 貢献

貢献は大歓迎です！プルリクエストを送信してください。

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
