import unittest
from unittest.mock import Mock, patch
from src.database import DatabaseManager
from src.userinterface import MockUserInterface
from src.external import MockExternalService

class TestUnitComponents(unittest.TestCase):
    """Юнит-тесты отдельных компонентов"""
    
    # ========== ЮНИТ ТЕСТ 1 ==========
    def test_mock_user_interface(self):
        """
        ЮНИТ ТЕСТ: Проверка тестовой заглушки интерфейса
        """
        # Создаем заглушку с предопределенными вводами
        mock_ui = MockUserInterface(inputs=["3", "4", "5"])
        
        # Проверяем get_input
        self.assertEqual(mock_ui.get_input("Prompt: "), "3")
        self.assertEqual(mock_ui.get_input("Prompt: "), "4")
        self.assertEqual(mock_ui.get_input("Prompt: "), "5")
        
        # Проверяем show_result
        mock_ui.show_result("Test result")
        self.assertEqual(mock_ui.outputs, ["Test result"])
        
        # Проверяем show_error
        mock_ui.show_error("Test error")
        self.assertEqual(mock_ui.errors, ["Test error"])
    
    # ========== ЮНИТ ТЕСТ 2 ==========
    def test_mock_external_service(self):
        """
        ЮНИТ ТЕСТ: Проверка тестовой заглушки внешнего сервиса
        """
        # Успешный сервис
        success_service = MockExternalService(should_succeed=True)
        data = {'test': 'data'}
        
        result = success_service.send_data(data)
        self.assertTrue(result)
        self.assertEqual(success_service.call_count, 1)
        self.assertEqual(success_service.sent_data, [data])
        self.assertTrue(success_service.is_available())
        
        # Падающий сервис
        fail_service = MockExternalService(should_succeed=False)
        result = fail_service.send_data(data)
        self.assertFalse(result)
        self.assertEqual(fail_service.call_count, 1)
    
    # ========== ЮНИТ ТЕСТ 3 (дополнительный) ==========
    def test_database_operations_isolated(self):
        """
        ЮНИТ ТЕСТ: Изолированная проверка методов БД
        """
        db = DatabaseManager("test_unit.db")
        
        try:
            # Тест add_triangle
            result = db.add_triangle(3.0, 4.0, 5.0, "разносторонний", 
                                    [(0,0), (3,0), (0,4)], "")
            self.assertTrue(result)
            
            # Тест get_triangle
            retrieved = db.get_triangle(3.0, 4.0, 5.0)
            self.assertIsNotNone(retrieved)
            self.assertEqual(retrieved['triangle_type'], "разносторонний")
            
            # Тест delete_triangle
            deleted = db.delete_triangle(3.0, 4.0, 5.0)
            self.assertTrue(deleted)
            
            # Проверяем что удалено
            retrieved = db.get_triangle(3.0, 4.0, 5.0)
            self.assertIsNone(retrieved)
            
        finally:
            db.clear_all()
            import os
            if os.path.exists("test_unit.db"):
                os.remove("test_unit.db")


if __name__ == '__main__':
    unittest.main(verbosity=2)