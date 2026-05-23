from flask import Flask, render_template, request, redirect, flash, session
import psycopg2
import requests
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'super_secret_key'  

# Настройки подключения к БД
DB_CONFIG = {
    'dbname': 'finance',
    'user': 'postgres',
    'password': '',       
    'host': 'localhost',
    'port': '5432'
}

def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Регистрация
@app.route('/reg', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()

        # Проверяем, есть ли пользователь
        cur.execute("SELECT * FROM users WHERE name=%s", (name,))
        user = cur.fetchone()

        if user:
            flash('Пользователь уже существует')
            return redirect('/reg')

        # Хэшируем пароль
        password_hash = generate_password_hash(password)

        # Сохраняем
        cur.execute( """ INSERT INTO users(name,password_hash) VALUES(%s,%s)""", (name, password_hash))
        conn.commit()

        cur.close()
        conn.close()

        flash('Вы успешно зарегистрировались!')
        return redirect('/login')
    return render_template('register.html')

# Авторизация
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        name = request.form['name']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("SELECT * FROM users WHERE name=%s", (name,))
        user = cur.fetchone()

        cur.close()
        conn.close()

        # Проверяем пользователя и пароль
        if user and check_password_hash( user['password_hash'], password):

            session['user_id'] = user['id']
            session['name'] = user['name']

            flash('Вход выполнен')
            return redirect('/')

        flash('Неверный логин или пароль')
    return render_template('login.html')

# Добавление операции
@app.route('/add_operation', methods=['GET', 'POST'])
def add_operation():

    # Проверка авторизации
    if 'user_id' not in session:
        flash('Сначала войдите')
        return redirect('/login')

    if request.method == 'POST':

        date = request.form['date']
        sum_operation = request.form['sum']
        type_operation = request.form['type_operation']
        comment = request.form['comment']

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO operations
            (date,sum,user_id,type_operation,comment)
            VALUES(%s,%s,%s,%s,%s)
            """,
            (
                date,
                sum_operation,
                session['user_id'],
                type_operation,
                comment
            )
        )

        conn.commit()

        cur.close()
        conn.close()

        flash('Операция добавлена')

        return redirect('/add_operation')

    return render_template('add_operation.html')

# Просмотр операций
@app.route('/operations')
def operations():

    if 'user_id' not in session:
        flash('Сначала войдите')
        return redirect('/login')

    currency = request.args.get('currency', 'RUB')

    conn = get_db_connection()

    cur = conn.cursor(
        cursor_factory=RealDictCursor
    )

    cur.execute(
        """
        SELECT *
        FROM operations
        WHERE user_id=%s
        ORDER BY date DESC
        """,
        (session['user_id'],)
    )

    operations = cur.fetchall()

    cur.close()
    conn.close()

    # Конвертация валюты
    if currency != 'RUB':
        response = requests.get(f'http://127.0.0.1:5001/rate?currency={currency}')
        rate = response.json()['rate']

        for op in operations:
            op['sum'] = round(float(op['sum']) / rate, 2)

    return render_template(
        'operations.html',
        operations=operations,
        currency=currency
    )

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)
    