try:
    a = int(input("Введите первое число: "))
    b = int(input("Введите второе число: "))
    c = int(input("Введите третье число: "))

    print("Числа, которые попадают в интервал:")

    if 1 <= a <= 50:
        print(a)
    if 1 <= b <= 50:
        print(b)
    if 1 <= c <= 50:
        print(c)

except ValueError:
    print("ошибочка, необходимо вводить целые числа.")

