import asyncio
import logging
from datetime import time
from telegram import Bot
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8715610432:AAF0ZQRWgL0YiMhcIxdwrlNlygOkP0cbD3M"
CHAT_ID = 590951027

SEND_HOUR = 4
SEND_MINUTE = 0

WORDS = [
    {"word": "Resilience", "translation": "Төзімділік", "example": "She showed great resilience."},
    {"word": "Ambition", "translation": "Табандылық", "example": "His ambition drove him to success."},
    {"word": "Gratitude", "translation": "Алғыс", "example": "Express gratitude every day."},
    {"word": "Discipline", "translation": "Тәртіп", "example": "Discipline is the key to achievement."},
    {"word": "Integrity", "translation": "Адалдық", "example": "Act with integrity at all times."},
    {"word": "Empathy", "translation": "Жанашырлық", "example": "Empathy builds strong relationships."},
    {"word": "Courage", "translation": "Батылдық", "example": "It takes courage to speak the truth."},
    {"word": "Wisdom", "translation": "Даналық", "example": "Wisdom comes with experience."},
    {"word": "Patience", "translation": "Шыдамдылық", "example": "Patience is a virtue."},
    {"word": "Focus", "translation": "Назар аудару", "example": "Focus on what matters most."},
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
        message += f"*{i}. {w['word']}* — _{w['translation']}_\n📝 {w['example']}\n\n"
    message += "💪 Осы сөздерді бүгін қолданып көріңіз!"
    await context.bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

async def start(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Сәлем! Мен *ABA Group* боты!\nКүн сайын таңертең 3 ағылшын сөзін жіберемін.\n/words командасымен бірден алыңыз!", parse_mode="Markdown")

async def words_now(update, context: ContextTypes.DEFAULT_TYPE):
    words = get_three_words()
    message = "🌟 *ABA Group — Күнделікті ағылшын сөздері*\n\n"
    for i, w in enumerate(words, 1):
        message += f"*{i}. {w['word']}* — _{w['translation']}_\n📝 {w['example']}\n\n"
    await update.message.reply_text(message, parse_mode="Markdown")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("words", words_now))
    app.job_queue.run_daily(send_daily_words, time=time(hour=SEND_HOUR, minute=SEND_MINUTE))
    app.run_polling()

if __name__ == "__main__":
    main()
