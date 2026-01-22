# PDF Telegram Bot

A Telegram bot that extracts text and images from PDF files.

## Features
- Extract text from PDF documents.
- Extract images from PDF documents.
- Built with `python-telegram-bot`.

## Project Structure
- `main.py`: Entry point.
- `config.py`: Configuration and environment variable loading.
- `PdfTxtBot/`: Core logic.
  - `bot.py`: Telegram bot handlers.
  - `extracter.py`: Text extraction logic.
  - `ImageExtract.py`: Image extraction logic.
  - `messages.py`: Bot response strings.
- `PdfTxtBot/Docs/`: Temporary storage for processing files.

## Environment Variables
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token.

## Deployment
Configured to run as a VM deployment on Replit.
