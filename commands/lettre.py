"""
Commande `lettre` — Générer une lettre de motivation via Claude AI.
"""

import questionary
import anthropic
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from pathlib import Path
from sheets import get_toutes_candidatures
from config import (
    ANTHROPIC_API_KEY,
    CLAUDE_MODEL,
    TON_PRENOM,
    TON_NOM,
    TON_FORMATION,
    TON_ECOLE,
    TON_EMAIL,
    TON_TEL,
)

console = Console()

STYLE = questionary.Style([
    ("question", "bold cyan"),
    ("answer", "bold white"),
    ("pointer", "cyan"),
    ("highlighted", "bold cyan"),
])


def build_prompt(candidature: dict, infos_supp: str) -> str:
    return f"""Tu es un expert en rédaction de lettres de motivation pour des étudiants cherchant une alternance en France.

Rédige une lettre de motivation professionnelle, percutante et personnalisée pour cette candidature.

## Informations sur le candidat
- Prénom / Nom : {TON_PRENOM} {TON_NOM}
- Formation : {TON_FORMATION}
- École : {TON_ECOLE}
- Email : {TON_EMAIL}
- Téléphone : {TON_TEL}

## Informations sur la candidature
- Entreprise : {candidature.get('Entreprise', '')}
- Poste recherché : {candidature.get('Poste', '')}
- Ville : {candidature.get('Ville', '')}
- Secteur : {candidature.get('Secteur', '')}
- Contact RH : {candidature.get('Contact', 'Non renseigné')}

## Informations complémentaires fournies par le candidat
{infos_supp if infos_supp else "Aucune information supplémentaire."}

## Instructions de rédaction
- Ton : professionnel mais dynamique, pas trop formel
- Structure : accroche percutante → motivation pour l'entreprise → compétences → conclusion avec call-to-action
- Longueur : 3-4 paragraphes, environ 300 mots
- Personnalise vraiment en fonction du secteur et de l'entreprise
- Mets en valeur la complémentarité formation/alternance
- Termine par une formule de politesse adaptée

Rédige uniquement la lettre, sans commentaires ni explications supplémentaires.
"""


def run(output_path: str = None):
    if not ANTHROPIC_API_KEY:
        console.print(
            "[red]❌ Clé API Anthropic manquante.[/red]\n"
            "[yellow]Ajoute [bold]ANTHROPIC_API_KEY[/bold] dans ton fichier .env[/yellow]"
        )
        return

    console.print("\n[bold cyan]✍️  Génération de lettre de motivation[/bold cyan]\n")

    # Charger les candidatures
    try:
        candidatures = get_toutes_candidatures()
    except Exception as e:
        console.print(f"[red]❌ Erreur chargement des candidatures : {e}[/red]")
        return

    if not candidatures:
        console.print("[yellow]Aucune candidature trouvée. Commence par en ajouter une ![/yellow]")
        console.print("[dim]→ [bold]python main.py add[/bold][/dim]")
        return

    # Sélection de la candidature
    choix = [
        f"{i+1}. {c['Entreprise']} — {c['Poste']} ({c['Ville']})"
        for i, c in enumerate(candidatures)
    ]

    selection = questionary.select(
        "📋  Pour quelle candidature ?",
        choices=choix,
        style=STYLE,
    ).ask()

    if not selection:
        return

    idx = int(selection.split(".")[0]) - 1
    candidature = candidatures[idx]

    # Infos supplémentaires
    console.print("\n[dim]Tu peux préciser des éléments spécifiques à l'entreprise, des projets pertinents, tes points forts...[/dim]")
    infos_supp = questionary.text(
        "📝  Informations supplémentaires (optionnel) :",
        style=STYLE,
        multiline=True,
    ).ask()

    # Génération via Claude
    console.print(f"\n[dim cyan]⚡ Génération en cours pour [bold]{candidature['Entreprise']}[/bold]...[/dim cyan]\n")

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        prompt = build_prompt(candidature, infos_supp or "")

        lettre = ""
        with console.status("[cyan]Claude rédige ta lettre...[/cyan]"):
            message = client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )
            lettre = message.content[0].text

    except Exception as e:
        console.print(f"[red]❌ Erreur API Claude : {e}[/red]")
        return

    # Affichage
    console.print(Panel(
        lettre,
        title=f"[bold cyan]Lettre — {candidature['Entreprise']} · {candidature['Poste']}[/bold cyan]",
        border_style="cyan",
        padding=(1, 2),
    ))

    # Sauvegarde
    if not output_path:
        sauvegarder = questionary.confirm(
            "💾  Sauvegarder dans un fichier ?",
            default=True,
            style=STYLE,
        ).ask()

        if sauvegarder:
            nom_fichier = f"lettre_{candidature['Entreprise'].replace(' ', '_')}_{candidature['Poste'].replace(' ', '_')}.txt"
            output_path = questionary.text(
                "📁  Nom du fichier :",
                default=nom_fichier,
                style=STYLE,
            ).ask()

    if output_path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(lettre, encoding="utf-8")
        console.print(f"\n[bold green]✅ Lettre sauvegardée : {path.resolve()}[/bold green]")

    console.print("\n[dim]💡 Pense à relire et personnaliser avant d'envoyer ![/dim]\n")
