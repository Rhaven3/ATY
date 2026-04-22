"""
Commande `add` — Ajouter une nouvelle candidature via prompts interactifs.
"""

import questionary
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime
from config.config import STATUTS, COLONNES, PLATEFORMES
from config.sheets import ajouter_candidature

console = Console()


def run():
    console.print("\n[bold cyan]➕ Nouvelle candidature[/bold cyan]\n")

    style = questionary.Style([
        ("question", "bold cyan"),
        ("answer", "bold white"),
        ("pointer", "cyan"),
        ("highlighted", "bold cyan"),
        ("selected", "cyan"),
    ])

    # Collecte des infos via prompts interactifs
    entreprise: str = questionary.text(
        "Nom de l'entreprise :",
        style=style,
    ).ask()

    if not entreprise:
        console.print("[red]Annulé.[/red]")
        return

    poste: str = questionary.text(
        "Intitulé du poste :",
        style=style,
    ).ask()

    localisation: str = questionary.text(
        "Localisation :",
        style=style,
    ).ask()

    secteur: str = questionary.text(
        "Secteur d'activité :",
        style=style,
    ).ask()

    taille: str = questionary.text(
        "Taille de l'entreprise :",
        style=style,
    ).ask()

    url: str = questionary.text(
        "URL de l'offre :",
        style=style,
    ).ask()

    platform: str = questionary.select(
        "Plateforme :",
        choices=PLATEFORMES,
        style=style,
    ).ask()

    contact: str = questionary.text(
        "Nom du contact RH :",
        style=style,
    ).ask()

    email_tel_contact: str = questionary.text(
        "Email ou Tél du contact :",
        style=style,
    ).ask()

    statut: str = questionary.select(
        "Statut actuel :",
        choices=STATUTS[0],
        style=style,
    ).ask()

    notes: str = questionary.text(
        "Notes :",
        style=style,
    ).ask()

    # Construction de la ligne
    data = {
        f"{COLONNES[0]}": datetime.now().strftime("%d/%m/%Y"),
        f"{COLONNES[2]}": poste or "",
        f"{COLONNES[6]}": localisation or "",
        f"{COLONNES[3]}": entreprise or "",
        f"{COLONNES[4]}": secteur or "",
        f"{COLONNES[5]}": taille or "",
        f"{COLONNES[8]}": url or "",
        f"{COLONNES[9]}": contact or "",
        f"{COLONNES[10]}": email_tel_contact or "",
        f"{COLONNES[12]}": platform or "",
        f"{COLONNES[7]}": statut,
        f"{COLONNES[11]}": notes or "",
    }

    # Aperçu avant confirmation
    console.print()
    table = Table(show_header=False, border_style="cyan", padding=(0, 1))
    table.add_column("Champ", style="blue")
    table.add_column("Valeur", style="white")

    for k, v in data.items():
        if v:
            table.add_row(k, v)

    console.print(Panel(table, title="[bold cyan]Récapitulatif[/bold cyan]", border_style="cyan"))

    confirmer = questionary.confirm(
        "Enregistrer cette candidature ?",
        default=True,
    ).ask()

    if not confirmer:
        console.print("[yellow]Annulé.[/yellow]")
        return

    console.print("[dim]Enregistrement en cours...[/dim]")

    try:
        ligne = ajouter_candidature(data)
        console.print(
            f"\n[bold green]✅ Candidature enregistrée à la ligne {ligne} ![/bold green]"
        )
        console.print(
            f"[dim]Tu peux maintenant générer une lettre avec : "
            f"[bold]python main.py lettre[/bold][/dim]\n"
        )
    except Exception as e:
        console.print(f"[red]!! Erreur lors de l'enregistrement : {e}[/red]")
