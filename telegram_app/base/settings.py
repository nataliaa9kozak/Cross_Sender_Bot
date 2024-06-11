import os


SQL_ENGINE = os.environ.get('SQL_ENGINE', 'postgres')
SQL_USER = os.environ.get('SQL_USER', 'postgres')
SQL_PASSWORD = os.environ.get('SQL_PASSWORD', 'postgres')
SQL_HOST = os.environ.get('SQL_HOST', '5432')
SQL_PORT = os.environ.get('SQL_PORT', '5433')
SQL_DATABASE = os.environ.get('SQL_DATABASE', '')

REDIS_URL = os.environ.get('REDIS_URL', '')

BACKEND_URL = os.environ.get('BACKEND_URL', '')


# Telegram
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', '')


# Twitter
TWITTER_API_KEY = os.environ.get('TWITTER_API_KEY', '')
TWITTER_API_SECRET_KEY = os.environ.get('TWITTER_API_SECRET_KEY', '')
TWITTER_BEARER_TOKEN = os.environ.get('TWITTER_BEARER_TOKEN', '')
TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN', '')
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET', '')
TWITTER_CLIENT_ID = os.environ.get('TWITTER_CLIENT_ID', '')
TWITTER_CLIENT_SECRET = os.environ.get('TWITTER_CLIENT_SECRET', '')


# Facebook
FACEBOOK_ACCESS_TOKEN = os.environ.get('FACEBOOK_ACCESS_TOKEN', '')
FACEBOOK_PAGE_ID = os.environ.get('FACEBOOK_PAGE_ID', None)
