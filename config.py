import os
# абсолютный путь к аудитории, в которой находится данный файл
basedir = os.path.abspath(os.path.dirname(__file__))

'''
Класс конфигурации
'''

class Config:
    # секретный ключ для генерации подписей или токенов
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # конфигурация для SQLAlchemy и бд SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
