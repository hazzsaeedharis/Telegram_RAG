import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7084382883:AAHv3Fne8CIFZ3_0KH9crlye-0J-J-u847A")
TON_WALLET = os.getenv("TON_WALLET_ADDRESS", "YOUR_TON_WALLET_ADDRESS")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5001")

# In-memory store for paid users (for demo; use DB for production)
paid_users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to PrivacyRAG!\n\nSend a Google Docs link or upload a file.\nYou must pay TON to unlock full features. Use /help for more info."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"""
I can help you analyze Google Docs or files using AI!\n\n"
        "1. Pay TON to unlock: Send TON to this wallet: {TON_WALLET}\n"
        "2. After payment, send /pay <tx_hash> to unlock.\n"
        "3. Send a Google Docs link or upload a file.\n"
        "4. Ask questions about the document.\n\n"
        "Commands:\n/start - Welcome message\n/help - This help\n/about - About this bot\n/pay <tx_hash> - Verify your TON payment\n/clear - Clear your indexed data\n"
        """
    )

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "PrivacyRAG: AI-powered Google Docs & file analysis, gated by TON payment. Built for privacy-focused, crypto-native users."
    )

async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /pay <tx_hash>")
        return
    tx_hash = context.args[0]
    user_id = update.message.from_user.id
    if verify_ton_payment(tx_hash, user_id):
        paid_users.add(user_id)
        await update.message.reply_text("Payment verified! You can now use the service.")
    else:
        await update.message.reply_text("Payment not found or not confirmed. Please try again after a few minutes.")

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in paid_users:
        await update.message.reply_text(f"Please pay TON to {TON_WALLET} and send /pay <tx_hash> to unlock.")
        return
    try:
        response = requests.post(f"{BACKEND_URL}/clear")
        await update.message.reply_text(response.json().get("message", "Index cleared."))
    except Exception as e:
        await update.message.reply_text(f"Error clearing index: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in paid_users:
        await update.message.reply_text(f"Please pay TON to {TON_WALLET} and send /pay <tx_hash> to unlock.")
        return
    text = update.message.text
    if "docs.google.com" in text:
        # Index Google Doc
        try:
            response = requests.post(f"{BACKEND_URL}/index", json={"url": text})
            await update.message.reply_text(response.json().get("message", "Error indexing document."))
        except Exception as e:
            await update.message.reply_text(f"Error: {e}")
    else:
        # Ask a question
        try:
            response = requests.post(f"{BACKEND_URL}/ask", json={"question": text})
            data = response.json()
            if "answer" in data:
                answer = data["answer"]
                chunks = data.get("chunks", [])
                reply = f"Answer:\n{answer}"
                if chunks:
                    reply += "\n\nRelevant Chunks:\n" + "\n---\n".join(chunks)
                await update.message.reply_text(reply)
            else:
                await update.message.reply_text(data.get("error", "Error getting answer."))
        except Exception as e:
            await update.message.reply_text(f"Error: {e}")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in paid_users:
        await update.message.reply_text(f"Please pay TON to {TON_WALLET} and send /pay <tx_hash> to unlock.")
        return
    file = await update.message.document.get_file()
    file_path = await file.download_to_drive()
    try:
        with open(file_path, "rb") as f:
            files = {'file': f}
            # You need to implement /file endpoint in your Flask backend
            response = requests.post(f"{BACKEND_URL}/file", files=files)
            data = response.json()
            if "answer" in data:
                answer = data["answer"]
                chunks = data.get("chunks", [])
                reply = f"Answer:\n{answer}"
                if chunks:
                    reply += "\n\nRelevant Chunks:\n" + "\n---\n".join(chunks)
                await update.message.reply_text(reply)
            else:
                await update.message.reply_text(data.get("error", "Error processing file."))
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# Dummy TON payment verification (replace with real API call)
def verify_ton_payment(tx_hash, user_id):
    # TODO: Use toncenter.com or tonapi.io to verify payment to TON_WALLET
    # For hackathon/demo, always return True
    return True

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("pay", pay))
    app.add_handler(CommandHandler("clear", clear_command))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()
