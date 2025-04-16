import sqlalchemy as sa
from app.models import User, Genre, GenreLikes, MovieLikes, Movie, MovieGenre
from config import Config
from services.movies import Movies
from random import randint

engine = sa.create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)

# Создание сессии
SessionLocal = sa.orm.sessionmaker(bind=engine)
session = SessionLocal()

def delete_user(user_id_list):
    session.execute(
        sa.delete(User).where(User.id.in_(user_id_list))
    )
    session.commit()


def delete_genres(genre_id_list):
    session.execute(
        sa.delete(Genre).where(Genre.genre_id.in_(genre_id_list))
    )
    session.commit()


def add_genres(genres):
    for genre_name in genres:
        genre = Genre(genre_name=genre_name)
        session.add(genre)
    session.commit()


def add_movies():
    movies = Movies('kp_final')
    for i in range(movies.get_len()):
        data = movies.get_data_one_row(i)
        movie = Movie(id=data['id'], title=data['name_rus'], rating=data['kp_rating'],
                      duration=data['movie_duration'], rating_count=data['kp_rating_count'],
                      year=data['movie_year'], countries=data['countries'],
                      description=data['description'], poster=data['poster'], path=data['path'])
        session.add(movie)
    session.commit()


def add_movies_genre():
    movies = Movies('kp_final')
    for i in range(movies.get_len()):
        data = movies.get_data_one_row(i)
        movie_genres = list(map(lambda x: '#' + x, data['genres'].split(', ')))
        for genre in movie_genres:
            genre_id = session.execute(sa.select(Genre.genre_id).where(Genre.genre_name == genre)).scalar()
            if genre_id is  not None:
                movie_genre = MovieGenre(movie_id=data['id'], genre_id=genre_id)
                session.add(movie_genre)
    session.commit()
    # print(session.execute(sa.select(Genre.genre_id).where(Genre.genre_name.in_(list(map(lambda x: '#' + x, 'драма, комедия'.split(', ')))))).all())


def delete_movies(movies_id_list):
    session.execute(
        sa.delete(Movie).where(Movie.id.in_(movies_id_list))
    )
    session.commit()


def delete_genre_likes(user_id_likes_list):
    session.execute(
        sa.delete(GenreLikes).where(GenreLikes.user_id.in_(user_id_likes_list))
    )
    session.commit()


def delete_genre_movies(movie_id_list):
    session.execute(
        sa.delete(MovieGenre).where(MovieGenre.movie_id.in_(movie_id_list))
    )
    session.commit()


def get_random_movie():
    total = session.execute(sa.select(sa.func.count(Movie.id))).scalar()

    if not total:
        return "Нет роликов в базе"
    
    offset = randint(0, total - 1)
    stmt = sa.select(Movie).offset(offset).limit(1)
    movie = session.execute(stmt).scalar()

    return movie


def get_movie_genres(movie_id):
    genres_id_raw = session.execute(sa.select(MovieGenre.genre_id).where(MovieGenre.movie_id == movie_id)).all()
    genres_id = [row.genre_id for row in genres_id_raw]
    genres_name_raw = session.execute(sa.select(Genre.genre_name).where(Genre.genre_id.in_(genres_id))).all()
    genres_name = [row.genre_name for row in genres_name_raw]
    return genres_name


if __name__ == "__main__":
    movies = Movies('kp_final')
    genres_list = movies.get_genres()
    for i in range(20):
        genres_list[i] = '#' + genres_list[i]

    user_id_list = [1]
    genre_like_user_id_list = [1]
    movie_id_list = [326]


    # likes = session.execute(sa.select(GenreLikes).where(GenreLikes.user_id == 2)).scalars().all()
    # print(likes[0], likes[0].genre_id)

    # genre_id_list = [x for x in range(1, 21)]
    # delete_genre_likes(genre_like_user_id_list)
    # delete_user(user_id_list)
    # delete_genres(genre_id_list)
    # add_genres(genres_list)
    # add_movies()
    # delete_movies([326, 435, 448, 77044, 89518, 404900, 464963, 502838, 535341, 647823])
    # delete_genre_movies(movie_id_list)
    # add_movies_genre()
    # print(session.execute(sa.select(Genre.genre_id).where(Genre.genre_name == 'реальное ТВ')).scalar())
    movie_genres_id = session.execute(sa.select(MovieGenre.genre_id).where(MovieGenre.movie_id == 2997)).all()

    genres_id = [row.genre_id for row in movie_genres_id]

    print(genres_id)
