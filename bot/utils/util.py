import pytz
import datetime
import time

from bot.utils.config import TIMEZONE

def get_epoch():
    tz = pytz.timezone(TIMEZONE)
    current_time = datetime.datetime.now(tz)
    print(current_time)
    epoch = int(time.mktime(current_time.timetuple()))
    print(epoch)
    return epoch

print(get_epoch())