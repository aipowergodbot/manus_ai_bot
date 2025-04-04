import os
import telebot
from telebot import types
import requests
from io import BytesIO

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(content_types=['video', 'document'])
def handle_video(message):
    file_info = bot.get_file(message.video.file_id if message.video else message.document.file_id)
    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}"
    
    response = requests.get(file_url)
    if response.status_code == 200:
        # Save or analyze the video
        video_data = BytesIO(response.content)
        bot.reply_to(message, "Video received. Analyzing faces and identifying actors... (Feature coming soon)")
    else:
        bot.reply_to(message, "Failed to download video.")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Send me a short video clip, and I’ll try to tell you the show or actors.")

bot.polling()
