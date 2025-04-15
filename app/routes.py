from flask import render_template, flash, redirect, url_for, request, session
from urllib.parse import urlsplit
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import app, db
from app.forms import LoginForm, RegistrationForm, CheckboxForm # GenreCheckboxForm
from app.models import User, Genre, GenreLikes, MovieLikes
from services.movies import Movies


@app.route('/')
@app.route('/index')
@login_required
def index():
    movies = Movies('kp_final')
    return render_template('index.html', title='Лента', data=movies.get_data_one_row(0))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        login_user(user, remember=form.remember_me.data)

        # Если remember_me=False, делаем сессию временной
        if form.remember_me.data == False:
            session.permanent = False  # Сессия будет удалена при закрытии браузера
        else:
            session.permanent = True

        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Вход', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=False)
        return redirect(url_for('genres'))
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    genre_likes = db.session.execute(sa.select(GenreLikes).where(GenreLikes.user_id == user.id)).scalars().all()
    genres = []

    for like in genre_likes:
        genre = db.session.scalar(sa.select(Genre).where(Genre.genre_id == like.genre_id))
        genres.append(genre.genre_name)

    print(genres)

    likes = [
        {'user_id': user, 'movie_id': 1},
        {'user_id': user, 'movie_id': 1},
    ]
    return render_template('user.html', user=user, genres=genres)


@app.route('/genres', methods=['GET', 'POST'])
def genres():
    form = CheckboxForm()
    checkboxes = [form.field_1, form.field_2, form.field_3, form.field_4, form.field_5, form.field_6,
                form.field_7, form.field_8, form.field_9, form.field_10, form.field_11, form.field_12,
                form.field_13, form.field_14, form.field_15, form.field_16, form.field_17, form.field_18,
                form.field_19, form.field_20]
  
    if form.validate_on_submit():
        for ch in checkboxes:
            if ch.data == True:
                genre = db.session.scalar(sa.select(Genre).where(Genre.genre_name == ch.label.text))
                db_genre_id = genre.genre_id
                db_user_id = current_user.id
                genre_like = GenreLikes(genre_id=db_genre_id, user_id=db_user_id)
                db.session.add(genre_like)
                db.session.commit()
        return redirect(url_for('index'))

    return render_template('genres.html', title='Жанры', form=form, checkboxes=checkboxes)