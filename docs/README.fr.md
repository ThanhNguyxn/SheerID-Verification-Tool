# 🔐 Outil de Vérification SheerID

[![GitHub Stars](https://img.shields.io/github/stars/ThanhNguyxn/SheerID-Verification-Tool?style=social)](https://github.com/ThanhNguyxn/SheerID-Verification-Tool/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

Une collection complète d'outils pour automatiser les flux de travail de vérification SheerID pour divers services (Spotify, YouTube, Google One, etc.).

---

## 🛠️ Outils Disponibles

| Outil | Type | Cible | Description |
|------|------|--------|-------------|
| [spotify-verify-tool](../spotify-verify-tool/) | 🎵 Étudiant | Spotify Premium | Vérification des étudiants universitaires |
| [youtube-verify-tool](../youtube-verify-tool/) | 🎬 Étudiant | YouTube Premium | Vérification des étudiants universitaires |
| [one-verify-tool](../one-verify-tool/) | 🤖 Étudiant | Gemini Advanced | Vérification Google One AI Premium |
| [boltnew-verify-tool](../boltnew-verify-tool/) | 👨‍🏫 Enseignant | Bolt.new | Vérification des enseignants (Université) |
| [k12-verify-tool](../k12-verify-tool/) | 🏫 K12 | ChatGPT Plus | Vérification des enseignants K12 (Lycée) |
| [veterans-verify-tool](../veterans-verify-tool/) | 🎖️ Militaire | Général | Vérification du statut militaire |
| [veterans-extension](../veterans-extension/) | 🧩 Chrome | Navigateur | Extension Chrome pour la vérification militaire |

### 🔗 Outils Externes

| Outil | Type | Description |
|------|------|-------------|
| [RoxyBrowser](https://roxybrowser.com?code=01045PFA) | 🦊 Browser | **Navigateur anti-détection** — Gérer plusieurs comptes vérifiés sans être banni |
| [SheerID Auto Verify](https://ip123.in/sheerid/?code=01045PFA) | 🔐 Web | **Outil de vérification automatique** — Vérification SheerID rapide et automatique |
| [SheerID Verification Bot](https://t.me/SheerID_Verification_bot?start=ref_LdPKPES3Ej) | 🤖 Bot | Bot Telegram de la communauté vietnamienne |
| [Auto SheerID Bot](https://t.me/auto_sheerid_bot?start=7762497789) | 🤖 Bot | Bot de vérification automatisé |
| [Student Card Generator](https://thanhnguyxn.github.io/student-card-generator/) | 🎓 Tool | Créer des cartes d'étudiant pour la vérification manuelle |
| [Payslip Generator](https://thanhnguyxn.github.io/payslip-generator/) | 💰 Tool | Générer des fiches de paie pour la vérification des enseignants |


---

## 🧠 Architecture et Logique de Base

Tous les outils Python de ce dépôt partagent une architecture commune optimisée pour des taux de réussite élevés.

### 1. Le Flux de Vérification (The Verification Flow)
Les outils suivent un processus standardisé en "Cascade" :
1.  **Génération de Données (Data Generation)** : Crée une identité réaliste (Nom, Date de naissance, Email) correspondant à la démographie cible.
2.  **Soumission (`collectStudentPersonalInfo`)** : Soumet les données à l'API SheerID.
3.  **Saut SSO (`DELETE /step/sso`)** : Étape cruciale. Contourne l'exigence de se connecter à un portail scolaire.
4.  **Téléchargement de Document (`docUpload`)** : Télécharge un document de preuve généré (Carte d'étudiant, Relevé de notes ou Badge d'enseignant).
5.  **Achèvement (`completeDocUpload`)** : Signale à SheerID que le téléchargement est terminé.

### 2. Stratégies Intelligentes (Intelligent Strategies)

#### 🎓 Stratégie Universitaire (Spotify, YouTube, Gemini)
- **Sélection Pondérée** : Utilise une liste organisée de **45+ Universités** (US, VN, JP, KR, etc.).
- **Suivi du Succès** : Les universités avec des taux de réussite plus élevés sont sélectionnées plus souvent.
- **Génération de Documents** : Génère des cartes d'étudiant réalistes avec des noms et des dates dynamiques.

#### 👨‍🏫 Stratégie Enseignant (Bolt.new)
- **Ciblage par Âge** : Génère des identités plus âgées (25-55 ans) pour correspondre à la démographie des enseignants.
- **Génération de Documents** : Crée des "Certificats d'Emploi" au lieu de cartes d'étudiant.
- **Endpoint** : Cible `collectTeacherPersonalInfo` au lieu des endpoints étudiants.

#### 🏫 Stratégie K12 (ChatGPT Plus)
- **Ciblage par Type d'École** : Cible spécifiquement les écoles avec `type: "K12"` (pas `HIGH_SCHOOL`).
- **Logique d'Auto-Validation (Auto-Pass)** : La vérification K12 est souvent **automatiquement approuvée** sans téléchargement de document si les informations de l'école et de l'enseignant correspondent.
- **Repli** : Si le téléchargement est requis, il génère un Badge d'Enseignant.

#### 🎖️ Stratégie Vétérans (ChatGPT Plus)
- **Éligibilité Stricte** : Cible les militaires en service actif ou les vétérans séparés au cours des **12 derniers mois**.
- **Vérification Officielle** : SheerID vérifie par rapport à la base de données DoD/DEERS.
- **Logique** : Utilise par défaut des dates de libération récentes pour maximiser les chances d'auto-approbation.

---

## 📋 Démarrage Rapide

### Prérequis
- Python 3.8+
- `pip`

### Installation

1.  **Cloner le dépôt :**
    ```bash
    git clone https://github.com/ThanhNguyxn/SheerID-Verification-Tool.git
    cd SheerID-Verification-Tool
    ```

2.  **Installer les dépendances :**
    ```bash
    pip install httpx Pillow
    ```

3.  **Exécuter un outil (ex : Spotify) :**
    ```bash
    cd spotify-verify-tool
    python main.py "YOUR_SHEERID_URL"
    ```

---

## ⚠️ Avertissement

Ce projet est à des fins **éducatives uniquement**. Les outils démontrent comment fonctionnent les systèmes de vérification et comment ils peuvent être testés.
- Ne pas utiliser à des fins frauduleuses.
- Les auteurs ne sont pas responsables de toute mauvaise utilisation.
- Respectez les Conditions d'Utilisation de toutes les plateformes.

---

## 🤝 Contribuer

Les contributions sont les bienvenues ! N'hésitez pas à soumettre une Pull Request.

---

## 🦊 Partenaire Officiel: RoxyBrowser

🛡 **Protection Anti-Détection** — Empreinte digitale unique pour chaque compte, ressemble à différents vrais appareils.

📉 **Empêcher le Lien** — Empêche SheerID et les plateformes de lier vos comptes.

🚀 **Idéal pour les Utilisateurs en Masse** — Gérez en toute sécurité des centaines de comptes vérifiés.

[![Essai Gratuit](https://img.shields.io/badge/Essai%20Gratuit-RoxyBrowser-ff6b35?style=for-the-badge&logo=googlechrome&logoColor=white)](https://roxybrowser.com?code=01045PFA)

---

## ❤️ Soutien

Si vous trouvez ce projet utile, pensez à me soutenir :

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-ea4aaa?style=for-the-badge&logo=github)](https://github.com/sponsors/ThanhNguyxn)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/thanhnguyxn)

---

## 🌐 Langues

| 🇺🇸 [English](../README.md) | 🇻🇳 [Tiếng Việt](./README.vi.md) | 🇨🇳 [中文](./README.zh.md) | 🇯🇵 [日本語](./README.ja.md) | 🇰🇷 [한국어](./README.ko.md) |
|:---:|:---:|:---:|:---:|:---:|
| 🇪🇸 [Español](./README.es.md) | 🇫🇷 [Français](./README.fr.md) | 🇩🇪 [Deutsch](./README.de.md) | 🇧🇷 [Português](./README.pt-BR.md) | 🇷🇺 [Русский](./README.ru.md) |
| 🇸🇦 [العربية](./README.ar.md) | 🇮🇳 [हिन्दी](./README.hi.md) | 🇹🇭 [ไทย](./README.th.md) | 🇹🇷 [Türkçe](./README.tr.md) | 🇵🇱 [Polski](./README.pl.md) |
| 🇮🇹 [Italiano](./README.it.md) | 🇮🇩 [Bahasa Indonesia](./README.id.md) | | | |
