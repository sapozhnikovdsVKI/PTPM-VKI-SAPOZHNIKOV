from src.trianglecalc import TriangleCalculator
from src.database import DatabaseManager
from src.userinterface import IUserInterface
from src.external import IExternalService
from typing import Tuple, List

class Controller:
    """Контроллер для обработки запросов на вычисление треугольников"""
    
    def __init__(self, calculator: TriangleCalculator, 
                 db: DatabaseManager,
                 user_interface: IUserInterface,
                 external_service: IExternalService):
        self.calculator = calculator
        self.db = db
        self.user_interface = user_interface
        self.external_service = external_service
    
    def process_triangle(self, side_a: str, side_b: str, side_c: str) -> Tuple[str, List[Tuple], str]:
        """
        Основной метод обработки треугольника.
        
        Логика:
        1. Проверяет БД
        2. Если нет в БД -> вычисляет и сохраняет
        3. Отправляет результат внешнему сервису
        4. Возвращает результат
        """
        try:
            a = float(side_a)
            b = float(side_b)
            c = float(side_c)
        except ValueError:
            error_msg = "Некорректные входные данные"
            self.user_interface.show_error(error_msg)
            return "", [], error_msg
        
        # Проверяем БД
        cached_result = self.db.get_triangle(a, b, c)
        
        if cached_result:
            # Данные есть в БД
            triangle_type = cached_result['triangle_type']
            coordinates = cached_result['coordinates']
            error_message = cached_result['error_message']
            source = "БД (кэш)"
        else:
            # Вычисляем
            triangle_type, coordinates, error_message = self.calculator.calculate(side_a, side_b, side_c)
            
            # Сохраняем в БД
            self.db.add_triangle(a, b, c, triangle_type, coordinates, error_message)
            source = "Вычисление"
        
        # Формируем результат
        if triangle_type == "не треугольник" or not triangle_type:
            result_msg = f"❌ {error_message}"
        else:
            result_msg = (f"✅ Тип: {triangle_type}\n"
                         f"   Вершины: {coordinates}\n"
                         f"   Источник: {source}")
        
        # Отправляем внешнему сервису
        service_data = {
            'sides': [a, b, c],
            'type': triangle_type,
            'coordinates': coordinates
        }
        
        if self.external_service.send_data(service_data):
            result_msg += "\n   📤 Данные отправлены"
        else:
            result_msg += "\n   ⚠️ Ошибка отправки данных"
        
        self.user_interface.show_result(result_msg)
        return triangle_type, coordinates, error_message
    
    def get_user_input_and_process(self) -> bool:
        """Запрашивает данные у пользователя и обрабатывает"""
        try:
            self.user_interface.show_result("Введите длины сторон треугольника:")
            
            side_a = self.user_interface.get_input("Сторона A: ")
            side_b = self.user_interface.get_input("Сторона B: ")
            side_c = self.user_interface.get_input("Сторона C: ")
            
            self.process_triangle(side_a, side_b, side_c)
            return True
            
        except Exception as e:
            self.user_interface.show_error(f"Произошла ошибка: {e}")
            return False