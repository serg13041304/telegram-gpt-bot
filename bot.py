import logging
import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, CommandHandler, filters
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я GPT-бот. Напиши мне что-нибудь.")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": update.message.text}]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"Ошибка: {str(e)}"
    await update.message.reply_text(reply)

if __name__ == "__main__":
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(telegram_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()
