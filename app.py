from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, Usuario
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave-secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meubanco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Cria as tabelas quando o app iniciar
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        user = Usuario.query.filter_by(email=email).first()
        if user and check_password_hash(user.senha, senha):
            session['usuario_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            flash('Login inválido')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        if Usuario.query.filter_by(email=email).first():
            flash('Usuário já existe!')
        else:
            novo = Usuario(
                email=email,
                senha=generate_password_hash(senha),
                tipoUsuario=False,
                mudaSenha=False,
                liberacao=True
            )
            db.session.add(novo)
            db.session.commit()
            flash('Usuário cadastrado com sucesso!')
            return redirect(url_for('login'))
    return render_template('register.html')
@app.route('/logout')
def logout():
    session.pop('usuario_id', None)  # remove a sessão do usuário
    return redirect(url_for('login'))  # redireciona para a página de login


@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
