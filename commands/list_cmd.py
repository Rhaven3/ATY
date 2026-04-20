"""
Commande `list` — Afficher toutes les candidatures dans un tableau.
"""

from rich.console import Console
from rich.table import Table
from rich.text import Text
from config.sheets import get_toutes_candidatures

console = Console()

STATUT_COLORS = {
    "À envoyer": "yellow",
    "Envoyée": "blue",
    "En attente": "cyan",
    "Relancé": "magenta",
    "Entretien planifié": "bold green",
    "Entretien passé": "green",
    "Refus": "red",
    "Accepté 🎉": "bold yellow",
}


def run(filtre_statut: str = None):
    console.print("\n[bold cyan]📋 Candidatures en cours[/bold cyan]\n")

    try:
        candidatures = get_toutes_candidatures()
    except Exception as e:
        console.print(f"[red]❌ Impossible de charger les candidatures : {e}[/red]")
        return

    if not candidatures:
        console.print("[yellow]Aucune candidature enregistrée pour l'instant.[/yellow]")
        console.print("[dim]Lance [bold]python main.py add[/bold] pour commencer ![/dim]")
        return

    # Filtrage optionnel
    if filtre_statut:
        candidatures = [c for c in candidatures if filtre_statut.lower() in c.get("Statut", "").lower()]
        if not candidatures:
            console.print(f"[yellow]Aucune candidature avec le statut '{filtre_statut}'.[/yellow]")
            return

    # Tableau rich
    table = Table(
        show_header=True,
        header_style="bold cyan",
        border_style="dim cyan",
        show_lines=True,
        expand=True,
    )

    table.add_column("#", style="dim", width=3)
    table.add_column("Date", style="dim white", width=10)
    table.add_column("Entreprise", style="bold white")
    table.add_column("Poste", style="white")
    table.add_column("Ville", style="dim white", width=12)
    table.add_column("Statut", width=20)
    table.add_column("Notes", style="dim white")

    for i, c in enumerate(candidatures, 1):
        statut = c.get("Statut", "")
        color = STATUT_COLORS.get(statut, "white")
        statut_text = Text(statut, style=color)

        table.add_row(
            str(i),
            c.get("Date", ""),
            c.get("Entreprise", ""),
            c.get("Poste", ""),
            c.get("Ville", ""),
            statut_text,
            c.get("Notes", "")[:40] + ("..." if len(c.get("Notes", "")) > 40 else ""),
        )

    console.print(table)

    # Stats rapides
    total = len(candidatures)
    entretiens = sum(1 for c in candidatures if "Entretien" in c.get("Statut", ""))
    acceptes = sum(1 for c in candidatures if "Accepté" in c.get("Statut", ""))
    refus = sum(1 for c in candidatures if c.get("Statut") == "Refus")

    console.print(
        f"\n[dim]Total : [bold white]{total}[/bold white] candidature(s) · "
        f"[green]{entretiens}[/green] entretien(s) · "
        f"[yellow]{acceptes}[/yellow] accepté(s) · "
        f"[red]{refus}[/red] refus[/dim]\n"
    )
