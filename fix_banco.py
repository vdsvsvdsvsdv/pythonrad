# -*- coding: utf-8 -*-
from app import app, db
import os

if not os.path.exists('instance'):
    os.makedirs('instance')

with app.app_context():
    db.create_all()
    print("✅ Banco criado com sucesso em:")
    print(os.path.abspath('instance/meubanco.db'))