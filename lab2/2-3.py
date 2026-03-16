try:
    str = input("введите строку")

    count_dots = 0 
    new_str = ""

    for i in str:
        if i == ".":
            count_dots += 1
        else:
            new_str += i

    print("строка без точек:", new_str)
    print("кол-во удаленных символов", new_str)

except Exception as e:
    print("ошибка",)