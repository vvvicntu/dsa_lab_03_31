class IncorrectTriangleSides(Exception):
    pass

# Принимает три стороны и проверяет их на корректность
class Triangle:
    def __init__(self, a, b, c):
        # Проверка на положительные числа
        if a <= 0 or b <= 0 or c <= 0:
            raise IncorrectTriangleSides("Стороны должны быть больше нуля")
        
        # Проверка неравенства треугольника
        if a + b <= c or a + c <= b or b + c <= a:
            raise IncorrectTriangleSides("Сумма двух сторон должна быть больше третьей")
            
        self.a = a
        self.b = b
        self.c = c

    # Возвращает тип треугольника в виде строки
    def triangle_type(self):
        if self.a == self.b == self.c:
            return "equilateral"
        elif self.a == self.b or self.a == self.c or self.b == self.c:
            return "isosceles"
        else:
            return "nonequilateral"
        
    # Вычисляет периметр треугольника
    def perimeter(self):
        return self.a + self.b + self.c

if __name__ == "__main__":
    try:
        tr = Triangle(3, 4, 5)
        print(f"Тип: {tr.triangle_type()}, Периметр: {tr.perimeter()}")
    except IncorrectTriangleSides as e:
        print(f"Ошибка: {e}")
