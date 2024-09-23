from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///teste.db"  # Caminho relativo para o arquivo do banco de dados SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String())
    data_nascimento = db.Column(db.String())
    email = db.Column(db.String())
    senha = db.Column(db.String())

    def __init__(self, nome, data_nascimento, email, senha):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.email = email
        self.senha = senha

