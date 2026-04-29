"""
Configuration centrale du projet.
Les variables sont lues depuis .env (voir .env.example).
"""

import os
from pathlib import Path
from dotenv import load_dotenv

#  TEXT configuration
CMD = "aty"
CONFIG_DIR = Path.home() / ".config\\aty"
CONFIG_DIR_TEXT = "~/.config/aty/"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

# Charge le fichier .env depuis la racine du projet
load_dotenv(CONFIG_DIR / ".env")

# === Google Sheets ===
GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", f"{CONFIG_DIR}\credentials.json")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "")
SHEET_NAME = os.getenv("SHEET_NAME", "Candidatures")

# === Anthropic (Claude) ===
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = "claude-sonnet-4-6"

# === Ton profil (pour les lettres de motivation) ===
PRENOM = os.getenv("PRENOM", "")
NOM = os.getenv("NOM", "")
FORMATION = os.getenv("FORMATION", "")
FORMATION_FUTUR = os.getenv("FORMATION_FUTUR")
ECOLE = os.getenv("ECOLE", "")
EMAIL = os.getenv("EMAIL", "")
TEL = os.getenv("TEL", "")

# === Colonnes du Google Sheet ===
# Ordre des colonnes dans le sheet
COLONNES = [
    "Date",
    "Date Relance",
    "Intitulé",
    "Entreprise",
    "Secteur",
    "Taille",
    "Localisation",
    "Statut",
    "Lien",
    "Contact",
    "Email/Tel",
    "Note",
    "Plateforme"
]

STATUTS = [
    [
        "Postuler",
        "Relancer",
        "Entretien",
        "Refus",
        "Stage",
        "Accepté",
    ],
    [
        "blue",         
        "magenta",
        "cyan",
        "red",
        "white",
        "green"
    ]
]

PLATEFORMES = [
    "Indeed",
    "Linkedin",
    "Hellowork",
    "Welcome to the Jungle",
    "Aidostage.com",
    "La bonne boite",
    "Le POOL",
    "ADN Ouest",
    "Manageo"
    "Portail Entreprise",
    "Job Dating",
    "Autre",
]