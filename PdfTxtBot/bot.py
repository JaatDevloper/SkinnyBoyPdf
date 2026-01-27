import os
import telegram
from telegram import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, Update, constants
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes, ApplicationBuilder, CallbackQueryHandler

# Local Imports
from .hindi_fix import krutidev_to_unicode, fix_file_content

TOKEN = "YOUR_BOT_TOKEN_HERE"

class PDFBot:
    def __init__(self, TOKEN: str) -> None:
        self.app = ApplicationBuilder().token(TOKEN).build()
        self.app.add_handler(CommandHandler("start", self.__start__))
        self.app.add_handler(CommandHandler("txt", self.__txt_fix_handler__))
        self.app.add_handler(MessageHandler(filters.Document.ALL, self.__fileHandler__))

    async def __start__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("नमस्ते! अपनी Krutidev .txt फाइल भेजें और फिर उसे /txt के साथ रिप्लाई करें।")

    async def __fileHandler__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.document.file_name.endswith(".txt"):
            await update.message.reply_text("✅ फाइल मिल गई! अब इस फाइल को **Reply** करें और लिखें: `/txt`", parse_mode="Markdown")

    async def __txt_fix_handler__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message.reply_to_message or not update.message.reply_to_message.document:
            await update.message.reply_text("❌ कृपया फाइल को Reply करके /txt लिखें।")
            return

        reply = update.message.reply_to_message
        doc = reply.document
        
        # Download and Process
        file = await context.bot.get_file(doc.file_id)
        input_path = f"input_{doc.file_name}"
        output_path = f"Fixed_{doc.file_name}"
        
        await file.download_to_drive(input_path)

        with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        fixed_content = fix_file_content(content)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(fixed_content)

        await update.message.reply_document(document=open(output_path, "rb"), caption="✨ फोंट फिक्स कर दिया गया है!")

        # Cleanup
        os.remove(input_path)
        os.remove(output_path)

if __name__ == "__main__":
    bot = PDFBot(TOKEN)
    bot.app.run_polling()
    
