# Взят из проекта, под доработку

import asyncio
import html
from datetime import datetime, timedelta

import pytz
from aiogram.types import BufferedInputFile

from bot.aiogram_bot.loader import bot
from bot.database.requests.reports import get_report_by_date, add_report, get_reports_last_7_days
from bot.utils.config import LOGCHAT_ID
from bot.utils.models import models

last_minute = -1
last_hour = -1


async def send_log(message, disable_notification=False, title_file=None, description_file=None):
    if title_file and description_file:
        file = BufferedInputFile(message.encode(), filename=str(title_file) + ".txt")
        await bot.send_document(LOGCHAT_ID, file, caption=description_file[:1020])
        return
    if len(message) > 4000:
        file = BufferedInputFile(message.encode(), filename="err.txt")

        await bot.send_document(LOGCHAT_ID, file, caption="undefinded error")

    else:
        await bot.send_message(LOGCHAT_ID, str(message)[:4090], disable_notification=disable_notification)
