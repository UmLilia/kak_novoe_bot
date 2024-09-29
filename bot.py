import logging
import os

from telegram import Update
from telegram.ext import Application

from tgbot.dispatcher import setup_handlers

TOKEN = os.environ['TOKEN']

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


def main():
    """ Run thr bot """
    application = Application.builder().token(TOKEN).build()
    application = setup_handlers(application)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
