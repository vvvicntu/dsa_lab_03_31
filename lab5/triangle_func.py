class IncorrectTriangleSides(Exception):
    pass

def get_triangle_type(a, b, c):
    # Стороны должны быть положительными
    if a <= 0 or b <= 0 or c <= 0:
        raise IncorrectTriangleSides()

    # Проверка существования треугольника
    if a + b <= c or a + c <= b or b + c <= a:
        raise IncorrectTriangleSides()

    # Определение типа треугольника
    if a == b == c:
        return "equilateral"
    elif a == b or a == c or b == c:
        return "isosceles"
    else:
        return "nonequilateral"
    
if __name__ == "__main__":
    try:
        print(get_triangle_type(2, 2, 2))
    except IncorrectTriangleSides:
        print("Ошибка")