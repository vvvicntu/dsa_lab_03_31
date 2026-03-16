try:
    str = input("Введите строку: ")

    count_dots = 0
    new_str = ""

    for i in str:
        #если символ точка, то увеличиваем счетчик на единицу
        if i == ".":
            count_dots += 1
        #если символ не точка то добавляем его в новую строку
        else:
            new_str += i

    print("строка без точек:", new_str)
    print("количество удаленных символов:", count_dots)

except Exception as e:
    print("произошла ошибка", e)

