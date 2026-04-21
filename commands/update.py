"""
Commande `update` — Mettre à jour le statut d'une candidature.
"""

import questionary
from rich.console import Console
from config.sheets import get_toutes_candidatures, update_statut
from config.config import STATUTS, COLONNES

console = Console()

STYLE = questionary.Style([
    ("question", "bold cyan"),
    ("answer", "bold white"),
    ("pointer", "cyan"),
    ("highlighted", "bold cyan"),
])


def run():
    console.print("\n[bold cyan]🔄 Mise à jour d'une candidature[/bold cyan]\n")

    try:
        candidatures = get_toutes_candidatures()
    except Exception as e:
        console.print(f"[red]❌ Erreur : {e}[/red]")
        return

    if not candidatures:
        console.print("[yellow]Aucune candidature trouvée.[/yellow]")
        return

    choix = [
        f"{i+1}. {c[COLONNES[3]]} — {c[COLONNES[2]]} [{c.get(COLONNES[7], '?')}]"
        for i, c in enumerate(candidatures)
    ]

    selection = questionary.select(
        "📋 Quelle candidature mettre à jour ?",
        choices=choix,
        style=STYLE,
    ).ask()

    if not selection:
        return

    idx = int(selection.split(".")[0]) - 1
    candidature = candidatures[idx]

    nouveau_statut = questionary.select(
        f"📊 Nouveau statut pour [bold]{candidature['Entreprise']}[/bold] :",
        choices=STATUTS[0],
        default=candidature.get("Statut", STATUTS[0][0]),
        style=STYLE,
    ).ask()

    notes = questionary.text(
        "📝  Mettre à jour les notes ? (laisse vide pour conserver) :",
        style=STYLE,
    ).ask()

    try:
        update_statut(
            row_index=idx,
            nouveau_statut=nouveau_statut,
            notes=notes if notes else None,
        )
        console.print(
            f"\n[bold green]✅ Statut mis à jour → [cyan]{nouveau_statut}[/cyan][/bold green]\n"
        )
    except Exception as e:
        console.print(f"[red]❌ Erreur lors de la mise à jour : {e}[/red]")
