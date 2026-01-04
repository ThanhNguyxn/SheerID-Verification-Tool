# 🔐 أداة التحقق SheerID

[![GitHub Stars](https://img.shields.io/github/stars/ThanhNguyxn/SheerID-Verification-Tool?style=social)](https://github.com/ThanhNguyxn/SheerID-Verification-Tool/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

مجموعة شاملة من الأدوات لأتمتة سير عمل التحقق من SheerID لمختلف الخدمات (Spotify و YouTube و Google One وما إلى ذلك).

---

## 🛠️ الأدوات المتاحة

| الأداة | النوع | الهدف | الوصف |
|------|------|--------|-------------|
| [spotify-verify-tool](../spotify-verify-tool/) | 🎵 طالب | Spotify Premium | التحقق من طالب جامعي |
| [youtube-verify-tool](../youtube-verify-tool/) | 🎬 طالب | YouTube Premium | التحقق من طالب جامعي |
| [one-verify-tool](../one-verify-tool/) | 🤖 طالب | Gemini Advanced | التحقق من Google One AI Premium |
| [boltnew-verify-tool](../boltnew-verify-tool/) | 👨‍🏫 معلم | Bolt.new | التحقق من المعلم (الجامعة) |
| [k12-verify-tool](../k12-verify-tool/) | 🏫 K12 | ChatGPT Plus | التحقق من معلم K12 (المدرسة الثانوية) |
| [veterans-verify-tool](../veterans-verify-tool/) | 🎖️ عسكري | عام | التحقق من الحالة العسكرية |
| [veterans-extension](../veterans-extension/) | 🧩 Chrome | متصفح | إضافة Chrome للتحقق العسكري |

### 🔗 أدوات خارجية

| الأداة | النوع | الوصف |
|------|------|-------------|
| [SheerID VIP Bot](https://t.me/SheerID_VIP_Bot?start=ref_REF001124) | ⚡ Bot | بوت Telegram بديل مع معالجة أسرع |
| [SheerID VN Bot](https://t.me/sheeridvn_bot?start=invite_7762497789) | 🇻🇳 Bot | بوت Telegram للمجتمع الفيتنامي |
| [Veterans Verify Bot](https://t.me/vgptplusbot?start=ref_7762497789) | 🎖️ Bot | بوت التحقق العسكري |
| [Batch 1Key.me](https://batch.1key.me/) | 📦 Web | التحقق المجمع لعناوين URL متعددة |
| [Student Card Generator](https://thanhnguyxn.github.io/student-card-generator/) | 🎓 Tool | إنشاء بطاقات هوية الطالب للتحقق اليدوي |
| [Payslip Generator](https://thanhnguyxn.github.io/payslip-generator/) | 💰 Tool | إنشاء قسائم رواتب للتحقق من المعلمين |
| [RoxyBrowser](https://roxybrowser.com?code=01045PFA) | 🦊 Browser | **متصفح مضاد للكشف** — إدارة حسابات متعددة تم التحقق منها بأمان دون حظر |

---

## 🧠 البنية الأساسية والمنطق

تشترك جميع أدوات Python في هذا المستودع في بنية مشتركة ومحسنة مصممة لتحقيق معدلات نجاح عالية.

### 1. تدفق التحقق (The Verification Flow)
تتبع الأدوات عملية "الشلال" (Waterfall) الموحدة:
1.  **توليد البيانات (Data Generation)**: إنشاء هوية واقعية (الاسم، تاريخ الميلاد، البريد الإلكتروني) تتطابق مع التركيبة السكانية المستهدفة.
2.  **الإرسال (`collectStudentPersonalInfo`)**: إرسال البيانات إلى SheerID API.
3.  **تخطي SSO (`DELETE /step/sso`)**: خطوة حاسمة. يتجاوز شرط تسجيل الدخول إلى بوابة المدرسة.
4.  **تحميل المستند (`docUpload`)**: تحميل مستند إثبات تم إنشاؤه (بطاقة هوية الطالب أو كشف الدرجات أو شارة المعلم).
5.  **الإكمال (`completeDocUpload`)**: إرسال إشارة إلى SheerID بأن التحميل قد انتهى.

### 2. الاستراتيجيات الذكية (Intelligent Strategies)

#### 🎓 استراتيجية الجامعة (Spotify, YouTube, Gemini)
- **الاختيار الموزون**: يستخدم قائمة منسقة تضم **45+ جامعة** (الولايات المتحدة، فيتنام، اليابان، كوريا، إلخ).
- **تتبع النجاح**: يتم اختيار الجامعات ذات معدلات النجاح الأعلى بشكل متكرر.
- **توليد المستندات**: إنشاء بطاقات هوية طلاب واقعية بأسماء وتواريخ ديناميكية.

#### 👨‍🏫 استراتيجية المعلم (Bolt.new)
- **استهداف العمر**: إنشاء هويات أقدم (25-55 عامًا) لتتناسب مع التركيبة السكانية للمعلمين.
- **توليد المستندات**: إنشاء "شهادات توظيف" بدلاً من بطاقات هوية الطالب.
- **نقطة النهاية**: يستهدف `collectTeacherPersonalInfo` بدلاً من نقاط نهاية الطالب.

#### 🏫 استراتيجية K12 (ChatGPT Plus)
- **استهداف نوع المدرسة**: يستهدف بشكل خاص المدارس ذات `type: "K12"` (وليس `HIGH_SCHOOL`).
- **منطق التمرير التلقائي (Auto-Pass)**: غالبًا ما يتم **الموافقة تلقائيًا** على التحقق من K12 دون تحميل مستند إذا تطابقت معلومات المدرسة والمعلم.
- **الاحتياطي**: إذا كان التحميل مطلوبًا، فإنه ينشئ شارة معلم.

#### 🎖️ استراتيجية المحاربين القدامى (ChatGPT Plus)
- **أهلية صارمة**: يستهدف الأفراد العسكريين في الخدمة الفعلية أو المحاربين القدامى الذين تم تسريحهم خلال **الـ 12 شهرًا الماضية**.
- **فحص موثوق**: يتحقق SheerID من قاعدة بيانات DoD/DEERS.
- **المنطق**: يستخدم تواريخ تسريح حديثة بشكل افتراضي لزيادة فرص الموافقة التلقائية.

---

## 📋 بداية سريعة

### المتطلبات الأساسية
- Python 3.8+
- `pip`

### التثبيت

1.  **استنساخ المستودع:**
    ```bash
    git clone https://github.com/ThanhNguyxn/SheerID-Verification-Tool.git
    cd SheerID-Verification-Tool
    ```

2.  **تثبيت التبعيات:**
    ```bash
    pip install httpx Pillow
    ```

3.  **تشغيل أداة (مثل Spotify):**
    ```bash
    cd spotify-verify-tool
    python main.py "YOUR_SHEERID_URL"
    ```

---

## ⚠️ إخلاء المسؤولية

هذا المشروع **للأغراض التعليمية فقط**. توضح الأدوات كيفية عمل أنظمة التحقق وكيف يمكن اختبارها.
- لا تستخدم لأغراض احتيالية.
- المؤلفون غير مسؤولين عن أي سوء استخدام.
- احترام شروط الخدمة لجميع المنصات.

---

## 🤝 المساهمة

المساهمات مرحب بها! لا تتردد في إرسال طلب سحب (Pull Request).

---

## 🦊 الشريك الرسمي: RoxyBrowser

🛡 **حماية ضد الكشف** — بصمة فريدة لكل حساب، تبدو كأجهزة حقيقية مختلفة.

📉 **منع الربط** — يمنع SheerID والمنصات من ربط حساباتك.

🚀 **مثالي للمستخدمين بكميات كبيرة** — إدارة مئات الحسابات المُتحقق منها بأمان.

[![تجربة مجانية](https://img.shields.io/badge/تجربة%20مجانية-RoxyBrowser-ff6b35?style=for-the-badge&logo=googlechrome&logoColor=white)](https://roxybrowser.com?code=01045PFA)

---

## ❤️ الدعم

إذا وجدت هذا المشروع مفيدًا، يرجى التفكير في دعمي:

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-ea4aaa?style=for-the-badge&logo=github)](https://github.com/sponsors/ThanhNguyxn)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/thanhnguyxn)

---

## 🌐 اللغات

| 🇺🇸 [English](../README.md) | 🇻🇳 [Tiếng Việt](./README.vi.md) | 🇨🇳 [中文](./README.zh.md) | 🇯🇵 [日本語](./README.ja.md) | 🇰🇷 [한국어](./README.ko.md) |
|:---:|:---:|:---:|:---:|:---:|
| 🇪🇸 [Español](./README.es.md) | 🇫🇷 [Français](./README.fr.md) | 🇩🇪 [Deutsch](./README.de.md) | 🇧🇷 [Português](./README.pt-BR.md) | 🇷🇺 [Русский](./README.ru.md) |
| 🇸🇦 [العربية](./README.ar.md) | 🇮🇳 [हिन्दी](./README.hi.md) | 🇹🇭 [ไทย](./README.th.md) | 🇹🇷 [Türkçe](./README.tr.md) | 🇵🇱 [Polski](./README.pl.md) |
| 🇮🇹 [Italiano](./README.it.md) | 🇮🇩 [Bahasa Indonesia](./README.id.md) | | | |
