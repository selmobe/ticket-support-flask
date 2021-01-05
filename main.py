from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user
from app import app, db
from app.models import User

import datetime

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/teste')
def teste():
    return render_template('layout_teste.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if name and email and password:
            user = User(name, email, password)
            db.session.add(user)
            user = User.query.filter_by(USER_EMAIL=email).first()

            db.session.commit()
            return redirect(url_for('login'))

    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect(url_for('home'))
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(USER_EMAIL=email).first()

        if not user or user.verify_password(password) and user.USER_STATUS == 1:
            login_user(user)

            user.USER_LAST_ACCESS = datetime.datetime.now()
            db.session.commit()

            return redirect(url_for('home'))
        if user.USER_STATUS != 1:
            error = "Usuário inativo/bloqueado"
        else:
            error = 'Usuário/senha inválidos'
        return render_template('login.html', error=error)
        

    elif request.method == "GET":
        if current_user.is_authenticated:
            return redirect(url_for('home'))

    return render_template('login.html')
    

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/users')
def users():
    user_list = User.query.all()
    return render_template('users.html', users=user_list)

@app.route('/users/edit/<int:user_id>', methods=["GET", "POST"])
def user_edit(user_id):
    user_edit = User.query.filter_by(USER_ID=user_id).first()

    if request.method == "GET":
        request.form.USER_ID = user_edit.USER_ID
        request.form.USER_NAME = user_edit.USER_NAME
        request.form.USER_EMAIL = user_edit.USER_EMAIL

        USER_ACCESS_LEVEL_LIST = {'1':'1 - Administrador', '2':'2 - Atendente', '3':"3 - Usuário"}
        USER_STATUS_LIST = {'1':'1 - Ativo', '2':'2 - Inativo', '3':'3 - Bloqueado' }

        USER_STATUS = str(user_edit.USER_STATUS)
        USER_ACCESS_LEVEL = str(user_edit.USER_ACCESS_LEVEL)

        return render_template('user_edit.html', user=user_edit, USER_STATUS_LIST=USER_STATUS_LIST, USER_STATUS=USER_STATUS, USER_ACCESS_LEVEL_LIST=USER_ACCESS_LEVEL_LIST, USER_ACCESS_LEVEL=USER_ACCESS_LEVEL)

    elif request.method == "POST" :
        if current_user.USER_ACCESS_LEVEL == 1:
            user_edit.USER_ACCESS_LEVEL = request.form['USER_ACCESS_LEVEL']
        if current_user.USER_ACCESS_LEVEL != 3:
            user_edit.USER_STATUS = request.form['USER_STATUS']

        user_edit.USER_NAME = request.form['USER_NAME']
        user_edit.USER_EMAIL = request.form['USER_EMAIL']
        
        

        db.session.add(user_edit)
        db.session.commit()
        return redirect(url_for('users'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

app.run(debug=True)