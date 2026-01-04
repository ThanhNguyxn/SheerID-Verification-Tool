# 🔐 SheerID सत्यापन उपकरण

[![GitHub Stars](https://img.shields.io/github/stars/ThanhNguyxn/SheerID-Verification-Tool?style=social)](https://github.com/ThanhNguyxn/SheerID-Verification-Tool/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

विभिन्न सेवाओं (Spotify, YouTube, Google One, आदि) के लिए SheerID सत्यापन वर्कफ़्लो को स्वचालित करने के लिए उपकरणों का एक व्यापक संग्रह।

---

## 🛠️ उपलब्ध उपकरण

| उपकरण | प्रकार | लक्ष्य | विवरण |
|------|------|--------|-------------|
| [spotify-verify-tool](../spotify-verify-tool/) | 🎵 छात्र | Spotify Premium | विश्वविद्यालय छात्र सत्यापन |
| [youtube-verify-tool](../youtube-verify-tool/) | 🎬 छात्र | YouTube Premium | विश्वविद्यालय छात्र सत्यापन |
| [one-verify-tool](../one-verify-tool/) | 🤖 छात्र | Gemini Advanced | Google One AI Premium सत्यापन |
| [boltnew-verify-tool](../boltnew-verify-tool/) | 👨‍🏫 शिक्षक | Bolt.new | शिक्षक सत्यापन (विश्वविद्यालय) |
| [k12-verify-tool](../k12-verify-tool/) | 🏫 K12 | ChatGPT Plus | K12 शिक्षक सत्यापन (हाई स्कूल) |
| [veterans-verify-tool](../veterans-verify-tool/) | 🎖️ सैन्य | सामान्य | सैन्य स्थिति सत्यापन |
| [veterans-extension](../veterans-extension/) | 🧩 Chrome | ब्राउज़र | सैन्य सत्यापन के लिए Chrome एक्सटेंशन |

### 🔗 बाहरी उपकरण

| उपकरण | प्रकार | विवरण |
|------|------|-------------|
| [SheerID VIP Bot](https://t.me/SheerID_VIP_Bot?start=ref_REF001124) | ⚡ Bot | तेज़ प्रसंस्करण के साथ वैकल्पिक टेलीग्राम बॉट |
| [SheerID VN Bot](https://t.me/sheeridvn_bot?start=invite_7762497789) | 🇻🇳 Bot | वियतनामी समुदाय टेलीग्राम बॉट |
| [Veterans Verify Bot](https://t.me/vgptplusbot?start=ref_7762497789) | 🎖️ Bot | सैन्य सत्यापन बॉट |
| [Batch 1Key.me](https://batch.1key.me/) | 📦 Web | कई URL के लिए बैच सत्यापन |
| [Student Card Generator](https://thanhnguyxn.github.io/student-card-generator/) | 🎓 Tool | मैन्युअल सत्यापन के लिए छात्र आईडी कार्ड बनाएं |
| [Payslip Generator](https://thanhnguyxn.github.io/payslip-generator/) | 💰 Tool | शिक्षक सत्यापन के लिए वेतन पर्ची बनाएं |
| [RoxyBrowser](https://roxybrowser.com?code=01045PFA) | 🦊 Browser | **एंटी-डिटेक्ट ब्राउज़र** — बैन हुए बिना कई सत्यापित खातों को सुरक्षित रूप से प्रबंधित करें |

---

## 🧠 मुख्य वास्तुकला और तर्क

इस रिपॉजिटरी में सभी Python उपकरण उच्च सफलता दर के लिए अनुकूलित एक सामान्य वास्तुकला साझा करते हैं।

### 1. सत्यापन प्रवाह (The Verification Flow)
उपकरण एक मानकीकृत "वाटरफॉल" प्रक्रिया का पालन करते हैं:
1.  **डेटा जनरेशन (Data Generation)**: एक यथार्थवादी पहचान (नाम, जन्म तिथि, ईमेल) बनाता है जो लक्ष्य जनसांख्यिकीय से मेल खाती है।
2.  **सबमिशन (`collectStudentPersonalInfo`)**: SheerID API को डेटा सबमिट करता है।
3.  **SSO स्किप (`DELETE /step/sso`)**: महत्वपूर्ण कदम। स्कूल पोर्टल में लॉग इन करने की आवश्यकता को बायपास करता है।
4.  **दस्तावेज़ अपलोड (`docUpload`)**: एक उत्पन्न प्रमाण दस्तावेज़ (छात्र आईडी, ट्रांसक्रिप्ट, या शिक्षक बैज) अपलोड करता है।
5.  **पूर्णता (`completeDocUpload`)**: SheerID को संकेत देता है कि अपलोड समाप्त हो गया है।

### 2. बुद्धिमान रणनीतियाँ (Intelligent Strategies)

#### 🎓 विश्वविद्यालय रणनीति (Spotify, YouTube, Gemini)
- **भारित चयन**: **45+ विश्वविद्यालयों** (यूएस, वीएन, जेपी, केआर, आदि) की एक क्यूरेटेड सूची का उपयोग करता है।
- **सफलता ट्रैकिंग**: उच्च सफलता दर वाले विश्वविद्यालयों को अधिक बार चुना जाता है।
- **दस्तावेज़ जनरेशन**: गतिशील नामों और तिथियों के साथ यथार्थवादी दिखने वाले छात्र आईडी कार्ड बनाता है।

#### 👨‍🏫 शिक्षक रणनीति (Bolt.new)
- **आयु लक्ष्यीकरण**: शिक्षक जनसांख्यिकी से मेल खाने के लिए पुरानी पहचान (25-55 वर्ष) उत्पन्न करता है।
- **दस्तावेज़ जनरेशन**: छात्र आईडी के बजाय "रोजगार प्रमाण पत्र" बनाता है।
- **एंडपॉइंट**: छात्र एंडपॉइंट के बजाय `collectTeacherPersonalInfo` को लक्षित करता है।

#### 🏫 K12 रणनीति (ChatGPT Plus)
- **स्कूल प्रकार लक्ष्यीकरण**: विशेष रूप से `type: "K12"` (न कि `HIGH_SCHOOL`) वाले स्कूलों को लक्षित करता है।
- **ऑटो-पास तर्क (Auto-Pass)**: यदि स्कूल और शिक्षक की जानकारी मेल खाती है, तो K12 सत्यापन अक्सर दस्तावेज़ अपलोड के बिना **स्वचालित रूप से स्वीकृत** हो जाता है।
- **फ़ॉलबैक**: यदि अपलोड की आवश्यकता होती है, तो यह एक शिक्षक बैज उत्पन्न करता है।

#### 🎖️ दिग्गजों की रणनीति (ChatGPT Plus)
- **सख्त पात्रता**: सक्रिय ड्यूटी सैन्य कर्मियों या **पिछले 12 महीनों** के भीतर छुट्टी पाने वाले दिग्गजों को लक्षित करता है।
- **आधिकारिक जाँच**: SheerID DoD/DEERS डेटाबेस के खिलाफ सत्यापित करता है।
- **तर्क**: स्वचालित अनुमोदन की संभावनाओं को अधिकतम करने के लिए डिफ़ॉल्ट रूप से हाल की डिस्चार्ज तिथियों का उपयोग करता है।

---

## 📋 त्वरित आरंभ

### पूर्वापेक्षाएँ
- Python 3.8+
- `pip`

### स्थापना

1.  **रिपॉजिटरी को क्लोन करें:**
    ```bash
    git clone https://github.com/ThanhNguyxn/SheerID-Verification-Tool.git
    cd SheerID-Verification-Tool
    ```

2.  **निर्भरताएँ स्थापित करें:**
    ```bash
    pip install httpx Pillow
    ```

3.  **उपकरण चलाएं (जैसे, Spotify):**
    ```bash
    cd spotify-verify-tool
    python main.py "YOUR_SHEERID_URL"
    ```

---

## ⚠️ अस्वीकरण

यह परियोजना केवल **शैक्षिक उद्देश्यों** के लिए है। उपकरण प्रदर्शित करते हैं कि सत्यापन प्रणाली कैसे काम करती है और उनका परीक्षण कैसे किया जा सकता है।
- धोखाधड़ी के उद्देश्यों के लिए उपयोग न करें।
- लेखक किसी भी दुरुपयोग के लिए जिम्मेदार नहीं हैं।
- सभी प्लेटफार्मों की सेवा की शर्तों का सम्मान करें।

---

## 🤝 योगदान

योगदान का स्वागत है! कृपया बेझिझक एक पुल अनुरोध सबमिट करें।

---

## 🦊 आधिकारिक भागीदार: RoxyBrowser

🛡 **एंटी-डिटेक्ट सुरक्षा** — प्रत्येक खाते के लिए अद्वितीय फ़िंगरप्रिंट, विभिन्न वास्तविक उपकरणों की तरह दिखता है।

📉 **लिंकेज रोकें** — SheerID और प्लेटफ़ॉर्म को आपके खातों को लिंक करने से रोकता है।

🚀 **बल्क उपयोगकर्ताओं के लिए आदर्श** — सैकड़ों सत्यापित खातों को सुरक्षित रूप से प्रबंधित करें।

[![मुफ्त में आज़माएं](https://img.shields.io/badge/मुफ्त%20में%20आज़माएं-RoxyBrowser-ff6b35?style=for-the-badge&logo=googlechrome&logoColor=white)](https://roxybrowser.com?code=01045PFA)

---

## ❤️ सहायता

यदि आपको यह परियोजना उपयोगी लगी, तो मुझे सहायता करने पर विचार करें:

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-ea4aaa?style=for-the-badge&logo=github)](https://github.com/sponsors/ThanhNguyxn)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/thanhnguyxn)

---

## 🌐 भाषाएँ

| 🇺🇸 [English](../README.md) | 🇻🇳 [Tiếng Việt](./README.vi.md) | 🇨🇳 [中文](./README.zh.md) | 🇯🇵 [日本語](./README.ja.md) | 🇰🇷 [한국어](./README.ko.md) |
|:---:|:---:|:---:|:---:|:---:|
| 🇪🇸 [Español](./README.es.md) | 🇫🇷 [Français](./README.fr.md) | 🇩🇪 [Deutsch](./README.de.md) | 🇧🇷 [Português](./README.pt-BR.md) | 🇷🇺 [Русский](./README.ru.md) |
| 🇸🇦 [العربية](./README.ar.md) | 🇮🇳 [हिन्दी](./README.hi.md) | 🇹🇭 [ไทย](./README.th.md) | 🇹🇷 [Türkçe](./README.tr.md) | 🇵🇱 [Polski](./README.pl.md) |
| 🇮🇹 [Italiano](./README.it.md) | 🇮🇩 [Bahasa Indonesia](./README.id.md) | | | |
