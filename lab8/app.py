import os
import json
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Настройка для ограничения запросов по IP-адресу клиента
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day"], # Общий лимит 100 запросов в сутки
    storage_uri="memory://"
)

DATA_FILE = "data.json"
data = {}

def load_data():
    # Загрузка данных из файла при старте приложения
    global data
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = {}
    else:
        data = {}

def save_data():
    # Сохранение изменений в файл после каждой операции
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

load_data()

@app.route('/set', methods=['POST'])
@limiter.limit("10 per minute") # Отдельный лимит для /set
def set_value():
    req_data = request.get_json()
    if not req_data or 'key' not in req_data or 'value' not in req_data:
        return jsonify({"error": "Необходимо передать 'key' и 'value'"}), 400
    
    key = str(req_data['key'])
    value = req_data['value']
    
    data[key] = value
    save_data()
    return jsonify({"status": "success", "message": f"Ключ '{key}' успешно сохранен"}), 200

@app.route('/get/<key>', methods=['GET'])
def get_value(key):
    # Получить значение по ключу
    if key in data:
        return jsonify({"key": key, "value": data[key]}), 200
    return jsonify({"error": f"Ключ '{key}' не найден"}), 404

@app.route('/delete/<key>', methods=['DELETE'])
@limiter.limit("10 per minute") # Отдельный лимит для /delete
def delete_value(key):
    # Удалить ключ
    if key in data:
        del data[key]
        save_data()
        return jsonify({"status": "success", "message": f"Ключ '{key}' успешно удален"}), 200
    return jsonify({"error": f"Ключ '{key}' не найден"}), 404

@app.route('/exists/<key>', methods=['GET'])
def exists_key(key):
    # Проверить наличие ключа
    exists = key in data
    return jsonify({"key": key, "exists": exists}), 200

# Обработчик ошибки превышения лимита запросов 
@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        "error": "Превышен лимит запросов",
        "message": str(e.description)
    }), 429

if __name__ == '__main__':
    app.run(debug=True, port=5000)
