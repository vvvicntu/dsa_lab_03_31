import unittest
# Импортируем функцию и исключение из первого файла
from triangle_func import get_triangle_type, IncorrectTriangleSides

class TestTriangleFunc(unittest.TestCase):

    # Позитивные тесты
    def test_equilateral(self):
        # Проверка равностороннего треугольника
        self.assertEqual(get_triangle_type(3, 3, 3), "equilateral")

    def test_isosceles(self):
        # Проверка равнобедренного треугольника
        self.assertEqual(get_triangle_type(3, 3, 4), "isosceles")

    def test_nonequilateral(self):
        # Проверка разностороннего треугольника
        self.assertEqual(get_triangle_type(3, 4, 5), "nonequilateral")

    # Негативные тесты 
    def test_zero_side(self):
        # Ошибка при нулевой стороне
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(0, 2, 3)

    def test_invalid_triangle(self):
        # Ошибка, если сумма двух сторон меньше третьей
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(0, 1, 1)

    def test_negative_side(self):
        # Ошибка, при отрицательной стороне
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(-1, 2, 2)

if __name__ == "__main__":
    unittest.main()
