# 🎯 ATY CLI

**A**lternance **T**racker p**Y**thon

> Suis tes candidatures d'alternance dans Google Sheets et génère des lettres de motivation personnalisées via Claude AI — en quelques secondes depuis ton terminal.

---

## ✨ Fonctionnalités

| Commande | Description |
|---|---|
| `python main.py setup` | ⚙️ Configuration guidée (première utilisation) |
| `python main.py add` | ➕ Ajouter une candidature via prompts interactifs |
| `python main.py list` | 📋 Voir toutes tes candidatures avec statuts colorés |
| `python main.py lettre` | ✍️ Générer une lettre de motivation via Claude AI |
| `python main.py update` | 🔄 Mettre à jour le statut d'une candidature |

---

## 🚀 Installation

### 1. Cloner et installer les dépendances

```bash
git clone <ton-repo>
cd alternance-tracker

# Créer un environnement virtuel (recommandé)
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
# ou : .venv\Scripts\activate  # Windows

pip install -r requirements.txt
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
python main.py setup
```

Le wizard te guide pour créer ton `.env` avec toutes les infos.

---

## 📁 Structure du projet

```
alternance-tracker/
├── main.py              # Point d'entrée CLI
├── config.py            # Lecture des variables d'environnement
├── sheets.py            # Intégration Google Sheets (CRUD)
├── commands/
│   ├── add.py           # Ajouter une candidature
│   ├── list_cmd.py      # Lister les candidatures
│   ├── lettre.py        # Générer une lettre de motivation
│   ├── update.py        # Mettre à jour un statut
│   └── setup.py         # Assistant de configuration
├── requirements.txt
├── .env.example         # Template de configuration
├── .gitignore
└── README.md
```

---

## 🗂️ Structure du Google Sheet

Le sheet est créé automatiquement avec ces colonnes :

| Date | Entreprise | Poste | Ville | Secteur | URL offre | Contact | Email contact | Statut | Notes |
|---|---|---|---|---|---|---|---|---|---|

### Statuts disponibles

- `À envoyer` → `Envoyée` → `En attente` → `Relancé`
- `Entretien planifié` → `Entretien passé`
- `Refus` / `Accepté 🎉`

---

## 💡 Exemples d'utilisation

```bash
# Première fois
python main.py setup

# Ajouter une candidature chez Thales en alternance dev
python main.py add

# Voir toutes les candidatures
python main.py list

# Filtrer par statut
python main.py list --statut "En attente"

# Générer une lettre pour Thales
python main.py lettre

# Sauvegarder directement dans un fichier
python main.py lettre --output lettres/thales.txt

# Mettre à jour le statut après un entretien
python main.py update
```

---

## 🔒 Sécurité

- Le fichier `.env` et `credentials.json` sont dans le `.gitignore`
- **Ne committe jamais** ces fichiers sur GitHub
- Les données restent sur ton Google Sheet personnel

---

## 🛠️ Dépendances

| Package | Rôle |
|---|---|
| `typer` | Framework CLI avec sous-commandes |
| `rich` | Affichage coloré et tableaux dans le terminal |
| `questionary` | Prompts interactifs (select, text, confirm) |
| `gspread` | Lecture/écriture Google Sheets |
| `google-auth` | Authentification compte de service |
| `anthropic` | API Claude pour les lettres de motivation |
| `python-dotenv` | Lecture du fichier .env |
