from rich.console import Console

from config.config import GOOGLE_CREDENTIALS_FILE, GOOGLE_SHEET_ID
from config.sheets import get_sheet

console = Console()

console.print(GOOGLE_CREDENTIALS_FILE)
console.print(GOOGLE_SHEET_ID)
sheet = get_sheet()
console.print(sheet)