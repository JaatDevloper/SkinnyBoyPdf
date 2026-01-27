import os
import telegram
from telegram import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaDocument, Update, constants
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes, ApplicationBuilder, CallbackQueryHandler

# Local Imports
from .messages import START_TEXT, HELPTEXT, ERRORTEXT, WRONGFILE
from .extracter import TextExtractor
from .ImageExtract import extractImg
from PdfTxtBot import messages
from .hindi_fix import krutidev_to_unicode, fix_file_content

class PDFBot:
    def __init__(self, TOKEN: str) -> None:
        self.app = ApplicationBuilder().token(TOKEN).build()
        self.app.add_handler(CommandHandler("start", self.__start__))
        self.app.add_handler(CommandHandler("help", self.__help__))
        self.app.add_handler(CommandHandler("txt", self.__txt_fix_handler__))
        self.app.add_handler(MessageHandler(filters=filters.Document.MimeType(
            'application/pdf'), callback=self.__fileHandler__))
        self.app.add_handler(MessageHandler(filters=filters.Document.ALL & ~filters.COMMAND, callback=self.__otherHandler__))
        self.app.add_handler(CallbackQueryHandler(self.__extract_text__))

        # ✅ Prevent infinite loop & CPU spike
        self.app.add_handler(MessageHandler(
            filters=filters.TEXT & ~filters.COMMAND,
            callback=self.__handler__
        ))

    async def __start__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_chat_action(update.effective_chat.id, action=constants.ChatAction.TYPING)
        await update.message.reply_text("👋")
        await context.bot.set_my_commands([BotCommand("start", "Restart the bot"), BotCommand("help", "Help Description")])
        await context.bot.send_message(update.effective_chat.id, text=START_TEXT.format(update.effective_user.first_name), parse_mode=constants.ParseMode.HTML)

    async def __help__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(text=HELPTEXT, parse_mode=constants.ParseMode.HTML)

    async def __handler__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(text=ERRORTEXT)

    async def __fileHandler__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [InlineKeyboardButton(text="Extract Text 📋", callback_data="Extract")],
            [InlineKeyboardButton(text="Get Images 📷", callback_data="Img")]
        ]
        await update.message.reply_document(
            document=update.message.document, 
            caption="Click On 👇 Extract Button to Get Text", 
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    async def __otherHandler__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            filename = update.message.document.file_name.split(".")
            extension = filename[-1].lower()
            if extension == "txt":
                await update.message.reply_text(
                    "✅ I received your .txt file.\n\nReply to this file with <b>/txt</b> to fix Hindi font encoding.",
                    parse_mode=constants.ParseMode.HTML
                )
                return
            await update.message.reply_text(text=WRONGFILE.format(extension), parse_mode=constants.ParseMode.HTML)
        except AttributeError:
            pass

    async def __extract_text__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.callback_query.message.document:
            await update.callback_query.answer("Error: No document found.", show_alert=True)
            return
        
        docs_dir = os.path.join("PdfTxtBot", "Docs")
        os.makedirs(docs_dir, exist_ok=True)
        
        filename = os.path.join(docs_dir, "file"+str(update.effective_chat.id)+".pdf")
        id = update.callback_query.message.document.file_id
        name = update.callback_query.message.document.file_name.split(".")[0]+".txt"
        
        data = await context.bot.get_file(file_id=id)
        await data.download_to_drive(custom_path=filename)
        await context.bot.answer_callback_query(update.callback_query.id, text="Downloading.....")

        if update.callback_query.data == "Extract":
            txtfilename = os.path.join(docs_dir, "file" + str(update.effective_chat.id)+".txt")
            txt = TextExtractor(filename=filename)
            with open(txtfilename, "w", encoding="utf-8") as f:
                f.write(txt.extract)

            try:
                await context.bot.send_chat_action(
                    action=constants.ChatAction.UPLOAD_DOCUMENT,
                    chat_id=update.effective_chat.id
                )
                await context.bot.send_media_group(
                    chat_id=update.effective_chat.id,
                    media=[InputMediaDocument(
                        media=open(txtfilename, "rb"),
                        caption="Converted Text",
                        filename=name
                    )]
                )
            except telegram.error.BadRequest as bd:
                if bd.message == "File must be non-empty":
                    await update.callback_query.message.reply_text(
                        messages.SCANFILE.format(update.effective_user.first_name)
                    )

            if os.path.exists(txtfilename): os.remove(txtfilename)
            if os.path.exists(filename): os.remove(filename)

        elif update.callback_query.data == "Img":
            data = await extractImg(filename)
            jpgfile = data[0]["output_jpgfiles"]
            for files in jpgfile:
                await context.bot.send_chat_action(
                    action=constants.ChatAction.UPLOAD_PHOTO,
                    chat_id=update.effective_chat.id
                )
                try:
                    await context.bot.send_photo(
                        update.effective_chat.id,
                        photo=open(files, "rb"),
                        read_timeout=50,
                        write_timeout=50
                    )
                except telegram.error.TimedOut:
                    await context.bot.send_message(
                        update.effective_chat.id,
                        text="Some Error Occurred ❗"
                    )
                if os.path.exists(files): os.remove(files)

            img_dir = os.path.join(f"{filename}_dir")
            if os.path.exists(img_dir): os.removedirs(img_dir)
            if os.path.exists(filename): os.remove(filename)

    async def __txt_fix_handler__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message.reply_to_message:
            await update.message.reply_text(
                "❌ Please reply to a .txt file with /txt to fix Hindi encoding."
            )
            return

        document = update.message.reply_to_message.document
        
        # Process Raw Text Message
        if not document:
            text_content = update.message.reply_to_message.text
            if not text_content:
                await update.message.reply_text("❌ The message you replied to has no text or file.")
                return
            
            fixed_text = krutidev_to_unicode(text_content)
            await update.message.reply_text(f"✅ Fixed Hindi Text:\n\n{fixed_text}")
            return
        
        # Process .txt File
        if not document.file_name.lower().endswith(".txt"):
            await update.message.reply_text("❌ Only .txt files are supported for this command.")
            return

        await context.bot.send_chat_action(update.effective_chat.id, action=constants.ChatAction.TYPING)

        try:
            file = await context.bot.get_file(document.file_id)
            docs_dir = os.path.join("PdfTxtBot", "Docs")
            os.makedirs(docs_dir, exist_ok=True)
            
            file_path = os.path.join(docs_dir, f"temp_{update.effective_chat.id}_{document.file_name}")
            await file.download_to_drive(custom_path=file_path)

            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Apply optimized Hindi fix logic
            fixed_content = fix_file_content(content)

            output_path = os.path.join(docs_dir, f"Fixed_{document.file_name}")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(fixed_content)

            with open(output_path, "rb") as output_file:
                await update.message.reply_document(
                    document=output_file,
                    caption=f"✅ Fixed Hindi: {document.file_name}\n(Kruti Dev ➔ Unicode)"
                )

        except Exception as e:
            await update.message.reply_text(f"❌ Error processing file: {str(e)}")

        finally:
            # Final Cleanup
            if 'file_path' in locals() and os.path.exists(file_path):
                os.remove(file_path)
            if 'output_path' in locals() and os.path.exists(output_path):
                os.remove(output_path)

    def run(self):
        self.app.run_polling()
        
