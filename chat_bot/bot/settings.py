import os

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from dotenv import load_dotenv
import logging

from sqlalchemy import create_engine

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
LOGGER = logging.getLogger(__name__)


BASE_DIR = os.path.abspath(os.getcwd())
load_dotenv(f'{BASE_DIR}/.env')

TOKEN = os.getenv("TOKEN")

DATABASES = {
    "ENGINE": os.getenv("DB_ENGINE", default="django.db.backends.postgresql"),
    "NAME": os.getenv("POSTGRES_DB", default="julias_db"),
    "USER": os.getenv("POSTGRES_USER", default="npronichev"),
    "PASSWORD": os.getenv("POSTGRES_PASSWORD", default="julias_user"),
    "HOST": os.getenv("POSTGRES_HOST", default="localhost"),
    "PORT": os.getenv("POSTGRES_PORT", default=5432)
}

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{DATABASES['USER']}:{DATABASES['PASSWORD']}@" \
                          f"{DATABASES['HOST']}/{DATABASES['NAME']}"

ENGINE = create_engine(
    SQLALCHEMY_DATABASE_URL
)

STORAGE = RedisStorage2(host=os.getenv("REDIS_HOST"),
                        port=int(os.getenv("REDIS_PORT")),
                        db=3,
                        prefix='fsm_key')

ADMIN_ID = 1234
