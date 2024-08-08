import os
import django
import asyncio
from telebot.async_telebot import AsyncTeleBot, types
from asgiref.sync import sync_to_async
from threading import Thread

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bot_core.settings')
django.setup()

from admin_panel.models import TgUser, UserMessage
from bot_core.settings import TELEGRAM_API_TOKEN

bot = AsyncTeleBot(TELEGRAM_API_TOKEN)

@bot.message_handler(commands=['start'])
async def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Share Phone Number", request_contact=True)
    markup.add(button_phone)
    await bot.send_message(message.chat.id, "Welcome! Please share your phone number.", reply_markup=markup)

@bot.message_handler(content_types=['contact'])
async def contact_handler(message):
    if message.contact:
        user, created = await sync_to_async(TgUser.objects.get_or_create)(user_id=message.from_user.id)
        user.username = message.from_user.username
        user.first_name = message.from_user.first_name
        user.last_name = message.from_user.last_name
        user.language_code = message.from_user.language_code
        user.phone = message.contact.phone_number
        await sync_to_async(user.save)()
        await bot.send_message(message.chat.id, "Thank you for sharing your phone number!", reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(func=lambda message: True)
async def handle_message(message):
    user, created = await sync_to_async(TgUser.objects.get_or_create)(user_id=message.from_user.id)
    await sync_to_async(UserMessage.objects.create)(
        user=user,
        message_text=message.text,
        date_received=message.date
    )

# Bot Management

def run_bot():
    asyncio.run(bot.polling())

def get_users():
    return TgUser.objects.all()

def stop_bot():
    pass

def set_token(new_token):
    global TELEGRAM_API_TOKEN
    TELEGRAM_API_TOKEN = new_token
    bot = AsyncTeleBot(TELEGRAM_API_TOKEN)

if __name__ == '__main__':
    run_bot()
