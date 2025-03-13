from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList, FormField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
import sqlalchemy as sa
from app import db
from app.models import User


# форма входа
class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    
    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('Логин занят')
        
    
    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError('Email занят')


# class GenreCheckboxForm(FlaskForm):
#     checked = BooleanField()

class CheckboxForm(FlaskForm):
    checkboxes = []
    genres_list = ['драмы', 'комедии', 'зарубежные', 'мелодрамы', 'триллеры', 'русские', 'приключения',
            'боевики', 'документальное', 'криминал', 'детективы', 'фантастика', 'семейное',
            'ужасы', 'фэнтези', 'мультфильм', 'фильмы', 'для детей', 'советские', 'военные']
    
    # я дико извиняюсь но оно по-другому не работает

    field_1 = BooleanField(f'#{genres_list[0]}')
    field_2 = BooleanField(f'#{genres_list[1]}')
    field_3 = BooleanField(f'#{genres_list[2]}')
    field_4 = BooleanField(f'#{genres_list[3]}')
    field_5 = BooleanField(f'#{genres_list[4]}')
    field_6 = BooleanField(f'#{genres_list[5]}')
    field_7 = BooleanField(f'#{genres_list[6]}')
    field_8 = BooleanField(f'#{genres_list[7]}')
    field_9 = BooleanField(f'#{genres_list[8]}')
    field_10 = BooleanField(f'#{genres_list[9]}')
    field_11 = BooleanField(f'#{genres_list[10]}')
    field_12 = BooleanField(f'#{genres_list[11]}')
    field_13 = BooleanField(f'#{genres_list[12]}')
    field_14 = BooleanField(f'#{genres_list[13]}')
    field_15 = BooleanField(f'#{genres_list[14]}')
    field_16 = BooleanField(f'#{genres_list[15]}')
    field_17 = BooleanField(f'#{genres_list[16]}')
    field_18 = BooleanField(f'#{genres_list[17]}')
    field_19 = BooleanField(f'#{genres_list[18]}')
    field_20 = BooleanField(f'#{genres_list[19]}')

    submit = SubmitField('Далее→')