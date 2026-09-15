import math

def get_triangle_info(str_a, str_b, str_c):
    """
    Вычисляет вид треугольника и координаты его вершин по длинам трех сторон.
    """

    try:
        a = float(str_a)
        b = float(str_b)
        c = float(str_c)
    except ValueError:

        return "", [(-2, -2), (-2, -2), (-2, -2)]

    if a <= 0 or b <= 0 or c <= 0:
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    if (a + b <= c) or (a + c <= b) or (b + c <= a):
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    if math.isclose(a, b) and math.isclose(b, c):
        triangle_type = "равносторонний"
    elif math.isclose(a, b) or math.isclose(a, c) or math.isclose(b, c):
        triangle_type = "равнобедренный"
    else:
        triangle_type = "разносторонний"

    x3 = (a**2 + b**2 - c**2) / (2 * a)

    y3_squared = b**2 - x3**2
    y3 = math.sqrt(y3_squared) if y3_squared > 0 else 0.0

    min_x = min(0.0, a, x3)
    shift_x = -min_x if min_x < 0 else 0.0

    p1 = (int(round(0 + shift_x)), int(round(0)))
    p2 = (int(round(a + shift_x)), int(round(0)))
    p3 = (int(round(x3 + shift_x)), int(round(y3)))

    return triangle_type, [p1, p2, p3]

if __name__ == "__main__":
    print("3, 4, 5:", get_triangle_info("3", "4", "5"))
    
    print("50, 50, 50:", get_triangle_info("50", "50", "50"))
    
    print("40, 40, 70:", get_triangle_info("40", "40", "70"))
    
    print("1, 2, 10:", get_triangle_info("1", "2", "10"))
    
    print("-5, 10, 10:", get_triangle_info("-5", "10", "10"))
    
    print("abc, 10, 10:", get_triangle_info("abc", "10", "10"))