from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Метод GET принимает параметр param, умножает его на случайное число
@app.route("/number", methods=["GET"])
def get_number():
    # Получаем параметр param из запроса
    param = request.args.get("param")

    # Если param не передан, возвращаем ошибку
    if param is None:
        return jsonify({"error": "парапапарам ошибка"}), 400
    
    # Пытаемся преобразовать param в целое число
    try:
        param = int(param)
    except ValueError:
        return jsonify({"парапапарам ошибка, тут должно быть число"}), 400

    # Генерируем случайное число и умножаем его на param
    rand_num = random.randint(1, 100)
    result = rand_num * param

    # Возвращаем результат в формате JSON
    return jsonify({
        "number": result,
        "operation": "multiplication",
        "random_number": rand_num,
    })

# Метод POST принимает JSON с параметром jsonParam, выполняет случайную операцию и возвращает результат в формате JSON
@app.route("/number", methods=["POST"])
def post_number():
    # Получаем JSON из запроса
    data = request.json

    # Проверяем, что JSON содержит параметр jsonParam
    if not data or "jsonParam" not in data:
        return jsonify({"error": "ошибка jsonParam"}), 400
    
    # Пытаемся преобразовать jsonParam в целое число
    try:
        json_param = int(data["jsonParam"])
    except ValueError:
        return jsonify({"error": "ошибка jsonParam, тут должно быть число"}), 400

    # Генерируем случайное число и выбираем случайную операцию
    rand_num = random.randint(1, 100)
    operation = random.choice(["sum", "sub", "mul", "div"])

    # Выполняем выбранную операцию
    if operation == "sum":
        result = rand_num + json_param
    elif operation == "sub":
        result = rand_num - json_param
    elif operation == "mul":
        result = rand_num * json_param
    else:
        if json_param == 0:
            return jsonify({"error": "деление на ноль!"}), 400
        result = rand_num / json_param

    # Возвращаем результат в формате JSON
    return jsonify({
        "number": result,
        "operation": operation,
        "random_number": rand_num
    })

# Метод DELETE генерирует случайное число и случайную операцию
@app.route("/number", methods=["DELETE"])
def delete_number():

    # Генерируем случайное число и выбираем случайную операцию
    rand_num = random.randint(1, 100)
    operation = random.choice(["sum", "sub", "mul", "div"])

    # Возвращаем результат в формате JSON
    return jsonify({
        "number": rand_num,
        "operation": operation
    })

if __name__ == "__main__":
    app.run(debug=True)

