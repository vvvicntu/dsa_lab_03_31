try:
    a = float(input("Введите первое число: "))
    b = float(input("Введите второе число: "))
    c = float(input("Введите третье число: "))

    minimum = min(a, b, c)

    print("Минимальное число:", minimum)

except ValueError:
    print("ошибочка ввода, пж введите число")

