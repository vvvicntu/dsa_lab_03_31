import sys
try:
    #Читаем массив из аргументов командной строки
    arr = [int(x) for x in sys.argv[1:]]

    sum_odd_index = 0

    #Суммируем элементы с нечетными индексами
    for i in range(len(arr)):
        if i % 2 != 0:
            sum_odd_index += arr[i]

    print("Сумма элементов с нечетными индексами:", sum_odd_index)

    #Удваиваем элементы, которые меньше 15
    for i in range(len(arr)):
        if arr[i] < 15:
            arr[i] *= 2

    print("Измененный массив:", arr)

except:
    print("возникла ошибка при обработке массива")

