import unittest
import datetime
from src.Delivery import calculate_delivery_cost  # Импортируем из папки src

class TestDeliveryCost(unittest.TestCase):
    
    def test_normal_delivery_calculation(self):
        """Тест обычного расчета: вес 10 кг, дистанция 1000 км"""
        cost, date_str = calculate_delivery_cost(weight=10.0, distance=1000, package_type="обычный")
        # База 200 + 1000*5 = 5200. Вес 10 кг (между 5 и 20) -> * 1.2 = 6240
        self.assertEqual(cost, 6240)
        self.assertEqual(date_str, "2026-09-05") # 1000 // 500 = 2 дня. 3 сентября + 2 = 5 сентября

    def test_express_delivery_should_be_more_expensive(self):
        """Тест экспресс-доставки: стоимость должна расти, а не падать"""
        cost_normal, _ = calculate_delivery_cost(weight=10.0, distance=1000, package_type="обычный", is_express=False)
        cost_express, _ = calculate_delivery_cost(weight=10.0, distance=1000, package_type="обычный", is_express=True)
        
        # ОЖИДАНИЕ: Экспресс должен стоить дороже обычного
        # ТЕКУЩЕЕ ПОВЕДЕНИЕ КОДА: cost_express будет в 2 раза МЕНЬШЕ (баг с *= 0.5)
        self.assertGreater(cost_express, cost_normal, "Экспресс-доставка не может быть дешевле обычной!")

    def test_express_delivery_minimum_one_day(self):
        """Тест экспресс-доставки на короткую дистанцию: минимум 1 день"""
        _, date_str = calculate_delivery_cost(weight=5.0, distance=400, package_type="обычный", is_express=True)
        
        # 400 // 500 = 0 -> max(1, 0) = 1 день.
        # Но в коде есть: days_needed // 2 -> 1 // 2 = 0 дней.
        # Дата не должна быть равна дате отправки (2026-09-03)
        self.assertNotEqual(date_str, "2026-09-03", "Доставка не может занять 0 дней!")

    def test_fragile_package(self):
        """Тест хрупкого груза"""
        cost, _ = calculate_delivery_cost(weight=2.0, distance=100, package_type="хрупкий")
        # База 200 + 100*5 = 700. Вес <= 5 (коэфф 1). Хрупкий +300. Итого 1000.
        self.assertEqual(cost, 1000)

    def test_dangerous_package(self):
        """Тест опасного груза"""
        cost, _ = calculate_delivery_cost(weight=25.0, distance=100, package_type="опасный")
        # База 200 + 100*5 = 700. Вес >= 20 -> * 1.5 = 1050. Опасный +1000. Итого 2050.
        self.assertEqual(cost, 2050)

    def test_invalid_weight_too_light(self):
        """Тест невалидного веса (слишком легкий)"""
        cost, date = calculate_delivery_cost(weight=0.05, distance=100, package_type="обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_invalid_weight_too_heavy(self):
        """Тест невалидного веса (слишком тяжелый)"""
        cost, date = calculate_delivery_cost(weight=55.0, distance=100, package_type="обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_invalid_distance(self):
        """Тест невалидной дистанции"""
        cost, date = calculate_delivery_cost(weight=10.0, distance=6000, package_type="обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_invalid_package_type(self):
        """Тест неверного типа посылки"""
        cost, date = calculate_delivery_cost(weight=10.0, distance=100, package_type="животное")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_boundary_weight_exact_5kg(self):
        """Граничное условие: вес ровно 5.0 кг"""
        cost, _ = calculate_delivery_cost(weight=5.0, distance=100, package_type="обычный")
        # Должен сработать базовый тариф без надбавки за вес (5.0 не > 5.0)
        self.assertEqual(cost, 700) # 200 + 500

if __name__ == '__main__':
    unittest.main(verbosity=2)
