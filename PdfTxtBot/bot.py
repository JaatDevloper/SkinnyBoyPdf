import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from hindi_fix import fix_file_content

TOKEN = "YOUR_BOT_TOKEN_HERE"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! Send your .txt file and reply with /txt to fix encoding.")

async def txt_fix_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.document:
        await update.message.reply_text("❌ Please reply to a .txt file with /txt.")
        return

    doc = update.message.reply_to_message.document
    input_file = f"in_{doc.file_id}.txt"
    output_file = f"Fixed_{doc.file_name}"

    try:
        # Downloading
        file = await context.bot.get_file(doc.file_id)
        await file.download_to_drive(input_file)

        # Reading with safety
        try:
            with open(input_file, "r", encoding="utf-8") as f:
                content = f.read()
        except:
            with open(input_file, "r", encoding="latin-1") as f:
                content = f.read()

        fixed_data = fix_file_content(content)

        # Writing Fixed Content
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(fixed_data)

        # Uploading
        await update.message.reply_document(
            document=open(output_file, "rb"), 
            caption="✅ Hindi Unicode Fixed! (English preserved)"
        )

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")
    finally:
        if os.path.exists(input_file): os.remove(input_file)
        if os.path.exists(output_file): os.remove(output_file)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("txt", txt_fix_handler))
    print("Bot is running...")
    app.run_polling()
    
