from pathlib import Path

import yaml

config_dir = Path(__file__).parent.parent.parent.resolve()
config_path = config_dir / "config" / "config.yml"

with open(config_path, "r") as f:
    config = yaml.safe_load(f)

TG_TOKEN = config['TG_TOKEN']

PG_HOST = config['DB_FILE']

TIMEZONE = config['TIMEZONE']

CHANNEL_ID = config['CHANNEL_URL'][13:] #имя канала без @

CHANNEL_URL = config['CHANNEL_URL']

SQLALCHEMY_URL = "sqlite+aiosqlite:///db.sqlite3"