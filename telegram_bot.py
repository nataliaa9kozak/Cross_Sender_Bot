import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, filters
import tweepy
import time
import requests
from io import BytesIO

# Заповніть наступні змінні своїми значеннями
TELEGRAM_TOKEN = '6661258189:AAGI2sUAZQXNPweGWO2RRoLf4W2urfFf1D4'
API_KEY = 'CNzrdKYT7bIQPt4smw3j8kV81'
API_SECRET_KEY = 'rDnyTckJBQt1rm2RyfLuJxahlOFVzky4c09p0PkO5IR1LAJ8My'
ACCESS_TOKEN = '1791183108571602944-2yMUvWWbLuyB71J5PKGpBKtDb1M6PL'
ACCESS_TOKEN_SECRET = 'B3LIZpq6dLEPWRwsPELHzlxiaK5ClNLeOWn9gBEFKiIjB'
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAFnHuAEAAAAAPOigsFR44gNrlNxZ%2FE9VL9CJ5sI%3DD82n1grMxh5QY1ZBfAv85aUKgjg0DoCvbVwqKLwugVDaPHjRBD'

# Аутентифікація з використанням ключів та токенів
client_v2 = tweepy.Client(bearer_token=BEARER_TOKEN, consumer_key=API_KEY, consumer_secret=API_SECRET_KEY,
                          access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
client_v1 = tweepy.API(auth)

# Логування
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Приклад функції для відправлення твітів
def send_tweet(message, media_ids=None):
    retries = 3
    for _ in range(retries):
        try:
            response = client_v2.create_tweet(text=message, media_ids=media_ids)
            print("Tweet sent:", response)
            return True
        except tweepy.TweepyException as e:
            print(f"Error: {e}")
            time.sleep(5)
    print("Failed to send tweet after retries")
    return False

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
        if send_tweet(user_says):
            await update.message.reply_text('Успішно опубліковано у Twitter!')
        else:
            await update.message.reply_text('Помилка при надсиланні у Twitter.')
    else:
        await update.message.reply_text('Будь ласка, введіть текст, який ви хочете опублікувати.')

# Функція для обробки текстових повідомлень
async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробляє текстові повідомлення."""
    user_says = update.message.text
    if send_tweet(user_says):
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
        media_response = client_v1.media_upload(filename="image.jpg", file=image)
        media_ids.append(media_response.media_id_string)
    except tweepy.TweepyException as e:
        print(f"Error uploading media: {e}")
        await update.message.reply_text('Помилка при завантаженні зображення у Twitter.')
        return

    if send_tweet(user_says, media_ids=media_ids):
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