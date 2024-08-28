import os
import django

# Установите переменную окружения DJANGO_SETTINGS_MODULE на ваш файл с настройками
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'super_info_core.settings')

# Инициализируйте Django
django.setup()

from django.conf import settings
from django.core.files import File
import datetime
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_TOKEN_BOT
from news.models import Publication, Category, Hashtag
from news.views import LOID


SAVE_PATH = os.path.join(settings.MEDIA_ROOT, 'telegram_img/')
bot = TeleBot(API_TOKEN_BOT)
title = None
short_description = None
description = None
file_name = None
category_id = None
hashtags = []
hashtag_ids = []
selected_hashtags = []
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)


@bot.message_handler(commands=['create_category'])
def create_category(message):
    new_category = bot.send_message(message.chat.id, "Напишите название категории:")
    bot.register_next_step_handler(new_category, category)


def category(message):
    category_title = message.text
    Category.objects.create(title=category_title)
    bot.send_message(message.chat.id, "Новая категория создана.")


@bot.message_handler(commands=['create_hashtag'])
def create_hashtag(message):
    new_hashtag = bot.send_message(message.chat.id, "Напишите название хэштега:")
    bot.register_next_step_handler(new_hashtag, hashtag)


def hashtag(message):
    hashtag_title = message.text
    Hashtag.objects.create(title=hashtag_title)
    bot.send_message(message.chat.id, "Новый хэштег создан.")


@bot.message_handler(commands=['new'])
def new_blog(message):
    if message.chat.id == LOID:
        msg = bot.send_message(message.chat.id, "Напишите название публикации:")
        bot.register_next_step_handler(msg, blog_title)


def blog_title(message):
    global title
    title = message.text
    categories = Category.objects.all()
    category_list = "\n".join([f"{item.id}: {item.title}" for item in categories])
    msg = bot.send_message(message.chat.id, f"Отлично, теперь напишите id категории:\n{category_list}")
    bot.register_next_step_handler(msg, blog_category)


def blog_category(message):
    global category_id
    try:
        category_id = int(message.text)
        msg = bot.send_message(message.chat.id, "Отлично, теперь напишите короткое описание")
        bot.register_next_step_handler(msg, blog_short_description)
    except Exception:
        msg = bot.send_message(message.chat.id, "Произошла ошибка, попробуйте заново")
        bot.register_next_step_handler(msg, blog_category)


def blog_short_description(message):
    global short_description
    short_description = message.text
    msg = bot.send_message(message.chat.id, "Отлично, теперь напишите полное описание")
    bot.register_next_step_handler(msg, blog_description)


def blog_description(message):
    global description
    description = message.text
    hashtags = Hashtag.objects.all()
    hashtag_list = "\n".join([f"{item.id}: {item.title}" for item in hashtags])
    msg = bot.send_message(message.chat.id, f"Теперь выберите хэштеги по id:\n{hashtag_list}\n Пример использования: 1,3,4")
    bot.register_next_step_handler(msg, blog_hashtag)


def blog_hashtag(message):
    global selected_hashtags, hashtags, hashtag_ids
    try:
        hashtag_ids = message.text.split(",")
    except Exception:
        msg = bot.send_message(message.chat.id, "Произошла ошибка, попробуйте заново")
        bot.register_next_step_handler(msg, blog_hashtag)
    hashtags = []
    hashtag_list = []
    for item in hashtag_ids:
        hashtag = Hashtag.objects.get(id=int(item))
        hashtags.append(hashtag)
        selected_hashtags.append("\n".join([f"{hashtag.id}: {hashtag.title}"]))
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text="Все верно", callback_data="da")
    btn2 = InlineKeyboardButton(text="Заново", callback_data="net")
    markup.row(btn1, btn2)
    bot.send_message(message.chat.id, f"Выбранные хэштеги: {selected_hashtags}", reply_markup=markup)


def blog_image(message):
    global file_name
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        file_name = message.caption if message.caption else datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"{file_name}.jpg"

        file_path = os.path.join(SAVE_PATH, file_name)

        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, f'Ваше изображение сохранено как {file_name}')
        markup = InlineKeyboardMarkup()
        btn = InlineKeyboardButton(text="отправить", callback_data="send")
        markup.add(btn)
        bot.send_message(message.chat.id, "Ваша публикация готова", reply_markup=markup)

    except Exception as e:
        msg = bot.reply_to(message, f'Произошла ошибка: {str(e)}')
        bot.register_next_step_handler(msg, blog_image)


@bot.callback_query_handler()
def send_blog(callback):
    if callback.data == "send":
        file_path = os.path.join(SAVE_PATH, file_name)
        with open(file_path, 'rb') as f:
            django_file = File(f)
            blog = Publication.objects.create(
                title=title,
                category=Category.objects.get(id=category_id),
                short_description=short_description,
                description=description,
                image=django_file,
            )
            blog.hashtags.add(*hashtags)
        bot.send_message(callback.message.chat.id, "Публикация отправлена")
    elif callback.data == "da":
        msg = bot.send_message(callback.message.chat.id, "Отлично, теперь отправьте мне картину публикации")
        bot.register_next_step_handler(msg, blog_image)
    elif callback.data == "net":
        msg = bot.send_message(callback.message.chat.id, "Хорошо, заново выберите хэштеги")
        bot.register_next_step_handler(msg, blog_hashtag)


bot.infinity_polling()
