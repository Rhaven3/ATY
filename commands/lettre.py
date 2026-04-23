"""
Commande `lettre` — Générer une lettre de motivation via Claude AI.
"""

import questionary
import anthropic
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from pathlib import Path
from config.sheets import get_toutes_candidatures
from config.config import (
    ANTHROPIC_API_KEY,
    CLAUDE_MODEL,
    PRENOM,
    NOM,
    FORMATION,
    FORMATION_FUTUR,
    ECOLE,
    EMAIL,
    TEL,
    COLONNES
)

console = Console()

STYLE = questionary.Style([
    ("question", "bold cyan"),
    ("answer", "bold white"),
    ("pointer", "cyan"),
    ("highlighted", "bold cyan"),
])

WEB_SEARCH_TOOL = {"type": "web_search_20250305", "name": "web_search"}
MAX_ITERATION = 5


def build_prompt(candidature: dict, infos_supp: str, writedLetter: str|None) -> str:
    return f"""Tu es un expert en rédaction de lettres de motivation pour des étudiants cherchant une alternance en France.

Rédige une lettre de motivation professionnelle, percutante et personnalisée pour cette candidature.

Avant de rédiger, utilise l'outil web_search pour rechercher des informations récentes et pertinentes sur l'entreprise :
- Valeurs, culture d'entreprise, mission
- Actualités récentes (projets, innovations, croissance)
- Informations sur le secteur / métier visé
- Ce qui rend cette entreprise unique ou attractive

## Informations sur le candidat
- Prénom / Nom : {PRENOM} {NOM}
- Formation Actuel : {FORMATION}
- Formation Futur : {FORMATION_FUTUR}
- École : {ECOLE}
- Email : {EMAIL}
- Téléphone : {TEL}

## Informations sur la candidature
{get_candidature_info(candidature)}

## Informations complémentaires fournies par le candidat
{infos_supp if infos_supp else "Aucune information supplémentaire."}

## Instructions de rédaction
- Ton : professionnel mais dynamique, pas trop formel
- Structure : accroche percutante →  compétences → parcours scolaire/pro -> motivation pour l'entreprise →
- Longueur : 3-4 paragraphes, environ 300 mots
- Personnalise vraiment en fonction du secteur et de l'entreprise
- Mets en valeur la complémentarité formation/alternance
- Termine par une formule de politesse adaptée

{f"""Complète uniquement les zones marquées [entre crochets] dans la lettre ci-dessous, 
{writedLetter}

en te basant sur les recherches effectuées sur l'entreprise. 
Retourne les zones remplacées, sans commentaires, ni explications.
""" if writedLetter else "Rédige uniquement la lettre, sans commentaires ni explications supplémentaires."}
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
        f"{i+1}. {c[COLONNES[2]]} — {c[COLONNES[3]]}"
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
        "Informations supplémentaires (optionnel) :",
        style=STYLE,
        multiline=True,
    ).ask()
    
    iswrited = questionary.confirm(
        "Tu as déjà une ébauche de lettre à compléter ?"
    ).ask()
    writedLetter = None
    if iswrited:
        writedLetter = questionary.text(
            "Lettre pré-écrite, spécifié ce qui doit-être généré par des [] (ex: [pourquoi cette entreprise]) : ",
            style=STYLE,
            multiline=True
        ).ask()
        

    # Génération via Claude + recherche web
    console.print(f"\n[dim cyan]🔍 Claude recherche des infos sur [bold]{candidature['Entreprise']}[/bold]...[/dim cyan]")
 
    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        prompt = build_prompt(candidature, infos_supp or "", writedLetter)
 
        lettre = ""
        queries = []
        with console.status("[cyan]Recherche en cours puis rédaction...[/cyan]"):
            lettre, queries = _generer_avec_recherche(client, prompt)
 
    except Exception as e:
        console.print(f"[red]❌ Erreur API Claude : {e}[/red]")
        return
 
    # Afficher les recherches effectuées
    if queries:
        console.print(f"[dim]🔎 Recherches effectuées : {' · '.join(queries)}[/dim]\n")
    else:
        console.print("[dim]🔎 Recherche web effectuée[/dim]\n")
 
    # Affichage
    console.print(Panel(
        lettre,
        title=f"[bold cyan]Lettre — {candidature[COLONNES[3]]} · {candidature[COLONNES[2]]}[/bold cyan]",
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
            nom_fichier = f"lettre_{candidature[COLONNES[3]].replace(' ', '_')}_{candidature[COLONNES[2]].replace(' ', '_')}.txt"
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
 

def _generer_avec_recherche(client: anthropic.Anthropic, prompt: str) -> tuple[str, list[str]]:
    """
    Boucle agentique : Claude peut faire plusieurs tours de recherche
    avant de produire la lettre finale.
    """
    messages = [{"role": "user", "content": prompt}]
    all_queries = []
 
    for i in range(MAX_ITERATION):
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=2048,
            tools=[WEB_SEARCH_TOOL],
            messages=messages,
        )
 
        # Collecter les queries de ce tour
        for block in response.content:
            if block.type == "tool_use" and block.name == "web_search":
                query = block.input.get("query", "")
                if query:
                    all_queries.append(query)
 
        # Claude a fini (plus d'appels d'outils) → extraire la lettre
        if response.stop_reason == "end_turn":
            lettre = next(
                (block.text for block in response.content if block.type == "text"),
                ""
            )
            return lettre, all_queries
 
        # Claude veut continuer à chercher → on lui renvoie les résultats
        if response.stop_reason == "tool_use":
            # Ajouter la réponse de l'assistant à l'historique
            messages.append({"role": "assistant", "content": response.content})
 
            # Construire les tool_results pour chaque appel
            tool_results = []
            for block in response.content:
                if block.type == "tool_result":
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.tool_use_id,
                        "content": block.content,
                    })
 
            # Si pas de tool_result explicite (l'API les gère en interne),
            # on relance simplement pour laisser Claude continuer
            if tool_results:
                messages.append({"role": "user", "content": tool_results})
            else:
                # web_search est géré côté serveur Anthropic,
                # on remet juste la réponse et on relance
                messages.append({"role": "user", "content": "Continue."})
 
        else:
            # Stop reason inattendue, on sort
            lettre = next(
                (block.text for block in response.content if block.type == "text"),
                ""
            )
            return lettre, all_queries

    console.print("[yellow]Nombre max de recherches atteint.[/yellow]")
    lettre = next((b.text for b in response.content if b.type == "text"), "")
    return lettre, all_queries


def get_candidature_info(candidature: dict) -> str:
    infos = ""
    for i in range(len(COLONNES)):
        infos += f"- {COLONNES[i]} : {candidature.get(COLONNES[i], '')}"
    return infos