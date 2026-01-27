import os
from telegram import (
    BotCommand, InlineKeyboardButton, InlineKeyboardMarkup,
    InputMediaDocument, Update, constants
)
import telegram
from telegram.ext import (
    CommandHandler, MessageHandler, filters,
    ContextTypes, ApplicationBuilder, CallbackQueryHandler
)

from .messages import *
from .extracter import TextExtractor
from .ImageExtract import extractImg
from PdfTxtBot import messages


class PDFBot:
    def __init__(self, TOKEN: str) -> None:
        self.app = ApplicationBuilder().token(TOKEN).build()

        self.app.add_handler(CommandHandler("start", self.__start__))
        self.app.add_handler(CommandHandler("help", self.__help__))
        self.app.add_handler(CommandHandler("txt", self.__txt_fix_handler__))

        self.app.add_handler(MessageHandler(
            filters.Document.MimeType("application/pdf"),
            self.__fileHandler__
        ))

        self.app.add_handler(MessageHandler(
            filters.Document.ALL & ~filters.COMMAND,
            self.__otherHandler__
        ))

        self.app.add_handler(CallbackQueryHandler(self.__extract_text__))

        # ⚠️ FIX: remove COMMAND from here to avoid infinite loop
        self.app.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            self.__handler__
        ))

    async def __start__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("👋")
        await context.bot.set_my_commands([
            BotCommand("start", "Restart the bot"),
            BotCommand("help", "Help Description"),
            BotCommand("txt", "Fix Hindi encoding from .txt")
        ])
        await update.message.reply_text(
            START_TEXT.format(update.effective_user.first_name),
            parse_mode=constants.ParseMode.HTML
        )

    async def __help__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            HELPTEXT, parse_mode=constants.ParseMode.HTML
        )

    async def __handler__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(ERRORTEXT)

    async def __fileHandler__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [[
            InlineKeyboardButton("Extract Text 📋", callback_data="Extract"),
            InlineKeyboardButton("Get Images 📷", callback_data="Img")
        ]]
        await update.message.reply_document(
            document=update.message.document,
            caption="Click 👇 to extract",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    async def __otherHandler__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        doc = update.message.document
        if not doc:
            return

        if doc.file_name.lower().endswith(".txt"):
            await update.message.reply_text(
                "✅ .txt received\nReply with <b>/txt</b> to fix Hindi encoding",
                parse_mode=constants.ParseMode.HTML
            )
            return

        ext = doc.file_name.split(".")[-1]
        await update.message.reply_text(
            WRONGFILE.format(ext),
            parse_mode=constants.ParseMode.HTML
        )

    async def __extract_text__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        doc = query.message.document
        if not doc:
            return

        os.makedirs("PdfTxtBot/Docs", exist_ok=True)
        pdf_path = f"PdfTxtBot/Docs/{query.from_user.id}.pdf"

        file = await context.bot.get_file(doc.file_id)
        await file.download_to_drive(pdf_path)

        if query.data == "Extract":
            txt_path = pdf_path.replace(".pdf", ".txt")
            text = TextExtractor(filename=pdf_path).extract

            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(text)

            await query.message.reply_document(
                document=open(txt_path, "rb"),
                caption="Converted Text"
            )

            os.remove(txt_path)
            os.remove(pdf_path)

        elif query.data == "Img":
            images = await extractImg(pdf_path)
            for img in images[0]["output_jpgfiles"]:
                await query.message.reply_photo(photo=open(img, "rb"))
                os.remove(img)

            os.remove(pdf_path)

    async def __txt_fix_handler__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message.reply_to_message:
            await update.message.reply_text(
                "❌ Reply to a .txt file with /txt"
            )
            return

        doc = update.message.reply_to_message.document
        if not doc or not doc.file_name.lower().endswith(".txt"):
            await update.message.reply_text("❌ Only .txt files supported")
            return

        from .hindi_fix import krutidev_to_unicode

        os.makedirs("PdfTxtBot/Docs", exist_ok=True)
        in_path = f"PdfTxtBot/Docs/in_{doc.file_name}"
        out_path = f"PdfTxtBot/Docs/fixed_{doc.file_name}"

        file = await context.bot.get_file(doc.file_id)
        await file.download_to_drive(in_path)

        with open(in_path, "r", encoding="utf-8", errors="ignore") as f:
            fixed = krutidev_to_unicode(f.read())

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(fixed)

        await update.message.reply_document(
            document=open(out_path, "rb"),
            caption="✅ Hindi Encoding Fixed (Unicode)"
        )

        os.remove(in_path)
        os.remove(out_path)
