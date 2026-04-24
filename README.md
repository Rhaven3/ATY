# ATY CLI

**A**lternance **T**racker p**Y**thon

> Suis tes candidatures d'alternance dans Google Sheets et génère des lettres de motivation personnalisées via Claude AI — en quelques secondes depuis ton terminal.

---

## ✨ Fonctionnalités

| Commande | Description |
|---|---|
| `aty setup` | ⚙️ Configuration guidée (première utilisation) |
| `aty add` | ➕ Ajouter une candidature via prompts interactifs |
| `aty list` | 📋 Voir toutes tes candidatures avec statuts colorés |
| `aty lettre` | ✍️ Générer une lettre de motivation via Claude AI |
| `aty update` | 🔄 Mettre à jour le statut d'une candidature |

---

## 🚀 Installation

### 1. Cloner et installer les dépendances

```bash
git clone https://github.com/Rhaven3/ATY.git 
cd ATY

uv tool install .
```

### 2. Configurer Google Sheets

#### a) Créer un projet Google Cloud

1. Va sur [console.cloud.google.com](https://console.cloud.google.com)
2. Crée un nouveau projet (ex: "alternance-tracker")
3. Active l'**API Google Sheets** (Bibliothèque → chercher "Sheets")
4. Active l'**API Google Drive**

#### b) Créer un compte de service

1. IAM & Admin → **Comptes de service** → Créer
2. Donne-lui un nom (ex: "alternance-bot")
3. Clé → Ajouter une clé → JSON → Télécharger
4. Renomme le fichier en `credentials.json` et place-le dans le projet

#### c) Partager ton Google Sheet

1. Crée un Google Sheet (ou utilises-en un existant)
2. **Partage-le** avec l'email du compte de service (ex: `alternance-bot@ton-projet.iam.gserviceaccount.com`)
3. Donne-lui le rôle **Éditeur**
4. Copie l'ID du sheet depuis l'URL

### 3. Obtenir une clé API Anthropic

1. Va sur [console.anthropic.com](https://console.anthropic.com)
2. Crée une clé API
3. Note-la (elle ne s'affichera qu'une fois !)

### 4. Lancer le setup

```bash
aty setup
```

Le wizard te guide pour créer ton `.env` avec toutes les infos.

