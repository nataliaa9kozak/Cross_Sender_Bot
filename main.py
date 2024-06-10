from dotenv import load_dotenv


load_dotenv(override=True)


import app.base.settings
from app.telegram_bot import main as tg_main


def main():
    tg_main()


if __name__ == '__main__':
    main()
