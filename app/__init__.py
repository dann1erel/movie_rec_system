from flask import Flask
from config import Config
# оболочка для пакета SQLAlschemy, который представляет собой объектно-реляционное отображение
from flask_sqlalchemy import SQLAlchemy
# оболочка для пакета Alembic, который представляет собой платформу миграции баз данных для SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models