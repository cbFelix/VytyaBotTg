import asyncio

from telebot.async_telebot import AsyncTeleBot
from telebot import *
from threading import Thread

from config import TELEGRAM_API_TOKEN

bot = AsyncTeleBot(TELEGRAM_API_TOKEN)


@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    text = "Hello!"
    await bot.reply_to(message, text)

# Bot Management


def run_bot():
    Thread.start(asyncio.run(bot.polling()))


def get_users():
    pass


def stop_bot():
    pass





