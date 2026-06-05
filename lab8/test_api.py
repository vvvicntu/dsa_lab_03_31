import requests

BASE_URL = "http://127.0.0.1:5000"

print("Тестирование POST /set")
set_res = requests.post(f"{BASE_URL}/set", json={"key": "user_1", "value": {"name": "Вика", "role": "admin"}})
print("Добавление user_1:", set_res.json())

print("\nТестирование GET /get/<key>")
get_res = requests.get(f"{BASE_URL}/get/user_1")
print("Получение user_1:", get_res.json())

print("\nТестирование GET /exists/<key>")
exists_res1 = requests.get(f"{BASE_URL}/exists/user_1")
exists_res2 = requests.get(f"{BASE_URL}/exists/user_2")
print("Существует user_1?:", exists_res1.json())
print("Существует user_2?:", exists_res2.json())

print("\nТестирование DELETE /delete/<key>")
del_res = requests.delete(f"{BASE_URL}/delete/user_1")
print("Удаление user_1:", del_res.json())

print("\nТестирование лимитов (10 запросов в минуту для /set)")
print("Отправка 12 быстрых запросов подряд")
for i in range(12):
    res = requests.post(f"{BASE_URL}/set", json={"key": f"test_{i}", "value": "val"})
    if res.status_code == 429:
        print(f"Запрос {i+1}: Заблокировано! Ответ:", res.json())
    else:
        print(f"Запрос {i+1}: Успешно")