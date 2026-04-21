"""
Commande `list` — Afficher toutes les candidatures dans un tableau.
"""

from rich.console import Console
from rich.table import Table
from rich.text import Text
from config.sheets import get_toutes_candidatures
from config.config import CMD, STATUTS, COLONNES

console = Console()

def run(filtre_statut: str = None):
    console.print("\n[bold cyan]Candidatures en cours[/bold cyan]\n")

    try:
        candidatures = get_toutes_candidatures()
    except Exception as e:
        console.print(f"[red]!! Impossible de charger les candidatures : {e}[/red]")
        return

    if not candidatures:
        console.print("[yellow]Aucune candidature enregistrée pour l'instant.[/yellow]")
        console.print(f"[dim]Lance [bold]{CMD} add[/bold] pour commencer ![/dim]")
        return

    # Filtrage optionnel
    if filtre_statut:
        candidatures = [c for c in candidatures if filtre_statut.lower() in c.get(COLONNES[7], "").lower()]
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
    table.add_column(COLONNES[1], style="dim white", width=10)
    table.add_column(COLONNES[2], style="dim white", width=10)
    table.add_column(COLONNES[3], style="dim white", width=10)
    table.add_column(COLONNES[7], style="dim white", width=10)
    table.add_column(COLONNES[11], style="dim white", width=10)
        
    for i, c in enumerate(candidatures, 1):
        statut = c.get(COLONNES[7], "")
        color = "bright_black"
        i=0
        for statt in STATUTS[0]:
            if statt == statut:
                color = STATUTS[1][i]
            i+=1

        table.add_row(
            str(i),
            c.get(COLONNES[1], ""),
            c.get(COLONNES[2], ""),
            c.get(COLONNES[3], ""),
            statut,
            c.get(COLONNES[11], "")[:40] + ("..." if len(c.get("Notes", "")) > 40 else ""),
            style=f"dim {color}",
        )

    console.print(table)

    # Stats rapides
    total = len(candidatures)
    entretiens = sum(1 for c in candidatures if STATUTS[0][2] in c.get(COLONNES[7], ""))
    acceptes = sum(1 for c in candidatures if STATUTS[0][5] in c.get(COLONNES[7], ""))
    refus = sum(1 for c in candidatures if STATUTS[0][3] in c.get(COLONNES[7], ""))
    stage = sum(1 for c in candidatures if STATUTS[0][4] in c.get(COLONNES[7], ""))

    console.print(
        f"\n[dim]Total : [bold white]{total}[/bold white] candidature(s) · "
        f"[green]{entretiens}[/green] entretien(s) · "
        f"[yellow]{acceptes}[/yellow] accepté(s) · "
        f"[red]{refus}[/red] refus · "
        f"[bold white]{stage}[/bold white] [white]stage[/white](s)[/dim]\n"
    )
