"""
Commande `add` — Ajouter une nouvelle candidature via prompts interactifs.
"""

import questionary
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime
from config import STATUTS, COLONNES
from sheets import ajouter_candidature

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
    entreprise = questionary.text(
        "🏢  Nom de l'entreprise :",
        style=style,
    ).ask()

    if not entreprise:
        console.print("[red]Annulé.[/red]")
        return

    poste = questionary.text(
        "💼  Intitulé du poste :",
        style=style,
    ).ask()

    ville = questionary.text(
        "📍  Ville :",
        style=style,
    ).ask()

    secteur = questionary.text(
        "🏭  Secteur d'activité :",
        style=style,
    ).ask()

    url = questionary.text(
        "🔗  URL de l'offre (optionnel) :",
        style=style,
    ).ask()

    contact = questionary.text(
        "👤  Nom du contact RH (optionnel) :",
        style=style,
    ).ask()

    email_contact = questionary.text(
        "📧  Email du contact (optionnel) :",
        style=style,
    ).ask()

    statut = questionary.select(
        "📊  Statut actuel :",
        choices=STATUTS,
        style=style,
    ).ask()

    notes = questionary.text(
        "📝  Notes (optionnel) :",
        style=style,
    ).ask()

    # Construction de la ligne
    data = {
        "Date": datetime.now().strftime("%d/%m/%Y"),
        "Entreprise": entreprise,
        "Poste": poste,
        "Ville": ville,
        "Secteur": secteur,
        "URL offre": url or "",
        "Contact": contact or "",
        "Email contact": email_contact or "",
        "Statut": statut,
        "Notes": notes or "",
    }

    # Aperçu avant confirmation
    console.print()
    table = Table(show_header=False, border_style="cyan", padding=(0, 1))
    table.add_column("Champ", style="dim cyan")
    table.add_column("Valeur", style="white")

    for k, v in data.items():
        if v:
            table.add_row(k, v)

    console.print(Panel(table, title="[bold cyan]Récapitulatif[/bold cyan]", border_style="cyan"))

    confirmer = questionary.confirm(
        "✅  Enregistrer cette candidature ?",
        default=True,
        style=style,
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
        console.print(f"[red]❌ Erreur lors de l'enregistrement : {e}[/red]")
