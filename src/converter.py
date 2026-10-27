class Converter:

    @staticmethod
    def do(x: float) -> int:
 
        if x == 0.0:
            raise ValueError("x не может быть равен 0.0")
        
        if x >= 100.7:
            return 1000
        
        if 0 < x < 100.7:
            return int(x)
        
        if -30.4 <= x < 0:
            return int(x) - 5
        
        if x <= -30.5:
            return -2000
        
        # Промежуток (-30.5; -30.4) не покрыт условиями
        # Но по заданию вход всегда с точностью 1 знак, поэтому таких значений не будет
        raise ValueError(f"Значение {x} не попадает ни в один диапазон")