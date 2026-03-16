try:
    m = float(input("Введите число: "))

    for i in range(1, 11):
        result = i * m
        print(result)

except ValueError:
    print("ошибочка необходимо ввести число.")


    