from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
@app.route('/')
@app.route('/index')
def index():
  username = {'username': 'TEST_USER'}
  return render_template('index.html', title='Лента', user=username)

@app.route('/user')
def user():
  username = {'username': 'TEST_USER'}
  return render_template('lk.html', user=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    flash(f'Zаход успешен логин {form.username.data} пароль {form.password.data}')
    return redirect(url_for('user'))
  return render_template('login.html', title='Zаход', form=form) 