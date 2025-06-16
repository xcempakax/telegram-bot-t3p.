from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

import os

BOT_TOKEN = os.environ['BOT_TOKEN']
RESIT_GROUP_ID = int(os.environ['RESIT_GROUP_ID'])
LOG_GROUP_ID = int(os.environ['LOG_GROUP_ID'])

bot = Bot(token=BOT_TOKEN)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    full_name = f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
    username = f"@{user.username}" if user.username else "No handle"
    
    message = (
        f"🆕 Customer started bot:\n"
        f"🆔 ID: {user.id}\n"
        f"👤 Username: {username}\n"
        f"📛 Name: {full_name}"
    )
    
    await bot.send_message(chat_id=LOG_GROUP_ID, text=message)
    await update.message.reply_text(
        "Hi! Saya Zet Resit. Anda boleh send semua resit dan gambar items di sini 😊"
    )

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    caption = update.message.caption if update.message.caption else "—"
    full_caption = (
        f"🧾 Resit diterima dari:\n"
        f"🆔 {user.id}\n"
        f"👤 @{user.username if user.username else 'No handle'}\n"
        f"📝 Remark: {caption}"
    )

    if update.message.photo:
        file = await update.message.photo[-1].get_file()
        await bot.send_photo(chat_id=RESIT_GROUP_ID, photo=file.file_id, caption=full_caption)
    elif update.message.document:
        file = await update.message.document.get_file()
        await bot.send_document(chat_id=RESIT_GROUP_ID, document=file.file_id, caption=full_caption)
    else:
        await update.message.reply_text("Sila hantar gambar atau dokumen PDF sahaja.")
        return

    await update.message.reply_text("✅ Bayaran anda diterima. Resit telah dihantar untuk semakan. Terima kasih kerana membeli dengan The Third Pick!😊")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    caption = (
        f"📩 Mesej dari customer:\n"
        f"🆔 {user.id}\n"
        f"👤 @{user.username if user.username else 'No handle'}\n"
        f"💬 \"{text}\""
    )

    await bot.send_message(chat_id=RESIT_GROUP_ID, text=caption)
    await update.message.reply_text("✍️ Mesej anda diterima dan dihantar ke admin. Terima kasih!")

async def cekid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"🆔 Telegram ID anda: `{user.id}`", parse_mode='Markdown')

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"⚠️ Update {update} caused error {context.error}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cekid", cekid))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.PDF, handle_file))
    app.add_error_handler(error_handler)
    print("🤖 BOT is running... full functions ready!")
    app.run_polling()

if __name__ == "__main__":
    main()

