from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    tipoUsuario = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)  # Aumentado para armazenar hash
    mudaSenha = db.Column(db.Boolean, default=False)
    liberacao = db.Column(db.Boolean, default=True)

class Perfil(db.Model):
    __tablename__ = 'perfil'
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    nome = db.Column(db.String(50))
    contato = db.Column(db.String(11))
    foto = db.Column(db.String(200))

class Oculos(db.Model):
    __tablename__ = 'oculos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(200))

class Cupom(db.Model):
    __tablename__ = 'cupons'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), nullable=False, unique=True)
    desconto = db.Column(db.Float, nullable=False)