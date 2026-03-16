sum = 0

try:
    num = int(input("Введите число (0 для завершения): "))

    while num != 0:
        sum += num
        num = int(input("Введите число (0 для завершения): "))

    print("Сумма чисел:", sum)

except ValueError:
    print("ошибочка необходимо вводить целые числа.")

