"""
Configuration centrale du projet.
Les variables sont lues depuis .env (voir .env.example).
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Charge le fichier .env depuis la racine du projet
load_dotenv(Path(__file__).parent / ".env")

# === Google Sheets ===
GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "")
SHEET_NAME = os.getenv("SHEET_NAME", "Candidatures")

# === Anthropic (Claude) ===
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = "claude-opus-4-5"

# === Ton profil (pour les lettres de motivation) ===
TON_PRENOM = os.getenv("TON_PRENOM", "")
TON_NOM = os.getenv("TON_NOM", "")
TON_FORMATION = os.getenv("TON_FORMATION", "")
TON_ECOLE = os.getenv("TON_ECOLE", "")
TON_EMAIL = os.getenv("TON_EMAIL", "")
TON_TEL = os.getenv("TON_TEL", "")

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
    "Postuler",
    "Relancer",
    "Entretien",
    "Refus",
    "Stage",
    "Accepté",
]
