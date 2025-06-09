# Importações necessárias
import os
from flask import Flask, render_template, redirect, url_for, request, session, flash
from models import db, Usuario, Oculos, Cupom
from werkzeug.security import generate_password_hash, check_password_hash

# Cria a aplicação Flask
app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_ultra_segura_123'

# Configuração do banco de dados
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'meubanco.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Função para criar dados de teste
def criar_dados_teste():
    with app.app_context():
        db.create_all()
        
        # Cria usuário admin se não existir
        if not Usuario.query.first():
            admin = Usuario(
                email="admin@example.com",
                senha=generate_password_hash("admin123"),
                tipoUsuario=True
            )
            db.session.add(admin)
            db.session.commit()
        
        if not Oculos.query.first():
            modelos = [
                ("Ray-Ban Aviador", 599.90, "Clássico, lente espelhada"),
                ("Oakley Holbrook", 450.00, "Esportivo, anti-impacto"),
                ("Prada PR 17WV", 1200.00, "Acetato, luxo italiano"),
                ("Havainas Polarized", 199.90, "Estilo praia, lente polarizada")
            ]
            for nome, preco, desc in modelos:
                db.session.add(Oculos(nome=nome, preco=preco, descricao=desc))
            
            db.session.commit()

# Rotas de autenticação
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and check_password_hash(usuario.senha, senha):
            session['user_id'] = usuario.id
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        flash('Email ou senha incorretos!', 'danger')
    return render_template('login.html')
@app.route('/finalizar-compra')
def finalizar_compra():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if not session.get('carrinho'):
        flash('Seu carrinho está vazio!', 'warning')
        return redirect(url_for('dashboard'))
    
    # Aqui você implementaria a lógica de pagamento
    session['carrinho'] = []
    flash('Compra finalizada com sucesso!', 'success')
    return redirect(url_for('dashboard'))

@app.context_processor
def utility_processor():
    def carrinho_total():
        if 'carrinho' in session:
            return sum(item['preco'] for item in session['carrinho'])
        return 0
    return dict(carrinho_total=carrinho_total)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            hashed_password = generate_password_hash(request.form['senha'])
            novo_usuario = Usuario(
                email=request.form['email'],
                senha=hashed_password,
                tipoUsuario=False
            )
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Registro realizado com sucesso! Faça login.', 'success')
            return redirect(url_for('login'))
        except:
            flash('Erro ao registrar. Email já existe.', 'danger')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Você foi deslogado.', 'info')
    return redirect(url_for('login'))

# Rotas principais
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if 'carrinho' not in session:
        session['carrinho'] = []
    
    return render_template('dashboard.html', 
                         oculos=Oculos.query.all(),
                         carrinho=session['carrinho'])

@app.route('/add_carrinho/<int:oculos_id>')
def add_carrinho(oculos_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    item = Oculos.query.get_or_404(oculos_id)
    session['carrinho'].append({
        'id': item.id,
        'nome': item.nome,
        'preco': item.preco
    })
    session.modified = True
    flash(f"{item.nome} adicionado ao carrinho!", 'success')
    return redirect(url_for('dashboard'))

@app.route('/remover_item/<int:index>')
def remover_item(index):
    try:
        item = session['carrinho'].pop(index)
        session.modified = True
        flash(f"{item['nome']} removido!", 'info')
    except IndexError:
        flash("Item não encontrado no carrinho", 'error')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    criar_dados_teste()
    app.run(debug=True)