import unittest
import os
from src.trianglecalc import TriangleCalculator
from src.database import DatabaseManager
from src.userinterface import MockUserInterface
from src.external import MockExternalService
from src.controller import Controller

class TestTriangleIntegration(unittest.TestCase):
    """Интеграционные тесты для системы расчета треугольников"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        # Создаем тестовую БД
        self.test_db_path = "test_triangles.db"
        
        # Создаем компоненты
        self.calculator = TriangleCalculator()
        self.db = DatabaseManager(self.test_db_path)
        self.userinterface = MockUserInterface()
        self.external = MockExternalService()
        
        # Создаем контроллер
        self.controller = Controller(
            calculator=self.calculator,
            db=self.db,
            userinterface=self.userinterface,
            external=self.external
        )
    
    def tearDown(self):
        """Очистка после каждого теста"""
        self.db.clear_all()
        self.db._get_connection().close()
        # Удаляем файл БД
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
    
    # ========== ИНТЕГРАЦИОННЫЙ ТЕСТ 1 ==========
    def test_full_workflow_new_triangle(self):
        """
        ИНТЕГРАЦИОННЫЙ ТЕСТ: Полный цикл обработки нового треугольника
        Проверяет взаимодействие всех компонентов
        """
        # Вызываем контроллер
        triangle_type, coordinates, error = self.controller.process_triangle("3", "4", "5")
        
        # Проверяем результат вычислений
        self.assertEqual(triangle_type, "разносторонний")
        self.assertEqual(len(coordinates), 3)
        self.assertEqual(error, "")
        
        # Проверяем что данные сохранены в БД
        cached = self.db.get_triangle(3.0, 4.0, 5.0)
        self.assertIsNotNone(cached)
        self.assertEqual(cached['triangle_type'], "разносторонний")
        
        # Проверяем что данные отправлены внешнему сервису
        self.assertEqual(self.external.call_count, 1)
        self.assertEqual(self.external.sent_data[0]['type'], "разносторонний")
        
        # Проверяем что интерфейс показал результат
        self.assertEqual(len(self.userinterface.outputs), 1)
        self.assertIn("разносторонний", self.userinterface.outputs[0])
    
    # ========== ИНТЕГРАЦИОННЫЙ ТЕСТ 2 ==========
    def test_caching_from_database(self):
        """
        ИНТЕГРАЦИОННЫЙ ТЕСТ: Проверка кэширования
        Второй запрос должен взять данные из БД, а не вычислять
        """
        # Первый запрос - вычисление
        self.controller.process_triangle("5", "5", "5")
        first_call_count = self.external.call_count
        
        # Второй запрос с теми же данными - должен взять из БД
        self.controller.process_triangle("5", "5", "5")
        second_call_count = self.external.call_count
        
        # Внешний сервис должен быть вызван дважды (для каждого запроса)
        self.assertEqual(second_call_count, 2)
        
        # Но в БД должна быть только одна запись
        # (проверяем что не создались дубликаты)
        self.db._get_connection()  # Просто чтобы получить подключение
        import sqlite3
        conn = sqlite3.connect(self.test_db_path)
        count = conn.execute("SELECT COUNT(*) FROM triangles").fetchone()[0]
        conn.close()
        self.assertEqual(count, 1)
    
    # ========== ИНТЕГРАЦИОННЫЙ ТЕСТ 3 ==========
    def test_error_handling_integration(self):
        """
        ИНТЕГРАЦИОННЫЙ ТЕСТ: Обработка ошибок во всех компонентах
        """
        # Невалидные данные
        triangle_type, coordinates, error = self.controller.process_triangle("-5", "10", "10")
        
        # Проверяем результат
        self.assertEqual(triangle_type, "не треугольник")
        self.assertNotEqual(error, "")
        
        # Проверяем что ошибка сохранена в БД
        cached = self.db.get_triangle(-5.0, 10.0, 10.0)
        self.assertIsNotNone(cached)
        self.assertEqual(cached['triangle_type'], "не треугольник")
        self.assertIn("положительными", cached['error_message'])
        
        # Проверяем что интерфейс показал ошибку
        self.assertEqual(len(self.user_interface.errors), 0)  # Ошибка в result, не в error
        self.assertTrue(any("не треугольник" in out for out in self.user_interface.outputs))
    
    # ========== ИНТЕГРАЦИОННЫЙ ТЕСТ 4 (дополнительный) ==========
    def test_external_service_failure(self):
        """
        ИНТЕГРАЦИОННЫЙ ТЕСТ: Обработка сбоя внешнего сервиса
        """
        # Создаем сервис который всегда падает
        failing_service = MockExternalService(should_succeed=False)
        self.controller.external_service = failing_service
        
        # Вызываем контроллер
        triangle_type, coordinates, error = self.controller.process_triangle("3", "4", "5")
        
        # Вычисление должно пройти успешно
        self.assertEqual(triangle_type, "разносторонний")
        
        # Но сервис должен быть вызван и вернуть failure
        self.assertEqual(failing_service.call_count, 1)
        
        # Проверяем что в результате есть предупреждение
        result_output = self.user_interface.outputs[0]
        self.assertIn("⚠️ Ошибка отправки данных", result_output)
    
    # ========== ИНТЕГРАЦИОННЫЙ ТЕСТ 5 (дополнительный) ==========
    def test_multiple_triangles_workflow(self):
        """
        ИНТЕГРАЦИОННЫЙ ТЕСТ: Обработка нескольких треугольников
        """
        triangles = [
            ("3", "4", "5", "разносторонний"),
            ("5", "5", "5", "равносторонний"),
            ("40", "40", "70", "равнобедренный"),
        ]
        
        for a, b, c, expected_type in triangles:
            triangle_type, _, _ = self.controller.process_triangle(a, b, c)
            self.assertEqual(triangle_type, expected_type)
        
        # Проверяем что все сохранены в БД
        self.assertEqual(len(self.userinterface.outputs), 3)
        
        # Проверяем что внешний сервис вызван 3 раза
        self.assertEqual(self.external.call_count, 3)


if __name__ == '__main__':
    unittest.main(verbosity=2)
