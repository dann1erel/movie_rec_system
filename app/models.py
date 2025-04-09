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
    movie_likes: so.Mapped['MovieLikes'] = so.relationship(back_populates='user')
    genre_likes: so.Mapped['GenreLikes'] = so.relationship(back_populates='user')


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)


    # как печатать объекты этого класса
    def __repr__(self):
        return '<User {}>'.format(self.username)
    

class Movie(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    rating: so.Mapped[float] = so.mapped_column(sa.Float, index=True)
    duration: so.Mapped[int] = so.mapped_column(sa.Integer, index=True)
    rating_count: so.Mapped[int] = so.mapped_column(sa.Integer, index=True)
    year: so.Mapped[int] = so.mapped_column(sa.Integer, index=True)
    # genres через новую таблицу 
    countries: so.Mapped[str] = so.mapped_column(sa.String(128), index=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(2048), index=True)
    poster: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)

    movie_genre: so.Mapped['MovieGenre'] = so.relationship(back_populates='movie')
    movie_likes: so.Mapped['MovieLikes'] = so.relationship(back_populates='movie')


    # как печатать объекты этого класса
    def __repr__(self):
        return '<Movie ID {}; Title {}>'.format(self.id, self.title)
 

# таблица movie, где находятся лайки фильмов пользователей, по этим данным строить алгоритм??? ONE-TO-MANY
class MovieLikes(db.Model):
    movie_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Movie.id), index=True, primary_key=True) # тут надо разобраться с ключами типа должна быть ещё таблица для хранения видиков
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True, primary_key=True)

    # для связи высокоуровневое представление базы взаимосвязи, а не фактическое поле
    user: so.Mapped['User'] = so.relationship(back_populates='movie_likes')
    movie: so.Mapped['Movie'] = so.relationship(back_populates='movie_likes')

    # как печатать объекты этого класса
    def __repr__(self):
        return '<Movie ID {}; User ID {}>'.format(self.movie_id, self.user_id)
    

# таблица genre, где находятся любимые жанры пользователей
class Genre(db.Model):
    genre_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    genre_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)

    genre_likes: so.Mapped['GenreLikes'] = so.relationship(back_populates='genre')
    movie_genre: so.Mapped['MovieGenre'] = so.relationship(back_populates='genre')


    # как печатать объекты этого класса
    def __repr__(self):
        return '<Genre ID {}; Genre name {}>'.format(self.genre_id, self.genre_name)
    

class MovieGenre(db.Model):
    movie_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Movie.id), index=True, primary_key=True)
    genre_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Genre.genre_id), index=True, primary_key=True)

    movie: so.Mapped['Movie'] = so.relationship(back_populates='movie_genre')
    genre: so.Mapped['Genre'] = so.relationship(back_populates='movie_genre')
    

    # как печатать объекты этого класса
    def __repr__(self):
        return '<Movie ID {}; Genre ID {}>'.format(self.movie_id, self.genre_id)
    

# таблица genre_likes где хранятся жанры, которые пользователь отметил как любимые
class GenreLikes(db.Model):
    genre_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Genre.genre_id), index=True, primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True, primary_key=True)

    user: so.Mapped['User'] = so.relationship(back_populates='genre_likes')
    genre: so.Mapped['Genre'] = so.relationship(back_populates='genre_likes')


    # как печатать объекты этого класса
    def __repr__(self):
        return '<Genre ID {}; User ID {}>'.format(self.genre_id, self.user_id)
