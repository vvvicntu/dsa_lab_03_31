import requests
import random

URL = "http://127.0.0.1:5000/number"

# GET
param = random.randint(1, 10)
get_result = requests.get(URL, params={"param": param}).json()
print("GET-запрос:", get_result)

# POST
json_param = random.randint(1, 10)
post_result = requests.post(URL, json={"jsonParam": json_param}).json()
print("POST-запрос:", post_result)

# DELETE
delete_result = requests.delete(URL).json()
print("DELETE-запрос:", delete_result)

# Функция для выполнения операции 
def calc(a, b, op):
    if op == "sum":
        return a + b
    if op == "sub":
        return a - b
    if op == "mul":
        return a * b
    if op == "div":
        return a / b

# Итоговый результат всех трех запросов
result = get_result["number"]
result = calc(result, post_result["number"], post_result["operation"])
result = calc(result, delete_result["number"], delete_result["operation"])

print("Result:", int(result))