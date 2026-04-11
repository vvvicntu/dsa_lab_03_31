import pytest
from triangle_class import Triangle, IncorrectTriangleSides 

# Позитивные тесты

def test_creation_and_perimeter():
    # Проверка создания объекта и расчета периметра
    t = Triangle(3, 4, 5)
    assert t.perimeter() == 12

def test_equilateral_type():
    # Проверка равностороннего треугольника
    t = Triangle(5, 5, 5)
    assert t.triangle_type() == "equilateral"

def test_isosceles_type():
    # Проверка равнобедренного треугольника
    t = Triangle(5, 5, 3)
    assert t.triangle_type() == "isosceles"

def test_nonequilateral_type():
    # Проверка разностороннего треугольника
    t = Triangle(3, 4, 5)
    assert t.triangle_type() == "nonequilateral"


# Негативные тесты

def test_zero_sides():
    # Ошибка при создании треугольника с нулевой стороной
    with pytest.raises(IncorrectTriangleSides):
        Triangle(0, 5, 5)

def test_negative_sides():
    # Ошибка при создании треугольника с отрицательной стороной
    with pytest.raises(IncorrectTriangleSides):
        Triangle(-1, 2, 2)

def test_invalid_triangle_rule():
    # Ошибка, если нарушено неравенство треугольника (1+1 < 10)
    with pytest.raises(IncorrectTriangleSides):
        Triangle(1, 1, 10)
