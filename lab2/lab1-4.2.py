count = 0

try:
    num = int(input("Введите число (0 для завершения): "))

    while num != 0:
        count += 1
        num = int(input("Введите число (0 для завершения): "))

    print("Количество чисел:", count)

except ValueError:
    print("ошибочка, необходимо вводить целые числа.")

