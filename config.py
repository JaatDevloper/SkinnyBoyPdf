import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ.get("TOK") or os.environ.get("TELEGRAM_BOT_TOKEN") or ""

if not TOKEN:
    raise ValueError("Please set TELEGRAM_BOT_TOKEN or TOK environment variable")