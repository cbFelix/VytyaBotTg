import os
import asyncio
from telebot.async_telebot import AsyncTeleBot, types
from asgiref.sync import sync_to_async
from threading import Thread
import django

from admin_panel.questions import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bot_core.settings')
django.setup()

from admin_panel.models import TgUser, UserMessage
from bot_core.settings import TELEGRAM_API_TOKEN

bot = AsyncTeleBot(TELEGRAM_API_TOKEN)


@bot.message_handler(commands=['start'])
async def send_welcome(message):
    # тут крч простая проверка есть ли пользователь в базе
    user, created = await sync_to_async(TgUser.objects.get_or_create)(user_id=message.from_user.id)

    if user.phone:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add("Машины", "Технологии")
        await bot.send_message(message.chat.id, "Добро пожаловать! Выберите интересующую вас тему.",
                               reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        button_phone = types.KeyboardButton(text="Поделиться номером телефона", request_contact=True)
        markup.add(button_phone)
        await bot.send_message(message.chat.id, "Пожалуйста, поделитесь вашим номером телефона для регистрации.",
                               reply_markup=markup)


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

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add("Машины", "Технологии")
        await bot.send_message(message.chat.id, "Спасибо за регистрацию! Теперь выберите интересующую вас тему.",
                               reply_markup=markup)


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


@bot.message_handler(commands=['topics'])
async def show_topics(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    buttons = [types.KeyboardButton(text="Car"), types.KeyboardButton(text="Technology")]
    markup.add(*buttons)
    await bot.send_message(message.chat.id, "Выберите тему:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in ["Car", "Technology"])
async def handle_topic_selection(message):
    questions = []
    if message.text == "Car":
        questions = Car.get_questions()
    elif message.text == "Technology":
        questions = Technology.get_questions()

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for q in questions:
        markup.add(types.KeyboardButton(text=q["question"]))
    await bot.send_message(message.chat.id, "Выберите вопрос:", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
async def handle_question(message):
    all_questions = Car.get_questions() + Technology.get_questions()

    for q in all_questions:
        if message.text == q["question"]:
            await bot.send_message(message.chat.id, q["answer"], reply_markup=types.ReplyKeyboardRemove())
            return

    await bot.send_message(message.chat.id, "Извините, я не нашел ответа на ваш вопрос.")


def set_token(new_token):
    global TELEGRAM_API_TOKEN
    TELEGRAM_API_TOKEN = new_token
    bot = AsyncTeleBot(TELEGRAM_API_TOKEN)


if __name__ == '__main__':
    run_bot()
