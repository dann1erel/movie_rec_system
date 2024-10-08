from typing import Optional # используется для того, чтобы можно было указать, что значение может быть отсутствующим (либо определённый тип, либо None)
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin # безопасные реализации обязательных элементов для flask login
from app import db, login


'''
В этом файле определяются таблицы базы данных
'''


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


# таблица users
class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(128), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    # для связи высокоуровневое представление базы взаимосвязи, а не фактическое поле
    likes: so.WriteOnlyMapped['Like'] = so.relationship(back_populates='user')


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)


    # как печатать объекты этого класса
    def __repr__(self):
        return '<User {}>'.format(self.username)


# таблица likes, где находятся лайки пользователей, по этим данным строить алгоритм??? ONE-TO-MANY
class Like(db.Model):
    movie_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    # для связи высокоуровневое представление базы взаимосвязи, а не фактическое поле
    user: so.Mapped['User'] = so.relationship(back_populates='likes')


    # как печатать объекты этого класса
    def __repr__(self):
        return '<Movie ID {}>'.format(self.movie_id)