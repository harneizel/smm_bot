import asyncio
import logging
import sys
from threading import Thread
from bot.utils.scheduler import main

from bot.aiogram_bot.app import aiogram_start



if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        thread1 = Thread(target=main)
        thread1.start()
        asyncio.run(aiogram_start())
    except KeyboardInterrupt:
        print("Goodbye!")
