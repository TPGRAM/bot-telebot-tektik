import os
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    filters,
    ContextTypes
)
from telegram.request import HTTPXRequest

TOKEN = "8560564631:AAFFJzIn26ASF7VZkIqmzWq461VqYH_7NX8"
CHANNEL_URL = "https://t.me/K1KKK5"  # 🔴 غيره لقناتك

DOWNLOAD_PATH = "downloads"
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

# ⚡ تحسين الاتصال
request = HTTPXRequest(
    connect_timeout=60,
    read_timeout=60,
    write_timeout=60
)

app = ApplicationBuilder().token(TOKEN).request(request).build()

# زر القناة
def get_button():
    keyboard = [
        [InlineKeyboardButton("اشترك بقناتي وتصير فكر بوت مجاني مح.", url=CHANNEL_URL)]
    ]
    return InlineKeyboardMarkup(keyboard)

# start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ ارسل رابط أو عدة روابط تيك توك")

# 📥 تحميل
async def download_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # استخراج كل الروابط
    urls = [u for u in text.split() if "tiktok.com" in u]

    if not urls:
        await update.message.reply_text("❌ دز رابط صح حب.")
        return

    await update.message.reply_text(f" ديحمل يابعد طويفي. {len(urls)} ")

    for url in urls:
        try:
            ydl_opts = {
                'outtmpl': f'{DOWNLOAD_PATH}/%(id)s.%(ext)s',
                'format': 'best[ext=mp4]/best',
                'quiet': True,
                'noplaylist': True,
                'concurrent_fragment_downloads': 5,  # ⚡ تسريع
                'retries': 3
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)

            # 🎥 فيديو
            if file_path.endswith(".mp4"):
                await update.message.reply_video(
                    video=open(file_path, 'rb'),
                    reply_markup=get_button()
                )

            # 🎧 صوت
            elif file_path.endswith((".mp3", ".m4a")):
                await update.message.reply_audio(
                    audio=open(file_path, 'rb'),
                    reply_markup=get_button()
                )

            # 🖼️ صور
            else:
                await update.message.reply_document(
                    document=open(file_path, 'rb'),
                    reply_markup=get_button()
                )

            os.remove(file_path)

        except Exception as e:
            await update.message.reply_text(f"❌ الرابط بي شي حب.:\n{url}")

# handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_tiktok))

print("🤖 البوت شغال بقوة 🔥")
app.run_polling(drop_pending_updates=True)
