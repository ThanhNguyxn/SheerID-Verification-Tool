# 🔐 Herramienta de Verificación SheerID

[![GitHub Stars](https://img.shields.io/github/stars/ThanhNguyxn/SheerID-Verification-Tool?style=social)](https://github.com/ThanhNguyxn/SheerID-Verification-Tool/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

Una colección completa de herramientas para automatizar los flujos de trabajo de verificación de SheerID para varios servicios (Spotify, YouTube, Google One, etc.).

---

## 🛠️ Herramientas Disponibles

| Herramienta | Tipo | Objetivo | Descripción |
|------|------|--------|-------------|
| [spotify-verify-tool](../spotify-verify-tool/) | 🎵 Estudiante | Spotify Premium | Verificación de estudiantes universitarios |
| [youtube-verify-tool](../youtube-verify-tool/) | 🎬 Estudiante | YouTube Premium | Verificación de estudiantes universitarios |
| [one-verify-tool](../one-verify-tool/) | 🤖 Estudiante | Gemini Advanced | Verificación de Google One AI Premium |
| [boltnew-verify-tool](../boltnew-verify-tool/) | 👨‍🏫 Profesor | Bolt.new | Verificación de profesores (Universidad) |
| [k12-verify-tool](../k12-verify-tool/) | 🏫 K12 | ChatGPT Plus | Verificación de profesores K12 (Escuela Secundaria) |
| [veterans-verify-tool](../veterans-verify-tool/) | 🎖️ Militar | General | Verificación de estatus militar |
| [veterans-extension](../veterans-extension/) | 🧩 Chrome | Navegador | Extensión de Chrome para verificación militar |

### 🔗 Herramientas Externas

| Herramienta | Tipo | Descripción |
|------|------|-------------|
| [RoxyBrowser](https://roxybrowser.com?code=01045PFA) | 🦊 Browser | **Navegador anti-detección** — Gestione múltiples cuentas verificadas sin ser baneado |
| [SheerID Auto Verify](https://ip123.in/sheerid/?code=01045PFA) | 🔐 Web | **Herramienta de verificación automática** — Verificación SheerID automática y rápida |
| [SheerID Verification Bot](https://t.me/SheerID_Verification_bot?start=ref_LdPKPES3Ej) | 🤖 Bot | Bot de Telegram de la comunidad vietnamita |
| [Auto SheerID Bot](https://t.me/auto_sheerid_bot?start=7762497789) | 🤖 Bot | Bot de verificación automatizado |
| [Student Card Generator](https://thanhnguyxn.github.io/student-card-generator/) | 🎓 Tool | Crear tarjetas de estudiante para verificación manual |
| [Payslip Generator](https://thanhnguyxn.github.io/payslip-generator/) | 💰 Tool | Generar nóminas para verificación de profesores |


---

## 🧠 Arquitectura y Lógica Principal

Todas las herramientas Python en este repositorio comparten una arquitectura común optimizada para altas tasas de éxito.

### 1. El Flujo de Verificación (The Verification Flow)
Las herramientas siguen un proceso estandarizado de "Cascada":
1.  **Generación de Datos (Data Generation)**: Crea una identidad realista (Nombre, Fecha de nacimiento, Email) que coincide con el grupo demográfico objetivo.
2.  **Envío (`collectStudentPersonalInfo`)**: Envía datos a la API de SheerID.
3.  **Omitir SSO (`DELETE /step/sso`)**: Paso crucial. Omite el requisito de iniciar sesión en un portal escolar.
4.  **Carga de Documentos (`docUpload`)**: Carga un documento de prueba generado (ID de estudiante, Transcripción o Insignia de profesor).
5.  **Finalización (`completeDocUpload`)**: Señala a SheerID que la carga ha finalizado.

### 2. Estrategias Inteligentes (Intelligent Strategies)

#### 🎓 Estrategia Universitaria (Spotify, YouTube, Gemini)
- **Selección Ponderada**: Utiliza una lista seleccionada de **45+ Universidades** (EE. UU., VN, JP, KR, etc.).
- **Seguimiento del Éxito**: Las universidades con tasas de éxito más altas se seleccionan con más frecuencia.
- **Generación de Documentos**: Genera tarjetas de identificación de estudiantes realistas con nombres y fechas dinámicos.

#### 👨‍🏫 Estrategia Docente (Bolt.new)
- **Segmentación por Edad**: Genera identidades mayores (25-55 años) para coincidir con la demografía de los profesores.
- **Generación de Documentos**: Crea "Certificados de Empleo" en lugar de identificaciones de estudiantes.
- **Endpoint**: Apunta a `collectTeacherPersonalInfo` en lugar de endpoints de estudiantes.

#### 🏫 Estrategia K12 (ChatGPT Plus)
- **Segmentación por Tipo de Escuela**: Apunta específicamente a escuelas con `type: "K12"` (no `HIGH_SCHOOL`).
- **Lógica de Aprobación Automática (Auto-Pass)**: La verificación K12 a menudo se **aprueba automáticamente** sin cargar documentos si la información de la escuela y el profesor coinciden.
- **Respaldo**: Si se requiere carga, genera una Insignia de Profesor.

#### 🎖️ Estrategia de Veteranos (ChatGPT Plus)
- **Elegibilidad Estricta**: Apunta a militares en servicio activo o veteranos separados dentro de los **últimos 12 meses**.
- **Verificación Autorizada**: SheerID verifica contra la base de datos DoD/DEERS.
- **Lógica**: Utiliza por defecto fechas de baja recientes para maximizar las posibilidades de aprobación automática.

---

## 📋 Inicio Rápido

### Requisitos previos
- Python 3.8+
- `pip`

### Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/ThanhNguyxn/SheerID-Verification-Tool.git
    cd SheerID-Verification-Tool
    ```

2.  **Instalar dependencias:**
    ```bash
    pip install httpx Pillow
    ```

3.  **Ejecutar una herramienta (ej. Spotify):**
    ```bash
    cd spotify-verify-tool
    python main.py "YOUR_SHEERID_URL"
    ```

---

## ⚠️ Descargo de Responsabilidad

Este proyecto es solo para **fines educativos**. Las herramientas demuestran cómo funcionan los sistemas de verificación y cómo se pueden probar.
- No utilizar para fines fraudulentos.
- Los autores no son responsables de ningún mal uso.
- Respete los Términos de Servicio de todas las plataformas.

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! No dude en enviar una Pull Request.

---

## 🦊 Socio Oficial: RoxyBrowser

🛡 **Protección Anti-Detección** — Huella digital única para cada cuenta, parecen dispositivos reales diferentes.

📉 **Prevenir Vinculación** — Impide que SheerID y las plataformas vinculen sus cuentas.

🚀 **Ideal para Usuarios Masivos** — Gestione de forma segura cientos de cuentas verificadas.

[![Prueba Gratis](https://img.shields.io/badge/Prueba%20Gratis-RoxyBrowser-ff6b35?style=for-the-badge&logo=googlechrome&logoColor=white)](https://roxybrowser.com?code=01045PFA)

---

## ⚠️ Descargo de Responsabilidad

Este proyecto es solo para **fines educativos**. Las herramientas demuestran cómo funcionan los sistemas de verificación y cómo se pueden probar.
- No utilizar para fines fraudulentos.
- Los autores no son responsables de ningún mal uso.
- Respete los Términos de Servicio de todas las plataformas.

---

## ❤️ Apoyo

Si encuentras útil este proyecto, considera apoyarme:

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-ea4aaa?style=for-the-badge&logo=github)](https://github.com/sponsors/ThanhNguyxn)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/thanhnguyxn)

---

## 🌐 Idiomas

| 🇺🇸 [English](../README.md) | 🇻🇳 [Tiếng Việt](./README.vi.md) | 🇨🇳 [中文](./README.zh.md) | 🇯🇵 [日本語](./README.ja.md) | 🇰🇷 [한국어](./README.ko.md) |
|:---:|:---:|:---:|:---:|:---:|
| 🇪🇸 [Español](./README.es.md) | 🇫🇷 [Français](./README.fr.md) | 🇩🇪 [Deutsch](./README.de.md) | 🇧🇷 [Português](./README.pt-BR.md) | 🇷🇺 [Русский](./README.ru.md) |
| 🇸🇦 [العربية](./README.ar.md) | 🇮🇳 [हिन्दी](./README.hi.md) | 🇹🇭 [ไทย](./README.th.md) | 🇹🇷 [Türkçe](./README.tr.md) | 🇵🇱 [Polski](./README.pl.md) |
| 🇮🇹 [Italiano](./README.it.md) | 🇮🇩 [Bahasa Indonesia](./README.id.md) | | | |
