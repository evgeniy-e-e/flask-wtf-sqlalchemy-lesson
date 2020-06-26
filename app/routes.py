from app import app, db
from flask import render_template, redirect, url_for, session
from app.models import User, Post
from app.forms import RegistrationForm, LoginForm, PostForm
from datetime import datetime
from app import login
from flask_login import login_user, logout_user, current_user


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def index():
    email = None
    if current_user.is_authenticated:
        email = current_user.email
    posts = Post.query.all()
    return render_template('index.html', email=email, posts=posts)


@app.route('/new', methods=['GET', 'POST'])
def create_post():
    email_user = session.get('email', False)
    if not email_user:
        return redirect(url_for('index'))
    form = PostForm()
    if form.validate_on_submit():
        user = User.query.filter(User.email == email_user).one()
        new_post = Post(
            text=form.text.data,
            date_created=datetime.now(),
            author_id=user.id
        )
        db.session.add(new_post)
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('create_post.html', form=form)


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = RegistrationForm()
    if form.validate_on_submit():
        register_data = {
            'name': form.name.data,
            'email': form.email.data,
            'age': form.age.data,
            'sex': form.sex.data,
            'password': form.password.data,
            'about_me': form.about_me.data,
        }
        if User.query.filter(User.email == register_data['email']).one_or_none() is not None:
            return render_template('registration.html', form=form, error="Такой пользователь уже существует!")
        new_user = User(
            email=register_data['email'],
            name=register_data['name'],
            age=register_data['age'],
            sex=register_data['sex'],
            about_me=register_data['about_me'],
        )
        new_user.set_password(register_data['password'])
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_data = {
            'email': form.email.data,
            'password': form.password.data,
            'remember_me': form.remember_me.data
        }
        user_db = User.query.filter(User.email == login_data['email']).one_or_none()
        if user_db is None or not user_db.check_password(login_data['password']):
            return render_template('login.html', title='Войти на сайт', form=form,
                                   error="Неправильный логин или пароль!")
        return redirect(url_for('index'))
    return render_template('login.html', title='Войти на сайт', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))