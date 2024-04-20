from app import app, db, manager
from app.models import Opinion, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def index():
    opinions = Opinion.query.order_by(Opinion.date.desc()).all()
    return render_template('index.html', opinions=opinions)


@app.route('/about')
def about():
    return render_template('about.html')


# записи


@app.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        author = current_user.id
        opinion = Opinion(title=title, intro=intro, text=text, author_id=author)

        try:
            db.session.add(opinion)
            db.session.commit()
            return redirect('/')
        except:
            return 'Возникла ошибка при добавлении публикации'
    else:
        return render_template('create.html')


@app.route('/<int:id>/')
def detail(id):
    opinion = Opinion.query.get(id)
    return render_template('detail.html', opinion=opinion)


# пользователь


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    psw = request.form.get('psw')

    if login and psw:
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.psw, psw):
            login_user(user)
            return redirect(url_for('profile'))
        else:
            flash("Логин или пароль указаны неверно")
    else:
        flash('Пожалуйста, заполните поля')
    return render_template('login.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    login = request.form.get('login')
    psw = request.form.get('psw')
    psw2 = request.form.get('psw2')

    if request.method == 'POST':
        if not (login or psw or psw2):
            flash('Пожалуйста, заполните поля')
        elif psw != psw2:
            flash('Пароли не совпадают')
        else:
            hash_psw = generate_password_hash(psw)
            new_user = User(login=login, psw=hash_psw)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login_page'))

    return render_template('registration.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@manager.unauthorized_handler
def unauthorized():
    flash('Вы не вошли в систему.')
    return redirect(url_for('login_page'))
