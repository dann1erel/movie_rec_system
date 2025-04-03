import sqlalchemy as sa
from app.models import User, Genre, GenreLikes, MovieLikes
from config import Config
from services.movies import Movies

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


def delete_genre_likes(user_id_likes_list):
    session.execute(
        sa.delete(GenreLikes).where(GenreLikes.user_id.in_(user_id_likes_list))
    )
    session.commit()


if __name__ == "__main__":
    movies = Movies('kp_final')
    genres_list = movies.get_genres()
    for i in range(20):
        genres_list[i] = '#' + genres_list[i]

    user_id_list = [1]
    genre_like_user_id_list = [1]

    # likes = session.execute(sa.select(GenreLikes).where(GenreLikes.user_id == 2)).scalars().all()
    # print(likes[0], likes[0].genre_id)

    genre_id_list = [x for x in range(1, 21)]
    # delete_genre_likes(genre_like_user_id_list)
    # delete_user(user_id_list)
    delete_genres(genre_id_list)
    add_genres(genres_list)
