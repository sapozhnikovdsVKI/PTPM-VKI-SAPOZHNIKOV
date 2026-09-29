import math
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def get_triangle_info(str_a, str_b, str_c):
    """
    Вычисляет вид треугольника и координаты его вершин по длинам трех сторон.
    """
    logger.info(f"Начало обработки. Входные данные: a={str_a}, b={str_b}, c={str_c}")

    try:
        a = float(str_a)
        b = float(str_b)
        c = float(str_c)
    except ValueError as e:
        logger.error(f"Не удалось преобразовать строки в числа. Ошибка: {e}")
        return "", [(-2, -2), (-2, -2), (-2, -2)]

    if a <= 0 or b <= 0 or c <= 0:
        logger.warning(f"Длины сторон должны быть строго положительными. Получено: a={a}, b={b}, c={c}")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    if (a + b <= c) or (a + c <= b) or (b + c <= a):
        logger.warning(f"Нарушено неравенство треугольника для сторон: a={a}, b={b}, c={c}")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    if math.isclose(a, b) and math.isclose(b, c):
        triangle_type = "равносторонний"
    elif math.isclose(a, b) or math.isclose(a, c) or math.isclose(b, c):
        triangle_type = "равнобедренный"
    else:
        triangle_type = "разносторонний"
        
    logger.info(f"Тип треугольника успешно определен: {triangle_type}")

    x3 = (a**2 + b**2 - c**2) / (2 * a)

    y3_squared = b**2 - x3**2
    y3 = math.sqrt(y3_squared) if y3_squared > 0 else 0.0

    min_x = min(0.0, a, x3)
    shift_x = -min_x if min_x < 0 else 0.0

    p1 = (int(round(0 + shift_x)), int(round(0)))
    p2 = (int(round(a + shift_x)), int(round(0)))
    p3 = (int(round(x3 + shift_x)), int(round(y3)))
    
    logger.info(f"Вычислены координаты вершин: {p1}, {p2}, {p3}")

    return triangle_type, [p1, p2, p3]

if __name__ == "__main__":
    print("3, 4, 5:", get_triangle_info("3", "4", "5"))
    print("-" * 60)
    
    print("50, 50, 50:", get_triangle_info("50", "50", "50"))
    print("-" * 60)
    
    print("40, 40, 70:", get_triangle_info("40", "40", "70"))
    print("-" * 60)
    
    print("1, 2, 10:", get_triangle_info("1", "2", "10"))
    print("-" * 60)
    
    print("-5, 10, 10:", get_triangle_info("-5", "10", "10"))
    print("-" * 60)
    
    print("abc, 10, 10:", get_triangle_info("abc", "10", "10"))