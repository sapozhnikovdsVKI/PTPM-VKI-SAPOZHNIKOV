import unittest
from src.converter import Converter


class TestConverter(unittest.TestCase):
    """Тесты для класса Converter"""
    
    # ========== Диапазон [100.7; +∞) -> 1000 ==========
    
    def test_x_equals_100_7_returns_1000(self):
        """Граничное значение: x = 100.7 должно вернуть 1000"""
        self.assertEqual(Converter.do(100.7), 1000)
    
    def test_x_greater_than_100_7_returns_1000(self):
        """x > 100.7 должно вернуть 1000"""
        self.assertEqual(Converter.do(150.5), 1000)
    
    def test_x_very_large_returns_1000(self):
        """Очень большое x должно вернуть 1000"""
        self.assertEqual(Converter.do(9999.9), 1000)
    
    def test_x_100_8_returns_1000(self):
        """x = 100.8 должно вернуть 1000"""
        self.assertEqual(Converter.do(100.8), 1000)
    
    # ========== Диапазон (0; 100.7) -> int(x) ==========
    
    def test_x_positive_small_returns_int(self):
        """Малое положительное x: отбрасывание дробной части"""
        self.assertEqual(Converter.do(5.3), 5)
    
    def test_x_positive_medium_returns_int(self):
        """Среднее положительное x"""
        self.assertEqual(Converter.do(50.7), 50)
    
    def test_x_close_to_100_7_from_below(self):
        """x близко к 100.7 снизу: 100.6 -> 100"""
        self.assertEqual(Converter.do(100.6), 100)
    
    def test_x_0_1_returns_0(self):
        """x = 0.1 -> int(0.1) = 0"""
        self.assertEqual(Converter.do(0.1), 0)
    
    def test_x_99_9_returns_99(self):
        """x = 99.9 -> 99"""
        self.assertEqual(Converter.do(99.9), 99)
    
    def test_x_1_0_returns_1(self):
        """x = 1.0 -> 1"""
        self.assertEqual(Converter.do(1.0), 1)
    
    # ========== x == 0.0 -> ValueError ==========
    
    def test_x_zero_raises_value_error(self):
        """x = 0.0 должно вызвать ValueError"""
        with self.assertRaises(ValueError):
            Converter.do(0.0)
    
    def test_x_zero_error_message(self):
        """Проверка сообщения об ошибке при x = 0.0"""
        with self.assertRaises(ValueError) as context:
            Converter.do(0.0)
        self.assertIn("0.0", str(context.exception))
    
    # ========== Диапазон [-30.4; 0) -> int(x) - 5 ==========
    
    def test_x_negative_small_returns_int_minus_5(self):
        """x = -5.3 -> int(-5.3) - 5 = -5 - 5 = -10"""
        self.assertEqual(Converter.do(-5.3), -10)
    
    def test_x_negative_medium_returns_int_minus_5(self):
        """x = -20.7 -> int(-20.7) - 5 = -20 - 5 = -25"""
        self.assertEqual(Converter.do(-20.7), -25)
    
    def test_x_boundary_minus_30_4(self):
        """Граничное значение: x = -30.4 -> int(-30.4) - 5 = -30 - 5 = -35"""
        self.assertEqual(Converter.do(-30.4), -35)
    
    def test_x_close_to_zero_negative(self):
        """x = -0.1 -> int(-0.1) - 5 = 0 - 5 = -5"""
        self.assertEqual(Converter.do(-0.1), -5)
    
    def test_x_minus_15_5(self):
        """x = -15.5 -> int(-15.5) - 5 = -15 - 5 = -20"""
        self.assertEqual(Converter.do(-15.5), -20)
    
    def test_x_minus_1_0(self):
        """x = -1.0 -> int(-1.0) - 5 = -1 - 5 = -6"""
        self.assertEqual(Converter.do(-1.0), -6)
    
    # ========== Диапазон (-∞; -30.5] -> -2000 ==========
    
    def test_x_equals_minus_30_5_returns_minus_2000(self):
        """Граничное значение: x = -30.5 должно вернуть -2000"""
        self.assertEqual(Converter.do(-30.5), -2000)
    
    def test_x_less_than_minus_30_5(self):
        """x < -30.5 должно вернуть -2000"""
        self.assertEqual(Converter.do(-50.3), -2000)
    
    def test_x_very_negative_returns_minus_2000(self):
        """Очень отрицательное x должно вернуть -2000"""
        self.assertEqual(Converter.do(-9999.9), -2000)
    
    def test_x_minus_31_0_returns_minus_2000(self):
        """x = -31.0 должно вернуть -2000"""
        self.assertEqual(Converter.do(-31.0), -2000)
    
    def test_x_minus_100_0_returns_minus_2000(self):
        """x = -100.0 должно вернуть -2000"""
        self.assertEqual(Converter.do(-100.0), -2000)
    
    # ========== Дополнительные граничные тесты ==========
    
    def test_x_just_below_100_7(self):
        """x = 100.6 (чуть ниже границы) -> 100"""
        self.assertEqual(Converter.do(100.6), 100)
    
    def test_x_just_above_0(self):
        """x = 0.1 (чуть выше 0) -> 0"""
        self.assertEqual(Converter.do(0.1), 0)
    
    def test_x_just_below_0(self):
        """x = -0.1 (чуть ниже 0) -> -5"""
        self.assertEqual(Converter.do(-0.1), -5)


if __name__ == '__main__':
    unittest.main(verbosity=2)