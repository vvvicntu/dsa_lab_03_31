from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Адреса микросервисов
CM_URL = "http://localhost:5001"
DM_URL = "http://localhost:5002"

# Веб-интерфейс на Jinja2
@app.route('/')
def index():
    # Gateway запрашивает данные у data-manager
    response = requests.get(f"{DM_URL}/currencies")
    currencies = response.json() if response.status_code == 200 else []
    return render_template('index.html', currencies=currencies)

# Дополнительный роут для формы конвертации
@app.route('/convert_web')
def convert_web():
    c_name = request.args.get('currency_name')
    amount = request.args.get('amount')
    # Проксируем запрос на data-manager
    resp = requests.get(f"{DM_URL}/convert", params={"currency_name": c_name, "amount": amount})
    data = resp.json()
    result = data.get('converted_result', 'Ошибка')
    
    # Снова получаем список для отображения таблицы
    currencies = requests.get(f"{DM_URL}/currencies").json()
    return render_template('index.html', currencies=currencies, result=result)

# Универсальный "Прокси" для API 
@app.route('/api/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    # Если путь для управления (load/delete/update) шлем на 5001
    if path in ['load', 'update_currency', 'delete']:
        url = f"{CM_URL}/{path}"
        resp = requests.post(url, json=request.json)
    # Если для получения данных на 5002
    else:
        url = f"{DM_URL}/{path}"
        resp = requests.get(url, params=request.args)
        
    return jsonify(resp.json()), resp.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
