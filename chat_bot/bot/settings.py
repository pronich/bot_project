import os
from dotenv import load_dotenv
import logging

from sqlalchemy import create_engine

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
LOGGER = logging.getLogger(__name__)


BASE_DIR = '/'.join(os.path.abspath(os.getcwd()).split('/')[:-1])
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
print(SQLALCHEMY_DATABASE_URL)

ENGINE = create_engine(
    SQLALCHEMY_DATABASE_URL
)
