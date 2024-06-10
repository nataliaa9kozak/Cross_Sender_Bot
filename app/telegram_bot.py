import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, filters
import tweepy
import requests
from io import BytesIO
from app.base.settings import TELEGRAM_TOKEN
from app.clients import TwitterClient


twitter_client = TwitterClient()

# Логування
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


# Функція для обробки команди /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Відправляє привітальне повідомлення та меню."""
    keyboard = [
        [InlineKeyboardButton("Надіслати твіт", callback_data='tweet')],
        [InlineKeyboardButton("Статус бота", callback_data='status')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Вітаю! Я ваш Телеграм бот. Що ви хочете зробити?', reply_markup=reply_markup)


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
    user_says = ' '.join(context.args)
    if user_says:
        if twitter_client.send_message(user_says):
            await update.message.reply_text('Успішно опубліковано у Twitter!')
        else:
            await update.message.reply_text('Помилка при надсиланні у Twitter.')
    else:
        await update.message.reply_text('Будь ласка, введіть текст, який ви хочете опублікувати.')


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


# Функція для обробки помилок
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Логування помилок, викликаних оновленнями."""
    logging.error(msg="Exception while handling an update:", exc_info=context.error)
    if isinstance(update, Update) and update.message:
        await update.message.reply_text('Виникла помилка. Спробуйте пізніше.')

def main() -> None:
    """Запускає бота."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("tweet", tweet))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_media_message))
    application.add_handler(CallbackQueryHandler(button))

    application.add_error_handler(error_handler)

    # Збільшення інтервалу опитування
    application.run_polling(poll_interval=5.0)  # Додавання інтервалу

if __name__ == '__main__':
    main()