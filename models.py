from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    tipoUsuario = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(30), nullable=False)
    mudaSenha = db.Column(db.Boolean, default=False)
    liberacao = db.Column(db.Boolean, default=False)
