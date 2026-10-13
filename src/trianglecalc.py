import math
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TriangleCalculator:
    """Класс для вычисления типа треугольника и его параметров"""
    
    def calculate(self, str_a, str_b, str_c):
        """
        Вычисляет вид треугольника по длинам трех сторон.
        Возвращает: (тип_треугольника, координаты_вершин, сообщение_об_ошибке)
        """
        logger.info(f"Начало вычислений: a={str_a}, b={str_b}, c={str_c}")
        
        try:
            a = float(str_a)
            b = float(str_b)
            c = float(str_c)
        except ValueError as e:
            error_msg = f"Не удалось преобразовать строки в числа: {e}"
            logger.error(error_msg)
            return "", [(-2, -2), (-2, -2), (-2, -2)], error_msg
        
        if a <= 0 or b <= 0 or c <= 0:
            error_msg = "Длины сторон должны быть положительными"
            logger.warning(error_msg)
            return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)], error_msg
        
        if (a + b <= c) or (a + c <= b) or (b + c <= a):
            error_msg = "Нарушено неравенство треугольника"
            logger.warning(error_msg)
            return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)], error_msg
        
        if math.isclose(a, b) and math.isclose(b, c):
            triangle_type = "равносторонний"
        elif math.isclose(a, b) or math.isclose(a, c) or math.isclose(b, c):
            triangle_type = "равнобедренный"
        else:
            triangle_type = "разносторонний"
        
        # Вычисление координат
        x3 = (a**2 + b**2 - c**2) / (2 * a)
        y3_squared = b**2 - x3**2
        y3 = math.sqrt(y3_squared) if y3_squared > 0 else 0.0
        
        min_x = min(0.0, a, x3)
        shift_x = -min_x if min_x < 0 else 0.0
        
        p1 = (int(round(0 + shift_x)), int(round(0)))
        p2 = (int(round(a + shift_x)), int(round(0)))
        p3 = (int(round(x3 + shift_x)), int(round(y3)))
        
        logger.info(f"Тип треугольника: {triangle_type}")
        return triangle_type, [p1, p2, p3], ""