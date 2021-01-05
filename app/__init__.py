from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder=".\\templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///.././app/base_de_dados.db'
app.config['SECRET_KEY'] = 'masterkey'

login_manager = LoginManager(app)
db = SQLAlchemy(app)    