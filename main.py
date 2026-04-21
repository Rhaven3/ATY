#!/usr/bin/env python3
"""
Alternance Tracker CLI
Suis tes candidatures et génère des lettres de motivation en quelques secondes.
"""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint

app = typer.Typer(
    help="Alternance Tracker — Suivi de candidatures & lettres de motivation",
    add_completion=False,
    rich_markup_mode="rich",
)
console = Console()

def show_banner():
    text = Text()
    text.append(" ______     ______   __  __    \n", style="green")
    text.append("/\\  __ \\   /\\__  _\\ /\\ \\_\\ \\   \n", style="green")
    text.append("\\ \\  __ \\  \\/_/\\ \\/ \\ \\____ \\  \n", style="green")
    text.append(" \\ \\_\\ \\_\\    \\ \\_\\  \\/\\_____\\ \n", style="green")
    text.append("  \\/_/\\/_/     \\/_/   \\/_____/ \n", style="green")
    text.append("\n")
    text.append("Le CLI Trackeur d'Alternance\n", style="bold cyan")
    text.append("Suivi · Candidatures · Lettres de motivation", style="dim white")
    console.print(Panel(text, border_style="cyan", padding=(1, 4)))


@app.command("add", help="Ajouter une nouvelle candidature")
def add_candidature():
    """Enregistre une nouvelle candidature dans Google Sheets."""
    show_banner()
    from commands.add import run
    run()


@app.command("list", help="Lister toutes les candidatures")
def list_candidatures(
    statut: str = typer.Option(None, "--statut", "-s", help="Filtrer par statut (ex: En attente, Relancé...)")
):
    """Affiche toutes les candidatures avec leur statut."""
    show_banner()
    from commands.list_cmd import run
    run(statut)


@app.command("lettre", help="Générer une lettre de motivation")
def generer_lettre(
    output: str = typer.Option(None, "--output", "-o", help="Chemin du fichier de sortie (.txt ou .docx)")
):
    """Génère une lettre de motivation personnalisée via Claude AI."""
    show_banner()
    from commands.lettre import run
    run(output)


@app.command("update", help="Mettre à jour le statut d'une candidature")
def update_statut():
    """Met à jour le statut d'une candidature existante."""
    show_banner()
    from commands.update import run
    run()


@app.command("setup", help="Configurer le projet (première utilisation)")
def setup():
    """Assistant de configuration initiale."""
    show_banner()
    from commands.setup import run
    run()


if __name__ == "__main__":
    app()
