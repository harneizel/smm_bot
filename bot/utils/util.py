import pytz
import datetime
import time
import hashlib
import urllib.parse as parse


from bot.utils.config import TIMEZONE, ROBOKASSA_PAYMENT_URL

def get_epoch():
    tz = pytz.timezone(TIMEZONE)
    current_time = datetime.datetime.now(tz)
    print(current_time)
    epoch = int(time.mktime(current_time.timetuple()))
    print(epoch)
    return epoch

print(get_epoch())

def calculate_signature(*args) -> str:
    """Create signature MD5.
    """
    return hashlib.md5(':'.join(str(arg) for arg in args).encode()).hexdigest()

def generate_payment_link(
    merchant_login: str,  # Merchant login
    merchant_password_1: str,  # Merchant password
    cost: float,  # Cost of goods, RU
      # Invoice number
    description: str,  # Description of the purchase
    is_test: int,
    Shp_id: int,
    robokassa_payment_url: str,
) -> str:
    """URL for redirection of the customer to the service.
    """
    signature = calculate_signature(
        merchant_login,
        cost,
        merchant_password_1,
        Shp_id
    )

    print(signature)
    data = {
        'MerchantLogin': merchant_login,
        'OutSum': cost,
        #'InvId': number,
        'Description': description,
        'SignatureValue': signature,
        'IsTest': is_test
    }
    return f'{robokassa_payment_url}?{parse.urlencode(data)}'