from flask import Flask, request, flash, url_for, redirect, render_template
from models import db, migrate, usuario
from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teste.db'  # caminho para o arquivo do banco de dados SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "random string"
db.init_app(app)
migrate.init_app(app, db)

@app.route('/')
def menu():
    return render_template('menu.html')

# usuario
@app.route('/new', methods=['GET', 'POST'])
def usuario_new():
    if request.method == 'POST':
        nome = request.form['nome'] 
        data_nascimento = request.form['data_nascimento'] 
        email = request.form['email'] 
        senha = request.form['senha']
        if not nome or not data_nascimento or not email or not senha:
            flash('Por favor cadastre tudo', 'error')
        else:
            usuario_teste = usuario.query.filter_by(email=email).first()

            if usuario_teste:
                # caso o email já exista, exibe mensagem de erro
                flash('Já existe um cadastro com este e-mail', 'error')
            usuarios = usuario(nome, data_nascimento, email, senha)
            db.session.add(usuarios)
            db.session.commit()
            flash('Adicionado corretamente')
            return redirect(url_for('usuario_home', id=usuarios.id))
    return render_template('usuario_new.html')

@app.route('/login', methods=['GET', 'POST'])
def usuario_login():
    if request.method == 'POST':
        email = request.form['email'] 
        senha = request.form['senha']

        usuarios = usuario.query.filter_by(email=email, senha=senha).first()
        if usuarios:
            return redirect(url_for('usuario_home', id=usuarios.id))
        else:
            flash('E-mail ou senha incorretos', 'error')
    return render_template('usuario_login.html')

@app.route('/home/<id>')
def usuario_home(id):
    usuarios = usuario.query.filter_by(id=id).first()

    if not usuarios:
        flash('Usuário não encontrado!', 'error')
        return redirect(url_for('usuario_login'))

    return render_template('usuario_home.html', usuarios=usuarios)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # cria as tabelas do banco de dados, se ainda não existirem
    app.run(debug=True)
