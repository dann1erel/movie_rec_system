import sqlalchemy as sa
from app.models import User, Genre, GenreLikes, MovieLikes
from config import Config

engine = sa.create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)

# Создание сессии
SessionLocal = sa.orm.sessionmaker(bind=engine)
session = SessionLocal()

def delete_user(user_id_list):
    for user_id in user_id_list:
        user = session.execute(sa.select(User).where(User.id == user_id)).scalar_one_or_none()
        if user is None:
            print(f"User with ID {user_id} not found.")
        else:
            session.delete(user)
    session.commit()


def delete_genres(genre_id_list):
    for genre_id in genre_id_list:
        genre = session.execute(sa.select(Genre).where(Genre.genre_id == genre_id)).scalar_one_or_none()
        if genre is None:
            print(f"User with ID {genre} not found.")
        else:
            session.delete(genre)
    session.commit()


def add_genres(genres):
    for genre_name in genres:
        genre = Genre(genre_name=genre_name)
        session.add(genre)
    session.commit()


def delete_genre_likes(genre_likes_id_list):
    for genre_id in genre_likes_id_list:
        genre_like_id = session.execute(sa.select(GenreLikes).where(GenreLikes.genre_id == genre_id)).scalar_one_or_none()
        if genre_like_id is None:
            print(f"User with ID {genre_like_id} not found.")
        else:
            session.delete(genre_like_id)
    session.commit()


if __name__ == "__main__":
    genres_list = ['драмы', 'комедии', 'зарубежные', 'мелодрамы', 'триллеры', 'русские', 'приключения',
            'боевики', 'документальное', 'криминал', 'детективы', 'фантастика', 'семейное',
            'ужасы', 'фэнтези', 'мультфильм', 'фильмы', 'для детей', 'советские', 'военные']
    for i in range(20):
        genres_list[i] = '#' + genres_list[i]


    user_id_list = [1, 2, 3, 4, 5]
    genre_like_id_list = [1, 2, 3, 4]

    # genre_id_list = [x for x in range(1, 21)]
    delete_user(user_id_list)
    # delete_genre_likes(genre_like_id_list)
    # delete_genres(genre_id_list)
    # add_genres(genres_list)
