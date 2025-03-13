from flask import Flask
from config import Config
# оболочка для пакета SQLAlschemy, который представляет собой объектно-реляционное отображение
from flask_sqlalchemy import SQLAlchemy
# оболочка для пакета Alembic, который представляет собой платформу миграции баз данных для SQLAlchemy
from flask_migrate import Migrate
# для управления состоянием входа пользователей
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# функция просмотра, которая обрабатывает логины
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models