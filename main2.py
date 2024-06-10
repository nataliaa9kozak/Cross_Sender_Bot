from requests_oauthlib import OAuth1Session, OAuth2Session
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
import logging

# Встановлення логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Ваш токен Telegram бота
TELEGRAM_TOKEN = '6661258189:AAGI2sUAZQXNPweGWO2RRoLf4W2urfFf1D4'

# Twitter OAuth конфігурація
TWITTER_API_KEY = 'YOUR_TWITTER_API_KEY'
TWITTER_API_SECRET_KEY = 'YOUR_TWITTER_API_SECRET_KEY'
TWITTER_CALLBACK_URI = 'YOUR_TWITTER_CALLBACK_URI'
TWITTER_REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
TWITTER_BASE_URL = 'https://api.twitter.com/'

# Instagram OAuth конфігурація
INSTAGRAM_CLIENT_ID = 'YOUR_INSTAGRAM_CLIENT_ID'
INSTAGRAM_CLIENT_SECRET = 'YOUR_INSTAGRAM_CLIENT_SECRET'
INSTAGRAM_REDIRECT_URI = 'YOUR_INSTAGRAM_REDIRECT_URI'
INSTAGRAM_AUTHORIZATION_URL = 'https://api.instagram.com/oauth/authorize'
INSTAGRAM_TOKEN_URL = 'https://api.instagram.com/oauth/access_token'

# Facebook OAuth конфігурація
FACEBOOK_CLIENT_ID = 'YOUR_FACEBOOK_CLIENT_ID'
FACEBOOK_CLIENT_SECRET = 'YOUR_FACEBOOK_CLIENT_SECRET'
FACEBOOK_REDIRECT_URI = 'https://yourapp.com/facebook/callback'
FACEBOOK_AUTHORIZATION_URL = 'https://www.facebook.com/v12.0/dialog/oauth'
FACEBOOK_TOKEN_URL = 'https://graph.facebook.com/v12.0/oauth/access_token'

# Функції команд
async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Login", callback_data='login'),
            InlineKeyboardButton("Schedule", callback_data='schedule'),
            InlineKeyboardButton("Post", callback_data='post'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Choose a command:', reply_markup=reply_markup)

async def login(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Login with Twitter", callback_data='login_twitter'),
            InlineKeyboardButton("Login with Instagram", callback_data='login_instagram'),
            InlineKeyboardButton("Login with Facebook", callback_data='login_facebook'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Choose a platform to log in:', reply_markup=reply_markup)

async def post(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Post function placeholder.')

async def schedule(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Schedule function placeholder.')

# Обробник кнопок
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'login':
        await login(update, context)
    elif query.data == 'login_twitter':
        await twitter_oauth_login(update, context)
    elif query.data == 'login_instagram':
        await instagram_oauth_login(update, context)
    elif query.data == 'login_facebook':
        await facebook_oauth_login(update, context)
    elif query.data == 'post':
        await post(update, context)
    elif query.data == 'schedule':
        await schedule(update, context)

# Функція авторизації Twitter
async def twitter_oauth_login(update: Update, context: CallbackContext) -> None:
    try:
        oauth = OAuth1Session(
            client_key=TWITTER_API_KEY,
            client_secret=TWITTER_API_SECRET_KEY,
            callback_uri=TWITTER_CALLBACK_URI
        )
        fetch_response = oauth.fetch_request_token(TWITTER_REQUEST_TOKEN_URL)
        resource_owner_key = fetch_response.get('oauth_token')
        resource_owner_secret = fetch_response.get('oauth_token_secret')

        base_authorization_url = TWITTER_BASE_URL + 'oauth/authorize'
        authorization_url = oauth.authorization_url(base_authorization_url)
        await update.callback_query.message.reply_text(f'Please go here and authorize: {authorization_url}')
    except Exception as e:
        logger.error(f'Error during Twitter OAuth login: {e}')
        await update.callback_query.message.reply_text('Failed to start Twitter login process.')

# Функція авторизації Instagram
async def instagram_oauth_login(update: Update, context: CallbackContext) -> None:
    try:
        oauth = OAuth2Session(
            client_id=INSTAGRAM_CLIENT_ID,
            redirect_uri=INSTAGRAM_REDIRECT_URI,
            scope=["user_profile", "user_media"]
        )
        authorization_url, state = oauth.authorization_url(INSTAGRAM_AUTHORIZATION_URL)
        context.user_data['oauth_state'] = state
        await update.callback_query.message.reply_text(f'Please go here and authorize: {authorization_url}')
    except Exception as e:
        logger.error(f'Error during Instagram OAuth login: {e}')
        await update.callback_query.message.reply_text('Failed to start Instagram login process.')

# Функція авторизації Facebook
async def facebook_oauth_login(update: Update, context: CallbackContext) -> None:
    try:
        oauth = OAuth2Session(
            client_id=FACEBOOK_CLIENT_ID,
            redirect_uri=FACEBOOK_REDIRECT_URI,
            scope=["public_profile", "email"]
        )
        authorization_url, state = oauth.authorization_url(FACEBOOK_AUTHORIZATION_URL)
        context.user_data['oauth_state'] = state
        await update.callback_query.message.reply_text(f'Please go here and authorize: {authorization_url}')
    except Exception as e:
        logger.error(f'Error during Facebook OAuth login: {e}')
        await update.callback_query.message.reply_text('Failed to start Facebook login process.')

# Основний запуск програми
if __name__ == '__main__':
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Додаємо обробники команд
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))

    # Запускаємо бота
    application.run_polling()
