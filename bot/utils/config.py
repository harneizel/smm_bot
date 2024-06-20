from pathlib import Path

import yaml

config_dir = Path(__file__).parent.parent.parent.resolve()
config_path = config_dir / "config" / "config.yml"

with open(config_path, "r") as f:
    config = yaml.safe_load(f)

TG_TOKEN = config['TG_TOKEN']
PG_HOST = config['DB_FILE']
TIMEZONE = config['TIMEZONE']
CHANNEL_ID = config['CHANNEL_ID'] #имя канала без @
CHANNEL_URL = str(config['CHANNEL_URL'])
PAYMENTS_TOKEN = config['PAYMENTS_TOKEN']
PRICE = config['PRICE']
BASIC_LIMIT = config['BASIC_LIMIT']
PAID_LIMIT = config['PAID_LIMIT']
ADMIN_IDS = config['ADMIN_IDS']
COZE_URL = config['COZE_URL']
COZE_TOKEN = config['COZE_TOKEN']
COZE_BOT_ID = config['COZE_BOT_ID']
DG_API_KEY = config['DG_API_KEY']
MRH_LOGIN = config['MRH_LOGIN']
PASS_1 = config['PASS_1']
DESCRIPTION = config['DESCRIPTION']

SQLALCHEMY_URL = "sqlite+aiosqlite:///db.sqlite3"