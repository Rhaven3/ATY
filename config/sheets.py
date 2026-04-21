"""
Intégration Google Sheets via gspread.
Toutes les opérations CRUD sur le sheet de suivi.
"""

import gspread
import typer
from datetime import datetime
from google.oauth2.service_account import Credentials
from rich.console import Console
from config.config import (
    GOOGLE_CREDENTIALS_FILE,
    GOOGLE_SHEET_ID,
    SHEET_NAME,
    COLONNES,
    STATUTS
)

console = Console()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def get_sheet():
    """Retourne le worksheet de suivi, crée les en-têtes si vide."""
    try:
        creds = Credentials.from_service_account_file(
            GOOGLE_CREDENTIALS_FILE, scopes=SCOPES
        )
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(GOOGLE_SHEET_ID)

        try:
            ws = spreadsheet.worksheet(SHEET_NAME)
        except gspread.WorksheetNotFound:
            console.print(f"[dim]worksheet: '{SHEET_NAME}' non trouvé[/dim]")
            ws = spreadsheet.add_worksheet(title=SHEET_NAME, rows=1000, cols=len(COLONNES))
            console.print(f"[green]worksheet: '{SHEET_NAME}' créée ![/green]")

        # Crée les en-têtes si la feuille est vide
        if not ws.get_all_values()[0]:
            ws.append_row(COLONNES)
            _format_header(ws)
            console.print(f"[green]✅ Feuille '{SHEET_NAME}' initialisée avec les en-têtes.[/green]")

        return ws

    except FileNotFoundError:
        console.print(
            f"[red]❌ Fichier credentials introuvable : {GOOGLE_CREDENTIALS_FILE}[/red]\n"
            "[yellow]Lance [bold]python main.py setup[/bold] pour configurer le projet.[/yellow]"
        )
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]❌ Erreur Google Sheets : {e}[/red]")
        raise


def _format_header(ws):
    """Applique un formatage basique aux en-têtes."""
    try:
        ws.format("A1:M1", {
            "backgroundColor": {"red": 0.2, "green": 0.2, "blue": 0.2},
            "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
        })
    except Exception:
        pass  # Le formatage est optionnel


def ajouter_candidature(data: dict) -> int:
    """
    Ajoute une ligne dans le sheet.
    data doit contenir les clés correspondant à COLONNES.
    Retourne le numéro de ligne ajoutée.
    """
    ws = get_sheet()
    row = [data.get(col, "") for col in COLONNES]
    ws.append_row(row, value_input_option="USER_ENTERED")
    console.print("[green]candidature ajoutée avec succées![/green]")
    all_rows = ws.get_all_values()
    return len(all_rows)


def get_toutes_candidatures() -> list[dict]:
    """Retourne toutes les candidatures sous forme de liste de dicts."""
    ws = get_sheet()
    records = ws.get_all_records()
    return records


def get_candidature_par_index(index: int) -> dict:
    """Retourne une candidature par son index (1-based, hors en-tête)."""
    ws = get_sheet()
    row = ws.row_values(index + 1)  # +1 pour l'en-tête
    return dict(zip(COLONNES, row))


def update_statut(row_index: int, nouveau_statut: str, notes: str = None):
    """
    Met à jour le statut (et optionnellement les notes) d'une candidature.
    row_index : index dans la liste (0-based), pas dans le sheet.
    """
    ws = get_sheet()
    sheet_row = row_index + 2  # +1 en-tête, +1 car 1-based
    col_statut = COLONNES.index("Statut") + 1
    ws.update_cell(sheet_row, col_statut, nouveau_statut)

    if notes is not None:
        col_notes = COLONNES.index("Note") + 1
        ws.update_cell(sheet_row, col_notes, notes)
        
    if nouveau_statut == STATUTS[1]:
        col_date_rel = 2
        ws.update_cell(sheet_row, col_date_rel, datetime.now().strftime("%d/%m/%Y"))
