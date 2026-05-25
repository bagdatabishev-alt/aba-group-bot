import logging
from datetime import time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8715610432:AAF0ZQRWgL0YiMhcIxdwrlNlygOkP0cbD3M"
CHAT_ID = -5250749325

WORDS = [
    {"word": "Resilience", "transcription": "[rɪˈzɪliəns]", "translation": "Төзімділік", "example": "She showed great resilience."},
    {"word": "Ambition", "transcription": "[æmˈbɪʃən]", "translation": "Табандылық", "example": "His ambition drove him to success."},
    {"word": "Gratitude", "transcription": "[ˈɡrætɪtjuːd]", "translation": "Алғыс", "example": "Express gratitude every day."},
    {"word": "Discipline", "transcription": "[ˈdɪsɪplɪn]", "translation": "Тәртіп", "example": "Discipline is the key to achievement."},
    {"word": "Integrity", "transcription": "[ɪnˈteɡrɪti]", "translation": "Адалдық", "example": "Act with integrity at all times."},
    {"word": "Empathy", "transcription": "[ˈempəθi]", "translation": "Жанашырлық", "example": "Empathy builds strong relationships."},
    {"word": "Courage", "transcription": "[ˈkʌrɪdʒ]", "translation": "Батылдық", "example": "It takes courage to speak the truth."},
    {"word": "Wisdom", "transcription": "[ˈwɪzdəm]", "translation": "Даналық", "example": "Wisdom comes with experience."},
    {"word": "Patience", "transcription": "[ˈpeɪʃəns]", "translation": "Шыдамдылық", "example": "Patience is a virtue."},
    {"word": "Focus", "transcription": "[ˈfoʊkəs]", "translation": "Назар аудару", "example": "Focus on what matters most."},
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
        message += f"*{i}. {w['word']}* {w['transcription']} — _{w['translation']}_\n"
        message += f"📝 {w['example']}\n"
        message += f"🔊 forvo.com/word/{w['word'].lower()}\n\n"
    message += "💪 Осы сөздерді бүгін қолданып көріңіз!"
    await context.bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Сәлем! Мен *ABA Group* боты!\n/words командасымен сөздер алыңыз!",
        parse_mode="Markdown"
    )

async def words_now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    words = get_three_words()
    message = "🌟 *ABA Group — Күнделікті ағылшын сөздері*\n\n"
    for i, w in enumerate(words, 1):
        message += f"*{i}. {w['word']}* {w['transcription']} — _{w['translation']}_\n"
        message += f"📝 {w['example']}\n"
        message += f"🔊 forvo.com/word/{w['word'].lower()}\n\n"
    await update.message.reply_text(message, parse_mode="Markdown")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("words", words_now))
    app.job_queue.run_daily(send_daily_words, time=time(hour=4, minute=0))
    app.run_polling()

if __name__ == "__main__":
    main()
