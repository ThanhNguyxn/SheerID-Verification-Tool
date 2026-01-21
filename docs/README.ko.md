# 🔐 SheerID 인증 도구

[![GitHub Stars](https://img.shields.io/github/stars/ThanhNguyxn/SheerID-Verification-Tool?style=social)](https://github.com/ThanhNguyxn/SheerID-Verification-Tool/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Documentation](https://img.shields.io/badge/Docs-Website-2ea44f?style=flat&logo=github&logoColor=white)](https://thanhnguyxn.github.io/SheerID-Verification-Tool/)

다양한 서비스(Spotify, YouTube, Google One 등)를 위한 SheerID 인증 워크플로를 자동화하는 포괄적인 도구 모음입니다.

---

## 🛠️ 사용 가능한 도구

| 도구 | 유형 | 대상 | 설명 |
|------|------|--------|-------------|
| [spotify-verify-tool](../spotify-verify-tool/) | 🎵 학생 | Spotify Premium | 대학생 인증 |
| [youtube-verify-tool](../youtube-verify-tool/) | 🎬 학생 | YouTube Premium | 대학생 인증 |
| [one-verify-tool](../one-verify-tool/) | 🤖 학생 | Gemini Advanced | Google One AI Premium 인증 |
| [boltnew-verify-tool](../boltnew-verify-tool/) | 👨‍🏫 교사 | Bolt.new | 교사 인증 (대학교) |
| [canva-teacher-tool](../canva-teacher-tool/) | 🇬🇧 교사 | Canva Education | 영국 교사 인증 (K-12) |
| [k12-verify-tool](../k12-verify-tool/) | 🏫 K12 | ChatGPT Plus | K12 교사 인증 (고등학교) |
| [veterans-verify-tool](../veterans-verify-tool/) | 🎖️ 군인 | 일반 | 군인 신분 인증 |
| [veterans-extension](../veterans-extension/) | 🧩 Chrome | 브라우저 | 군인 인증용 Chrome 확장 프로그램 |

### 🔗 외부 도구

| 도구 | 유형 | 설명 |
|------|------|-------------|
| [RoxyBrowser](https://roxybrowser.com?code=01045PFA) | 🦊 브라우저 | **안티 탐지 브라우저** — 밴 없이 여러 인증된 계정을 안전하게 관리 |
| [Check IP](https://ip123.in/en?code=01045PFA) | 🌐 웹 | **IP 확인** — IP 주소 및 프록시 상태 확인 |
| [SheerID Verification Bot](https://t.me/SheerID_Verification_bot?start=ref_LdPKPES3Ej) | 🤖 봇 | 자동 인증 텔레그램 봇 |
| [GPT Bot](https://t.me/vgptplusbot?start=ref_7762497789) | 🤖 봇 | 자동 인증 봇 |
| [Student Card Generator](https://thanhnguyxn.github.io/student-card-generator/) | 🎓 도구 | 수동 인증용 학생증 생성 |
| [Payslip Generator](https://thanhnguyxn.github.io/payslip-generator/) | 💰 도구 | 교사 인증용 급여 명세서 생성 |

---

## 🧠 핵심 아키텍처 및 로직

이 리포지토리의 모든 Python 도구는 높은 성공률을 위해 최적화된 공통 아키텍처를 공유합니다.

### 1. 인증 흐름 (The Verification Flow)
도구는 표준화된 "폭포수(Waterfall)" 프로세스를 따릅니다:
1.  **데이터 생성 (Data Generation)**: 목표 인구 통계와 일치하는 현실적인 신원(이름, 생년월일, 이메일)을 생성합니다.
2.  **제출 (`collectStudentPersonalInfo`)**: SheerID API에 데이터를 제출합니다.
3.  **SSO 건너뛰기 (`DELETE /step/sso`)**: 중요한 단계. 학교 포털에 로그인해야 하는 요구 사항을 우회합니다.
4.  **문서 업로드 (`docUpload`)**: 생성된 증빙 문서(학생증, 성적 증명서 또는 교사 배지)를 업로드합니다.
5.  **완료 (`completeDocUpload`)**: 업로드가 완료되었음을 SheerID에 알립니다.

### 2. 지능형 전략 (Intelligent Strategies)

#### 🎓 대학 전략 (Spotify, YouTube, Gemini)
- **가중치 선택**: **45개 이상의 대학**(미국, 베트남, 일본, 한국 등)으로 구성된 선별된 목록을 사용합니다.
- **성공 추적**: 성공률이 높은 대학이 더 자주 선택됩니다.
- **문서 생성**: 동적 이름과 날짜가 포함된 사실적인 학생증을 생성합니다.

#### 👨‍🏫 교사 전략 (Bolt.new)
- **연령 타겟팅**: 교사 인구 통계에 맞게 더 나이 든 신원(25-55세)을 생성합니다.
- **문서 생성**: 학생증 대신 "재직 증명서"를 생성합니다.
- **엔드포인트**: 학생 엔드포인트 대신 `collectTeacherPersonalInfo`를 타겟팅합니다.

#### 🏫 K12 전략 (ChatGPT Plus)
- **학교 유형 타겟팅**: `type: "K12"`(`HIGH_SCHOOL` 아님)인 학교를 구체적으로 타겟팅합니다.
- **자동 통과 로직 (Auto-Pass)**: 학교와 교사 정보가 일치하면 K12 인증은 문서 업로드 없이 **자동 승인**되는 경우가 많습니다.
- **대체**: 업로드가 필요한 경우 교사 배지를 생성합니다.

#### 🎖️ 재향 군인 전략 (ChatGPT Plus)
- **엄격한 자격**: 현역 군인 또는 **지난 12개월 이내**에 전역한 재향 군인을 타겟팅합니다.
- **권위 있는 확인**: SheerID는 DoD/DEERS 데이터베이스와 대조하여 확인합니다.
- **로직**: 자동 승인 기회를 극대화하기 위해 기본적으로 최근 전역 날짜를 사용합니다.

#### 🛡️ 안티 탐지 모듈
모든 도구에는 `anti_detect.py`가 포함되어 다음을 제공합니다:
- **랜덤 User-Agent**: 10개 이상의 실제 브라우저 UA 문자열 (Chrome, Firefox, Edge, Safari)
- **브라우저 유사 헤더**: 적절한 `sec-ch-ua`, `Accept-Language` 등
- **TLS 핑거프린트 스푸핑**: `curl_cffi`를 사용하여 Chrome의 JA3/JA4 핑거프린트 모방
- **랜덤 지연**: 인간 행동을 모방하는 감마 분포 타이밍
- **스마트 세션**: 최적의 HTTP 라이브러리 자동 선택 (curl_cffi > cloudscraper > httpx > requests)
- **NewRelic 헤더**: SheerID API 호출에 필요한 추적 헤더
- **세션 워밍**: 정상적인 브라우저 세션을 설정하기 위한 사전 인증 요청
- **이메일 생성**: 대학 도메인과 일치하는 현실적인 학생 이메일 생성
- **프록시 지리 매칭**: 일관성을 위해 프록시 위치를 대학 국가와 매칭
- **멀티 브라우저 위장**: Chrome, Edge, Safari 핑거프린트 간 로테이션

#### 📄 문서 생성 모듈
새로운 `doc_generator.py`는 생성된 문서에 대한 안티 탐지를 제공합니다:
- **노이즈 주입**: 템플릿 탐지를 피하기 위한 랜덤 픽셀 노이즈
- **색상 변형**: 고유성을 위한 6가지 다른 색상 구성
- **동적 위치 지정**: 요소 위치의 ±3px 변화
- **다양한 유형**: 학생증, 성적 증명서, 교사 배지
- **현실적인 세부 사항**: 랜덤 바코드, QR 코드, 과목 성적

> [!WARNING]
> **API 기반 도구에는 고유한 제한 사항이 있습니다**
>
> SheerID는 다음을 포함한 고급 탐지를 사용합니다:
> - **TLS 핑거프린팅**: Python `requests`/`httpx`는 탐지 가능한 서명을 가지고 있습니다
> - **신호 정보**: IP 주소, 장치 속성, 이메일 연령 분석
> - **AI 문서 검토**: 위조/템플릿 문서 탐지
>
> 최상의 결과를 위해: **주거용 프록시** + TLS 스푸핑을 위한 `curl_cffi` 설치를 권장합니다.
> 브라우저 확장 프로그램은 일반적으로 API 도구보다 성공률이 높습니다.

> [!IMPORTANT]
> **Gemini/Google One은 미국에서만 사용 가능 (2026년 1월 이후)**
>
> `one-verify-tool`은 미국 IP에서만 작동합니다. 해외 사용자는 인증 실패가 표시됩니다.

---

## 📋 빠른 시작

### 필수 조건
- Python 3.8+
- `pip`

### 설치

1.  **리포지토리 복제:**
    ```bash
    git clone https://github.com/ThanhNguyxn/SheerID-Verification-Tool.git
    cd SheerID-Verification-Tool
    ```

2.  **의존성 설치:**
    ```bash
    pip install httpx Pillow
    ```

3.  **[선택 사항] 강화된 안티 탐지:**
    ```bash
    pip install curl_cffi cloudscraper
    ```
    - `curl_cffi`: TLS 핑거프린트(JA3/JA4)를 스푸핑하여 실제 Chrome처럼 보이게 함
    - `cloudscraper`: Cloudflare 보호 우회

4.  **도구 실행 (예: Spotify):**
    ```bash
    cd spotify-verify-tool
    python main.py "YOUR_SHEERID_URL"
    ```

---

## 🦊 공식 파트너: RoxyBrowser

🛡 **안티 탐지 보호** — 각 계정마다 고유한 핑거프린트를 가지며, 다른 실제 기기처럼 보입니다.

📉 **연결 방지** — SheerID와 플랫폼이 계정을 연결하는 것을 방지합니다.

🚀 **대량 사용자에 적합** — 수백 개의 인증된 계정을 안전하게 관리합니다.

[![무료 체험](https://img.shields.io/badge/무료%20체험-RoxyBrowser-ff6b35?style=for-the-badge&logo=googlechrome&logoColor=white)](https://roxybrowser.com?code=01045PFA)

---

## ⚠️ 면책 조항

이 프로젝트는 **교육 목적으로만** 제공됩니다. 이 도구는 인증 시스템의 작동 방식과 테스트 방법을 보여줍니다.
- 사기 목적으로 사용하지 마십시오.
- 작성자는 오용에 대해 책임을 지지 않습니다.
- 모든 플랫폼의 서비스 약관을 준수하십시오.

---

## 🤝 기여

기여는 언제나 환영합니다! Pull Request를 보내주세요.

---

## ❤️ 후원

이 프로젝트가 도움이 되었다면 후원을 고려해 주세요:

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-ea4aaa?style=for-the-badge&logo=github)](https://github.com/sponsors/ThanhNguyxn)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/thanhnguyxn)

---

## 🌐 언어

| 🇺🇸 [English](../README.md) | 🇻🇳 [Tiếng Việt](./README.vi.md) | 🇨🇳 [中文](./README.zh.md) | 🇯🇵 [日本語](./README.ja.md) | 🇰🇷 [한국어](./README.ko.md) |
|:---:|:---:|:---:|:---:|:---:|
| 🇪🇸 [Español](./README.es.md) | 🇫🇷 [Français](./README.fr.md) | 🇩🇪 [Deutsch](./README.de.md) | 🇧🇷 [Português](./README.pt-BR.md) | 🇷🇺 [Русский](./README.ru.md) |
| 🇸🇦 [العربية](./README.ar.md) | 🇮🇳 [हिन्दी](./README.hi.md) | 🇹🇭 [ไทย](./README.th.md) | 🇹🇷 [Türkçe](./README.tr.md) | 🇵🇱 [Polski](./README.pl.md) |
| 🇮🇹 [Italiano](./README.it.md) | 🇮🇩 [Bahasa Indonesia](./README.id.md) | | | |
