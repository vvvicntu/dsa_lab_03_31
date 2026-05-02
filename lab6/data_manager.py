from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Конфигурация подключения к базе данных
DB_CONFIG = {
    "host": "localhost",
    "database": "mydb",
    "user": "myuser",
    "password": "mypass"
}

def get_db_connection():
    # Используем RealDictCursor, чтобы данные из базы сразу были похожи на словарь
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

# Эндпоинт для загрузки данных о валюте
@app.route('/convert', methods=['GET'])
def convert_currency():
    # Получаем параметры из URL
    currency_name = request.args.get('currency_name')
    amount = request.args.get('amount')
    
    if not currency_name or not amount:
        return jsonify({"error": "Укажите currency_name и amount"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Проверка существования и получение курса
        cur.execute("SELECT rate FROM currencies WHERE currency_name = %s", (currency_name,))
        result = cur.fetchone()
        
        if not result:
            return jsonify({"error": f"Валюта {currency_name} не найдена в БД"}), 404
            
        rate = float(result['rate'])
        converted_value = float(amount) * rate
        
        return jsonify({
            "currency": currency_name,
            "original_amount": amount,
            "converted_result": converted_value
        }), 200
    finally:
        cur.close()
        conn.close()

# Эндпоинт для получения всех валют и их курсов
@app.route('/currencies', methods=['GET'])
def get_all_currencies():
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT currency_name, rate FROM currencies")
        rows = cur.fetchall()
        return jsonify(rows), 200
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    # Запуск на порту 5002
    app.run(host='0.0.0.0', port=5002)
