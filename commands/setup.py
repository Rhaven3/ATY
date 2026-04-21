"""
Commande `setup` — Assistant de configuration initiale.
Crée le fichier .env et guide l'utilisateur.
"""

import questionary
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from pathlib import Path
from config.config import CMD

console = Console()

STYLE = questionary.Style([
    ("question", "bold cyan"),
    ("answer", "bold white"),
    ("pointer", "cyan"),
    ("highlighted", "bold cyan"),
])


def run():
    console.print(Panel(
        "[cyan]Ce wizard va créer ton fichier [bold].env[/bold] de configuration.\n"
        "Tes données resteront locales sur ta machine.[/cyan]",
        title="[bold]Configuration initiale[/bold]",
        border_style="cyan",
    ))

    env_path = Path(".env")
    if env_path.exists():
        overwrite = questionary.confirm(
            "!! Un fichier .env existe déjà. L'écraser ?",
            default=False,
            style=STYLE,
        ).ask()
        if not overwrite:
            console.print("[yellow]Configuration annulée.[/yellow]")
            return

    console.print("\n[bold cyan]Ton profil[/bold cyan]")

    prenom = questionary.text("Prénom :", style=STYLE).ask()
    nom = questionary.text("Nom :", style=STYLE).ask()
    formation = questionary.text("Formation (ex: Bachelor Dev Web) :", style=STYLE).ask()
    formation_futur = questionary.text("Formation Futur (ex: Master: Expert Architecte Développeur ):", style=STYLE).ask()
    ecole = questionary.text("École / Université :", style=STYLE).ask()
    email = questionary.text("Email :", style=STYLE).ask()
    tel = questionary.text("Téléphone :", style=STYLE).ask()

    console.print("\n[bold cyan]Clés API & Google Sheets[/bold cyan]")
    console.print("[dim]→ Anthropic API Key : https://console.anthropic.com[/dim]")
    anthropic_key = questionary.text("Anthropic API Key :", style=STYLE).ask()

    console.print("\n[dim]→ Google Sheet ID : c'est l'ID dans l'URL de ton sheet[/dim]")
    console.print("[dim]   ex: docs.google.com/spreadsheets/d/[bold]TON_ID_ICI[/bold]/edit[/dim]")
    sheet_id = questionary.text("Google Sheet ID :", style=STYLE).ask()

    console.print("\n[dim]→ credentials.json : télécharge-le depuis Google Cloud Console[/dim]")
    creds_file = questionary.text(
        "Chemin vers credentials.json :",
        default="credentials.json",
        style=STYLE,
    ).ask()

    sheet_name = questionary.text(
        "Nom de l'onglet dans le sheet :",
        default="Candidatures",
        style=STYLE,
    ).ask()

    # Écriture du .env
    env_content = f"""# ================================
# Alternance Tracker — Configuration
# ================================

# === Ton profil ===
PRENOM="{prenom}"
NOM="{nom}"
FORMATION="{formation}"
FORMATION_FUTUR="{formation_futur}"
ECOLE="{ecole}"
EMAIL="{email}"
TEL="{tel}"

# === API Anthropic (Claude) ===
ANTHROPIC_API_KEY="{anthropic_key}"

# === Google Sheets ===
GOOGLE_SHEET_ID="{sheet_id}"
GOOGLE_CREDENTIALS_FILE="{creds_file}"
SHEET_NAME="{sheet_name}"
"""

    env_path.write_text(env_content, encoding="utf-8")

    console.print(f"\n[bold green]✅ Fichier .env créé avec succès ![/bold green]")
    console.print("\n[bold]Prochaines étapes :[/bold]")
    console.print(f"  [cyan]1.[/cyan] Place ton [bold]{creds_file}[/bold] dans le dossier [bold]config/[/bold] du projet")
    console.print("  [cyan]2.[/cyan] Partage ton Google Sheet avec l'email du compte de service")
    console.print(f"  [cyan]3.[/cyan] Lance [bold]{CMD} add[/bold] pour ajouter ta première candidature !")
    console.print()
