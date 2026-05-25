import asyncio
import logging
from datetime import time
from telegram import Bot
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8715610432:AAF0ZQRWgL0YiMhcIxdwrlNlygOkP..."  # өзіңнің токенің
CHAT_ID = 590951027

SEND_HOUR = 4
SEND_MINUTE = 0

WORDS = [
    {"word": "Resilience", "translation": "Төзімділік"},
    {"word": "Ambition", "translation": "Табандылық"},
    {"word": "Gratitude", "translation": "Алғыс"},
    {"word": "Discipline", "translation": "Тәртіп"},
    {"word": "Integrity", "translation": "Адалдық"},
    {"word": "Empathy", "translation": "Жанашырлық"},
    {"word": "Courage", "translation": "Батылдық"},
    {"word": "Wisdom", "translation": "Даналық"},
    {"word": "Patience", "translation": "Шыдамдылық"},
    {"word": "Focus", "translation": "Назар аудару"},
]

logging.basicConfig(level=logging.INFO)
day_counter = {"index": 0}

def get_three_words():
    idx = day_counter["index"] % (len(WORDS) // 3)
    trio = WORDS[idx * 3: idx * 3 + 3]
    day_counter["index"] += 1
    return trio

async def send_daily_words(context: ContextTypes.DEFAULT_TYPE):
    words = get_three_words()
    message = "🌟 *ABA Group — Күнделікті ағылшын сөздері*\n\n"
    for i, w in enumerate(words, 1):
        message += f"*{i}. {w['word']}* — _{w['translation']}_\n"
    message += "\n💪 Осы сөздерді бүгін қолданып көр!"
    await context.bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

async def start(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Сәлем! Мен ABA Group English ботымын!")

async def words_now(update, context: ContextTypes.DEFAULT_TYPE):
    words = get_three_words()
    message = "🌟 *ABA Group — Күнделікті ағылшын сөздері*\n\n"
    for i, w in enumerate(words, 1):
        message += f"*{i}. {w['word']}* — _{w['translation']}_\n"
    await update.message.reply_text(message, parse_mode="Markdown")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("words", words_now))
    app.job_queue.run_daily(
        send_daily_words,
        time=time(hour=SEND_HOUR, minute=SEND_MINUTE)
    )
    app.run_polling()

if __name__ == "__main__":
    main()
