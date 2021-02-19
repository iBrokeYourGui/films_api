import os
import pathlib

BASE_DIR = pathlib.Path(__file__).parent


class Config():
    # os.environ.get('DATABASE_URL' - для подключения postgres на heroku
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL' or 'sqlite:///' + str(BASE_DIR / "data" / "db.sqlite3"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Вот аткую строку лучше автогенераторами создать uuid например
    SECRET_KEY = 'you-will-never-know'
