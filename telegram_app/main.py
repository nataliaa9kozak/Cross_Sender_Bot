import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler
import tweepy
import requests
from io import BytesIO
from base.settings import TELEGRAM_TOKEN
from clients import TwitterClient, BackendClient
from typing import Dict
import re
from enum import Enum, auto
import json
from utils import format_user_input


backend_client = BackendClient()
twitter_client = TwitterClient()

# Логування
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


class AppStates(Enum):
    START = auto()
    REGISTRATION_WAITING_EMAIL = auto()
    MENU = auto()
    TWEET = auto()
    CONFIG_MENU = auto()
    CONFIGS = auto()
    CONFIG_UPDATE = auto()


# Registration
cancel_word = 'cancel'
configs_command = 'configs'
view_command = 'view'
update_command = 'update'
cancel_markup = ReplyKeyboardMarkup([[cancel_word]])
menu_markup = ReplyKeyboardMarkup([["tweet", "status", "configs"], [cancel_word]])
configs_markup = ReplyKeyboardMarkup([[view_command, update_command], [cancel_word]])


# Функція для обробки команди /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Відправляє привітальне повідомлення та меню."""
    exist = await backend_client.is_telegram_id_exist(update.message.from_user.id)
    if not exist:
        await update.message.reply_text('Ви не зареєстровані, напишіть /register, щоб зареєструватись.')
        return ConversationHandler.END
    await update.message.reply_text('Вітаю! Я ваш Телеграм бот. Що ви хочете зробити?', reply_markup=menu_markup)
    return AppStates.MENU


# Функція для обробки команд меню
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробляє вибір користувача з меню."""
    query = update.callback_query
    await query.answer()

    if query.data == 'tweet':
        await query.edit_message_text(text="Введіть текст, який ви хочете опублікувати у Twitter:")
    elif query.data == 'status':
        await query.edit_message_text(text="Бот працює нормально.")


# Функція для обробки команди /tweet
async def tweet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отримує текст з повідомлення та надсилає його у Twitter."""
    await update.message.reply_text('Будь ласка, введіть текст, який ви хочете опублікувати.', reply_markup=cancel_markup)
    return AppStates.TWEET


# Функція для обробки текстових повідомлень
async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробляє текстові повідомлення."""
    user_says = update.message.text
    if twitter_client.send_message(user_says):
        await update.message.reply_text('Успішно опубліковано у Twitter!')
    else:
        await update.message.reply_text('Помилка при надсиланні у Twitter.')


# Функція для обробки медіа повідомлень
async def handle_media_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробляє медіа повідомлення (фото) та надсилає їх у Twitter."""
    media_files = update.message.photo
    user_says = update.message.caption or ""

    if not media_files:
        await update.message.reply_text('Будь ласка, надішліть зображення.')
        return# Обираємо найбільше за розміром зображення для кожного фото
    largest_photo = max(media_files, key=lambda x: x.file_size)

    media_ids = []
    file = await largest_photo.get_file()
    file_path = file.file_path
    response = requests.get(file_path)
    image = BytesIO(response.content)

    try:
        media_response = twitter_client.send_media(image)
        media_ids.append(media_response.media_id_string)
    except tweepy.TweepyException as e:
        print(f"Error uploading media: {e}")
        await update.message.reply_text('Помилка при завантаженні зображення у Twitter.')
        return

    if twitter_client.send_message(user_says, media_ids=media_ids):
        await update.message.reply_text('Успішно опубліковано у Twitter!')
    else:
        await update.message.reply_text('Помилка при надсиланні у Twitter.')


async def cancel_tweet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Відмінити твіт")
    return ConversationHandler.END


# Функція для обробки помилок
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Логування помилок, викликаних оновленнями."""
    logging.error(msg="Exception while handling an update:", exc_info=context.error)
    if isinstance(update, Update) and update.message:
        await update.message.reply_text('Виникла помилка. Спробуйте пізніше.')


def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])


async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""
    id_exist = await backend_client.is_telegram_id_exist(update.message.from_user.id)
    if id_exist:
        await update.message.reply_text("Ви вже зареєстровані", reply_markup=menu_markup)
        return AppStates.MENU
    await update.message.reply_text("Введіть пошту", reply_markup=cancel_markup)

    return AppStates.REGISTRATION_WAITING_EMAIL


async def email_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    email = update.message.text
    email_exist = await backend_client.is_email_exist(email)

    if email_exist:
        await update.message.reply_text("Ця пошта вже зареєстрована", reply_markup=cancel_markup)
        return AppStates.REGISTRATION_WAITING_EMAIL

    if (re.match(r'^[^@]+@[^@]+\.[^@]+$', email)):
        print('update.message.from_user', update.message.from_user)
        await backend_client.create_user(email=email, telegram_id=update.message.from_user.id)
        await update.message.reply_text(f"Success", reply_markup=ReplyKeyboardRemove())
    else:
        await update.message.reply_text("Пошта не валідна")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Відмінити", ReplyKeyboardRemove())
    return ConversationHandler.END


async def configs_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Конфіги', reply_markup=configs_markup)
    return AppStates.CONFIG_MENU


async def view_configs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    configs = await backend_client.get_configs(update.message.from_user.id)
    await update.message.reply_text(json.dumps(configs), reply_markup=configs_markup)
    return AppStates.CONFIG_MENU


async def update_config_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        'Update or create if not exist:\n'
        + 'Update structure:\n'
        + 'social_media\n'
        + 'KEY=VALUE\n'
        + 'KEY=VALUE\n',
        reply_markup=configs_markup
    )
    return AppStates.CONFIG_UPDATE


async def update_config(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    social_media, content = format_user_input(update.message.text)
    print(social_media, content)

    await backend_client.update_config(
        social_media=social_media,
        content=content,
        telegram_id=update.message.from_user.id
    )
    await update.message.reply_text(
        'Збережено', reply_markup=configs_markup
    )
    return AppStates.CONFIG_MENU


def main() -> None:
    """Запускає бота."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # conversation example
    # https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/conversationbot2.py
    register_handler = ConversationHandler(
        entry_points=[
            CommandHandler("register", register),
            CommandHandler("start", start),
            CommandHandler("tweet", tweet),
            # CommandHandler("configs", configs_menu)
        ],
        states={
            AppStates.REGISTRATION_WAITING_EMAIL: [
                MessageHandler(
                    filters.TEXT,
                    email_input
                ),
            ],
            AppStates.MENU: [
                MessageHandler(
                    filters.Regex("^tweet"),
                    tweet
                ),
                MessageHandler(
                    filters.Text(configs_command),
                    configs_menu
                ),
            ],
            AppStates.TWEET: [
                MessageHandler(
                    filters.TEXT,
                    handle_text_message
                ),
            ],
            AppStates.CONFIG_MENU: [
                MessageHandler(
                    filters.Regex(f"^{view_command}"),
                    view_configs
                ),
                MessageHandler(
                    filters.Text(update_command),
                    update_config_menu
                ),
            ],
            AppStates.CONFIG_UPDATE: [
                MessageHandler(
                    filters.TEXT,
                    update_config
                ),
            ],
        },
        fallbacks=[MessageHandler(filters.Regex(f"^{cancel_word}$"), cancel)],
    )
    application.add_handler(register_handler)

    application.add_error_handler(error_handler)

    # Збільшення інтервалу опитування
    application.run_polling(poll_interval=5.0)  # Додавання інтервалу


if __name__ == '__main__':
    main()
