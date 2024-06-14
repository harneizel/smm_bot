from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import asyncio

from bot.database.requests import reset_to_zero_requests



# Функция, которая будет выполняться в 00:00
def scheduled_task():
    asyncio.run(reset_to_zero_requests())
    print("Сброс запросов выполнен")

# сбрасывает количество сделанных запросов в 00:00
def main():
    # Инициализируем планировщик
    scheduler = BlockingScheduler()
    scheduler.add_job(scheduled_task, trigger=CronTrigger(hour=0, minute=0))  # Запуск каждый день в 00:00
    print("scheduler инициализирован")
    try:
        scheduler.start()
    except:
        print("Завершение scheduler")
        scheduler.shutdown()

