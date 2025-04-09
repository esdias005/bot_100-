
import sqlite3
import os

# Caminho para o banco de dados
DB_PATH = 'aviator_bot.db'

def init_db():
    """Inicializa o banco de dados e cria a tabela de usuários se não existir"""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
   
    # Cria a tabela de usuários
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
   
    connection.commit()
    connection.close()

def add_user(phone, password):
    """Adiciona um novo usuário ao banco de dados"""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
   
    cursor.execute(
        'INSERT INTO users (phone, password) VALUES (?, ?)',
        (phone, password)
    )
   
    connection.commit()
    connection.close()

def get_user(phone):
    """Busca um usuário pelo número de telefone"""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row  # Para acessar colunas pelo nome
    cursor = connection.cursor()
   
    cursor.execute('SELECT * FROM users WHERE phone = ?', (phone,))
    user = cursor.fetchone()
   
    connection.close()
   
    if user:
        return dict(user)  # Converte Row para dicionário
    return None
