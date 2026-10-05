import os
import re
import telebot
import yt_dlp

TOKEN = "8963960026:AAHo5TMAlfNDjqhItsoY3AlxsqUGPxhl29Q"

bot = telebot.TeleBot(TOKEN)

URL_RE = re.compile(r"https?://\S+")

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "👋 Salom!\n\n"
        "Video yoki audio havolasini yuboring."
    )

@bot.message_handler(func=lambda message: True)
def download_media(message):
    match = URL_RE.search(message.text or "")

    if not match:
        bot.reply_to(message, "❌ Havola topilmadi.")
        return

    url = match.group(0)
    status = bot.reply_to(message, "⏳ Yuklanmoqda...")

    os.makedirs("downloads", exist_ok=True)

    options = {
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "format": "best[ext=mp4]/best",
        "noplaylist": True,
        "quiet": True
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        if not os.path.exists(filename):
            raise Exception("Fayl topilmadi")

        with open(filename, "rb") as video:
            bot.send_video(
                message.chat.id,
                video,
                caption="✅ Tayyor"
            )

        os.remove(filename)

        bot.delete_message(
            message.chat.id,
            status.message_id
        )

    except Exception as e:
        bot.edit_message_text(
            "❌ Bu havolani yuklab bo‘lmadi.",
            message.chat.id,
            status.message_id
        )

print("🤖 Bot ishga tushdi...")
bot.infinity_polling()
