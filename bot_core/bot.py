import os
import asyncio
from telebot.async_telebot import AsyncTeleBot, types
from asgiref.sync import sync_to_async
import django

from bot_core.settings import TELEGRAM_API_TOKEN

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bot_core.settings')
django.setup()

from admin_panel.models import TgUser, UserMessage, Topic

bot = AsyncTeleBot(TELEGRAM_API_TOKEN)


async def show_topics(message):
    topics = await sync_to_async(list)(Topic.objects.all())
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for topic in topics:
        markup.add(topic.name)
    await bot.send_message(message.chat.id, "Выберите тему:", reply_markup=markup)


@bot.message_handler(commands=['start'])
async def send_welcome(message):
    user, created = await sync_to_async(TgUser.objects.get_or_create)(user_id=message.from_user.id)

    if user.phone:
        await show_topics(message)
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
        user.phone = message.contact.phone_number
        user.username = message.from_user.username
        user.first_name = message.from_user.first_name
        user.last_name = message.from_user.last_name
        user.language_code = message.from_user.language_code
        await sync_to_async(user.save)()

        topics = await sync_to_async(list)(Topic.objects.all())
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        for topic in topics:
            markup.add(topic.name)
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

    topics = await sync_to_async(list)(Topic.objects.all())
    topic_names = [topic.name for topic in topics]

    if message.text in topic_names:
        topic = await sync_to_async(Topic.objects.get)(name=message.text)
        questions = await sync_to_async(list)(topic.questions.all())
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        for question in questions:
            markup.add(question.question_text)
        await bot.send_message(message.chat.id, "Выберите вопрос:", reply_markup=markup)
    else:
        for topic in topics:
            questions = await sync_to_async(list)(topic.questions.all())
            question_dict = {q.question_text: q.answer_text for q in questions}
            if message.text in question_dict:
                await bot.send_message(message.chat.id, question_dict[message.text],
                                       reply_markup=types.ReplyKeyboardRemove())

                return

        await bot.send_message(message.chat.id, "Извините, я не нашел ответа на ваш вопрос.")


def run_bot():
    asyncio.run(bot.polling())


if __name__ == '__main__':
    run_bot()
