import unittest
import math
from src.my_project import get_triangle_info

class TestTriangleInfo(unittest.TestCase):
    """Тесты для функции get_triangle_info"""
    
    # ===== Тесты для равносторонних треугольников =====
    def test_equilateral_triangle_small(self):
        """Равносторонний треугольник с маленькими сторонами"""
        triangle_type, coords = get_triangle_info("5", "5", "5")
        self.assertEqual(triangle_type, "равносторонний")
        self.assertEqual(len(coords), 3)
    
    def test_equilateral_triangle_large(self):
        """Равносторонний треугольник с большими сторонами"""
        triangle_type, coords = get_triangle_info("100", "100", "100")
        self.assertEqual(triangle_type, "равносторонний")
    
    def test_equilateral_triangle_float(self):
        """Равносторонний треугольник с дробными сторонами"""
        triangle_type, coords = get_triangle_info("3.5", "3.5", "3.5")
        self.assertEqual(triangle_type, "равносторонний")
    
    # ===== Тесты для равнобедренных треугольников =====
    def test_isosceles_triangle_a_equals_b(self):
        """Равнобедренный треугольник: a = b"""
        triangle_type, coords = get_triangle_info("40", "40", "70")
        self.assertEqual(triangle_type, "равнобедренный")
    
    def test_isosceles_triangle_a_equals_c(self):
        """Равнобедренный треугольник: a = c"""
        triangle_type, coords = get_triangle_info("50", "60", "50")
        self.assertEqual(triangle_type, "равнобедренный")
    
    def test_isosceles_triangle_b_equals_c(self):
        """Равнобедренный треугольник: b = c"""
        triangle_type, coords = get_triangle_info("60", "50", "50")
        self.assertEqual(triangle_type, "равнобедренный")
    
    def test_isosceles_triangle_float_sides(self):
        """Равнобедренный треугольник с дробными сторонами"""
        triangle_type, coords = get_triangle_info("10.5", "10.5", "15")
        self.assertEqual(triangle_type, "равнобедренный")
    
    # ===== Тесты для разносторонних треугольников =====
    def test_scalene_triangle_classic(self):
        """Разносторонний треугольник (классический 3-4-5)"""
        triangle_type, coords = get_triangle_info("3", "4", "5")
        self.assertEqual(triangle_type, "разносторонний")
    
    def test_scalene_triangle_large(self):
        """Разносторонний треугольник с большими сторонами"""
        triangle_type, coords = get_triangle_info("10", "15", "20")
        self.assertEqual(triangle_type, "разносторонний")
    
    def test_scalene_triangle_float(self):
        """Разносторонний треугольник с дробными сторонами"""
        triangle_type, coords = get_triangle_info("3.1", "4.2", "5.3")
        self.assertEqual(triangle_type, "разносторонний")
    
    # ===== Тесты для невалидных данных (отрицательные числа) =====
    def test_negative_side_a(self):
        """Отрицательная сторона a"""
        triangle_type, coords = get_triangle_info("-5", "10", "10")
        self.assertEqual(triangle_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])
    
    def test_negative_side_b(self):
        """Отрицательная сторона b"""
        triangle_type, coords = get_triangle_info("10", "-5", "10")
        self.assertEqual(triangle_type, "не треугольник")
    
    def test_negative_side_c(self):
        """Отрицательная сторона c"""
        triangle_type, coords = get_triangle_info("10", "10", "-5")
        self.assertEqual(triangle_type, "не треугольник")
    
    def test_all_negative_sides(self):
        """Все стороны отрицательные"""
        triangle_type, coords = get_triangle_info("-3", "-4", "-5")
        self.assertEqual(triangle_type, "не треугольник")
    
    # ===== Тесты для нуля =====
    def test_zero_side_a(self):
        """Сторона a равна нулю"""
        triangle_type, coords = get_triangle_info("0", "5", "5")
        self.assertEqual(triangle_type, "не треугольник")
    
    def test_zero_side_b(self):
        """Сторона b равна нулю"""
        triangle_type, coords = get_triangle_info("5", "0", "5")
        self.assertEqual(triangle_type, "не треугольник")
    
    def test_zero_side_c(self):
        """Сторона c равна нулю"""
        triangle_type, coords = get_triangle_info("5", "5", "0")
        self.assertEqual(triangle_type, "не треугольник")
    
    # ===== Тесты для невалидных строк =====
    def test_invalid_string_a(self):
        """Невалидная строка для стороны a"""
        triangle_type, coords = get_triangle_info("abc", "10", "10")
        self.assertEqual(triangle_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])
    
    def test_invalid_string_b(self):
        """Невалидная строка для стороны b"""
        triangle_type, coords = get_triangle_info("10", "xyz", "10")
        self.assertEqual(triangle_type, "")
    
    def test_invalid_string_c(self):
        """Невалидная строка для стороны c"""
        triangle_type, coords = get_triangle_info("10", "10", "invalid")
        self.assertEqual(triangle_type, "")
    
    def test_empty_string(self):
        """Пустая строка"""
        triangle_type, coords = get_triangle_info("", "5", "5")
        self.assertEqual(triangle_type, "")
    
    def test_special_characters(self):
        """Специальные символы"""
        triangle_type, coords = get_triangle_info("5!", "@5", "5#")
        self.assertEqual(triangle_type, "")
    
    # ===== Тесты для нарушения неравенства треугольника =====
    def test_triangle_inequality_violation_1(self):
        """Нарушение неравенства треугольника: a + b <= c"""
        triangle_type, coords = get_triangle_info("1", "2", "10")
        self.assertEqual(triangle_type, "не треугольник")
    
    def test_triangle_inequality_violation_2(self):
        """Нарушение неравенства треугольника: a + c <= b"""
        triangle_type, coords = get_triangle_info("1", "10", "2")
        self.assertEqual(triangle_type, "не треугольник")
    
    def test_triangle_inequality_violation_3(self):
        """Нарушение неравенства треугольника: b + c <= a"""
        triangle_type, coords = get_triangle_info("10", "1", "2")
        self.assertEqual(triangle_type, "не треугольник")
    
    def test_triangle_inequality_equal(self):
        """Сумма двух сторон равна третьей"""
        triangle_type, coords = get_triangle_info("5", "5", "10")
        self.assertEqual(triangle_type, "не треугольник")
    
    # ===== Тесты для координат =====
    def test_coordinates_not_negative_one_for_valid(self):
        """Координаты не должны быть (-1, -1) для валидного треугольника"""
        triangle_type, coords = get_triangle_info("3", "4", "5")
        self.assertNotEqual(coords[0], (-1, -1))
        self.assertNotEqual(coords[1], (-1, -1))
        self.assertNotEqual(coords[2], (-1, -1))
    
    def test_coordinates_structure(self):
        """Координаты должны быть кортежем из трех пар"""
        triangle_type, coords = get_triangle_info("5", "6", "7")
        self.assertEqual(len(coords), 3)
        for coord in coords:
            self.assertIsInstance(coord, tuple)
            self.assertEqual(len(coord), 2)
    
    # ===== Граничные случаи =====
    def test_very_small_positive(self):
        """Очень маленькие положительные числа"""
        triangle_type, coords = get_triangle_info("0.001", "0.001", "0.001")
        self.assertEqual(triangle_type, "равносторонний")
    
    def test_very_large_numbers(self):
        """Очень большие числа"""
        triangle_type, coords = get_triangle_info("1000000", "1000000", "1000000")
        self.assertEqual(triangle_type, "равносторонний")
    
    def test_string_with_spaces(self):
        """Строка с пробелами"""
        triangle_type, coords = get_triangle_info(" 5 ", " 5 ", " 5 ")
        # Должно обработаться корректно или вернуть ошибку
        self.assertIn(triangle_type, ["равносторонний", ""])
    
    def test_mixed_valid_invalid(self):
        """Смешанные валидные и невалидные данные"""
        triangle_type, coords = get_triangle_info("5", "invalid", "5")
        self.assertEqual(triangle_type, "")


if __name__ == '__main__':
    unittest.main(verbosity=2)