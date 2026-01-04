# 🔐 Инструмент верификации SheerID

[![GitHub Stars](https://img.shields.io/github/stars/ThanhNguyxn/SheerID-Verification-Tool?style=social)](https://github.com/ThanhNguyxn/SheerID-Verification-Tool/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

Полный набор инструментов для автоматизации рабочих процессов верификации SheerID для различных сервисов (Spotify, YouTube, Google One и т.д.).

---

## 🛠️ Доступные инструменты

| Инструмент | Тип | Цель | Описание |
|------|------|--------|-------------|
| [spotify-verify-tool](../spotify-verify-tool/) | 🎵 Студент | Spotify Premium | Верификация студентов университетов |
| [youtube-verify-tool](../youtube-verify-tool/) | 🎬 Студент | YouTube Premium | Верификация студентов университетов |
| [one-verify-tool](../one-verify-tool/) | 🤖 Студент | Gemini Advanced | Верификация Google One AI Premium |
| [boltnew-verify-tool](../boltnew-verify-tool/) | 👨‍🏫 Учитель | Bolt.new | Верификация учителей (Университет) |
| [k12-verify-tool](../k12-verify-tool/) | 🏫 K12 | ChatGPT Plus | Верификация учителей K12 (Средняя школа) |
| [veterans-verify-tool](../veterans-verify-tool/) | 🎖️ Военный | Общее | Верификация военного статуса |
| [veterans-extension](../veterans-extension/) | 🧩 Chrome | Браузер | Расширение Chrome для военной верификации |

### 🔗 Внешние инструменты

| Инструмент | Тип | Описание |
|------|------|-------------|
| [SheerID VIP Bot](https://t.me/SheerID_VIP_Bot?start=ref_REF001124) | ⚡ Бот | Альтернативный Telegram-бот с более быстрой обработкой |
| [SheerID VN Bot](https://t.me/sheeridvn_bot?start=invite_7762497789) | 🇻🇳 Бот | Telegram-бот вьетнамского сообщества |
| [Veterans Verify Bot](https://t.me/vgptplusbot?start=ref_7762497789) | 🎖️ Бот | Бот для военной верификации |
| [Batch 1Key.me](https://batch.1key.me/) | 📦 Web | Пакетная верификация для нескольких URL |
| [Student Card Generator](https://thanhnguyxn.github.io/student-card-generator/) | 🎓 Tool | Создание студенческих билетов для ручной верификации |
| [Payslip Generator](https://thanhnguyxn.github.io/payslip-generator/) | 💰 Tool | Генерация расчетных листков для верификации учителей |
| [RoxyBrowser](https://roxybrowser.com?code=01045PFA) | 🦊 Browser | **Антидетект браузер** — Безопасное управление несколькими верифицированными аккаунтами без бана |

---

## 🧠 Основная архитектура и логика

Все инструменты Python в этом репозитории используют общую оптимизированную архитектуру, разработанную для достижения высоких показателей успеха.

### 1. Процесс верификации (The Verification Flow)
Инструменты следуют стандартизированному процессу "Водопад" (Waterfall):
1.  **Генерация данных (Data Generation)**: Создает реалистичную личность (Имя, Дата рождения, Email), соответствующую целевой демографии.
2.  **Отправка (`collectStudentPersonalInfo`)**: Отправляет данные в API SheerID.
3.  **Пропуск SSO (`DELETE /step/sso`)**: Критический шаг. Обходит требование входа на школьный портал.
4.  **Загрузка документов (`docUpload`)**: Загружает сгенерированный документ-подтверждение (Студенческий билет, Транскрипт или Удостоверение учителя).
5.  **Завершение (`completeDocUpload`)**: Сигнализирует SheerID о завершении загрузки.

### 2. Интеллектуальные стратегии (Intelligent Strategies)

#### 🎓 Университетская стратегия (Spotify, YouTube, Gemini)
- **Взвешенный выбор**: Использует отобранный список из **45+ университетов** (США, Вьетнам, Япония, Корея и т.д.).
- **Отслеживание успеха**: Университеты с более высокими показателями успеха выбираются чаще.
- **Генерация документов**: Генерирует реалистичные студенческие билеты с динамическими именами и датами.

#### 👨‍🏫 Стратегия для учителей (Bolt.new)
- **Таргетинг по возрасту**: Генерирует личности старшего возраста (25-55 лет) для соответствия демографии учителей.
- **Генерация документов**: Создает "Справки с места работы" вместо студенческих билетов.
- **Эндпоинт**: Нацелен на `collectTeacherPersonalInfo` вместо студенческих эндпоинтов.

#### 🏫 Стратегия K12 (ChatGPT Plus)
- **Таргетинг по типу школы**: Специально нацелен на школы с `type: "K12"` (не `HIGH_SCHOOL`).
- **Логика авто-пропуска (Auto-Pass)**: Верификация K12 часто **автоматически одобряется** без загрузки документов, если информация о школе и учителе совпадает.
- **Резерв**: Если требуется загрузка, генерирует удостоверение учителя.

#### 🎖️ Стратегия для ветеранов (ChatGPT Plus)
- **Строгая квалификация**: Нацелена на действующих военных или ветеранов, уволенных в течение **последних 12 месяцев**.
- **Авторитетная проверка**: SheerID проверяет по базе данных DoD/DEERS.
- **Логика**: По умолчанию использует недавние даты увольнения для максимизации шансов на автоматическое одобрение.

---

## 📋 Быстрый старт

### Предварительные требования
- Python 3.8+
- `pip`

### Установка

1.  **Клонировать репозиторий:**
    ```bash
    git clone https://github.com/ThanhNguyxn/SheerID-Verification-Tool.git
    cd SheerID-Verification-Tool
    ```

2.  **Установить зависимости:**
    ```bash
    pip install httpx Pillow
    ```

3.  **Запустить инструмент (например, Spotify):**
    ```bash
    cd spotify-verify-tool
    python main.py "YOUR_SHEERID_URL"
    ```

---

## ⚠️ Отказ от ответственности

Этот проект предназначен только для **образовательных целей**. Инструменты демонстрируют, как работают системы верификации и как их можно тестировать.
- Не используйте в мошеннических целях.
- Авторы не несут ответственности за любое неправильное использование.
- Соблюдайте Условия использования всех платформ.

---

## 🤝 Вклад

Вклад приветствуется! Пожалуйста, не стесняйтесь отправлять Pull Request.

---

## 🦊 Официальный Партнер: RoxyBrowser

🛡 **Защита от Обнаружения** — Уникальный отпечаток для каждого аккаунта, выглядит как разные реальные устройства.

📉 **Предотвращение Связывания** — Не позволяет SheerID и платформам связывать ваши аккаунты.

🚀 **Идеально для Массовых Пользователей** — Безопасно управляйте сотнями верифицированных аккаунтов.

[![Бесплатная Пробная Версия](https://img.shields.io/badge/Бесплатная%20Пробная-RoxyBrowser-ff6b35?style=for-the-badge&logo=googlechrome&logoColor=white)](https://roxybrowser.com?code=01045PFA)

---

## ❤️ Поддержка

Если вы нашли этот проект полезным, пожалуйста, поддержите меня:

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-ea4aaa?style=for-the-badge&logo=github)](https://github.com/sponsors/ThanhNguyxn)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/thanhnguyxn)

---

## 🌐 Языки

| 🇺🇸 [English](../README.md) | 🇻🇳 [Tiếng Việt](./README.vi.md) | 🇨🇳 [中文](./README.zh.md) | 🇯🇵 [日本語](./README.ja.md) | 🇰🇷 [한국어](./README.ko.md) |
|:---:|:---:|:---:|:---:|:---:|
| 🇪🇸 [Español](./README.es.md) | 🇫🇷 [Français](./README.fr.md) | 🇩🇪 [Deutsch](./README.de.md) | 🇧🇷 [Português](./README.pt-BR.md) | 🇷🇺 [Русский](./README.ru.md) |
| 🇸🇦 [العربية](./README.ar.md) | 🇮🇳 [हिन्दी](./README.hi.md) | 🇹🇭 [ไทย](./README.th.md) | 🇹🇷 [Türkçe](./README.tr.md) | 🇵🇱 [Polski](./README.pl.md) |
| 🇮🇹 [Italiano](./README.it.md) | 🇮🇩 [Bahasa Indonesia](./README.id.md) | | | |
