
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from database import init_db, add_user, get_user
from predict import generate_prediction
import os
import time
import random

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Chave secreta para sessões

# Inicializa o banco de dados
init_db()

@app.route('/')
def index():
    if 'user_phone' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
       
        # Validação dos dados de entrada
        if len(phone) != 9 or not phone.isdigit():
            flash('O número de telefone deve ter exatamente 9 dígitos')
            return render_template('register.html')
       
        if len(password) != 8:
            flash('A senha deve ter exatamente 8 caracteres')
            return render_template('register.html')
           
        if password != confirm_password:
            flash('As senhas não coincidem')
            return render_template('register.html')
       
        # Verifica se o usuário já existe
        existing_user = get_user(phone)
        if existing_user:
            flash('Este número de telefone já está cadastrado')
            return render_template('register.html')
           
        # Adiciona o usuário ao banco de dados
        add_user(phone, password)
       
        session['user_phone'] = phone
        flash('Cadastro realizado com sucesso!')
        return redirect(url_for('security'))
       
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form.get('phone')
        password = request.form.get('password')
       
        user = get_user(phone)
        if user and user['password'] == password:
            session['user_phone'] = phone
            return redirect(url_for('security'))
        else:
            flash('Credenciais inválidas')
           
    return render_template('login.html')

@app.route('/security', methods=['GET', 'POST'])
def security():
    if 'user_phone' not in session:
        return redirect(url_for('login'))
       
    if request.method == 'POST':
        code = request.form.get('security_code')
       
        # Código fixo de verificação
        if code == '943750':
            session['verified'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Código de verificação inválido')
           
    return render_template('security.html')

@app.route('/dashboard')
def dashboard():
    if 'user_phone' not in session or 'verified' not in session:
        return redirect(url_for('login'))
       
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/api/predict', methods=['POST'])
def predict():
    if 'user_phone' not in session or 'verified' not in session:
        return jsonify({'error': 'Não autorizado'}), 401
       
    betting_site_url = request.form.get('betting_site_url')
   
    # Verifica se o URL foi fornecido
    if not betting_site_url:
        return jsonify({'error': 'URL da casa de apostas não fornecido'}), 400
       
    # Gera a previsão
    prediction, wait_time = generate_prediction()
   
    return jsonify({
        'prediction': prediction,
        'wait_time': wait_time
    })

@app.route('/api/history')
def history():
    if 'user_phone' not in session or 'verified' not in session:
        return jsonify({'error': 'Não autorizado'}), 401
   
    # Simula o histórico das últimas 5 previsões
    history_list = []
    for _ in range(5):
        prediction, _ = generate_prediction()
        history_list.append(prediction)
   
    return jsonify({'history': history_list})

if __name__ == '__main__':
    app.run(debug="true")
