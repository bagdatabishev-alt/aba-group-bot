import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Bot
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

TOKEN = "8715610432:AAF0ZQRWgL0YiMhcIxdwrlNlygOkP0cbD3M"
CHAT_ID = 590951027

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
bot = Bot(token=TOKEN)

def get_three_words():
    idx = day_counter["index"] % (len(WORDS) // 3)
    trio = WORDS[idx * 3: idx * 3 + 3]
    day_counter["index"] += 1
    return trio

async def send_daily_words():
    words = get_three_words()
    message = "🌟 *ABA Group — Күнделікті ағылшын сөздері*\n\n"
    for i, w in enumerate(words, 1):
        message += f"*{i}. {w['word']}* — _{w['translation']}_\n📝 {w['example']}\n\n"
    message += "💪 Осы сөздерді бүгін қолданып көріңіз!"
    await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

async def start(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Сәлем! Мен *ABA Group* боты!\n/words командасымен сөздер алыңыз!", parse_mode="Markdown")

async def words_now(update, context: ContextTypes.DEFAULT_TYPE):
    words = get_three_words()
    message = "🌟 *ABA Group — Күнделікті ағылшын сөздері*\n\n"
    for i, w in enumerate(words, 1):
        message += f"*{i}. {w['word']}* — _{w['translation']}_\n📝 {w['example']}\n\n"
    await update.message.reply_text(message, parse_mode="Markdown")

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("words", words_now))
    
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_daily_words, 'cron', hour=4, minute=0)
    scheduler.start()
    
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
