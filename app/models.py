# используется для того, чтобы можно было указать, что значение может быть отсутствующим (либо определённый тип, либо None)
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

'''
В этом файле определяются таблицы базы данных
'''

# таблица users
class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(128), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    # для связи высокоуровневое представление базы взаимосвязи, а не фактическое поле
    likes: so.WriteOnlyMapped['Like'] = so.relationship(back_populates='author')

    # как печатать объекты этого класса
    def __repr__(self):
        return '<User {}>'.format(self.username)


# таблица likes, где находятся лайки пользователей, по этим данным строить алгоритм??? ONE-TO-MANY
class Like(db.Model):
    movie_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    # для связи высокоуровневое представление базы взаимосвязи, а не фактическое поле
    users: so.WriteOnlyMapped['User'] = so.relationship(back_populates='likes')

        # как печатать объекты этого класса
    def __repr__(self):
        return '<Movie ID {}>'.format(self.movie_id)