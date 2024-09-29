import os

'''
Класс конфигурации
'''

class Config:
    # секретный ключ для генерации подписей или токенов
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'