import unittest
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pages.search_page import SearchFilterPage


class TestSearchFilter(unittest.TestCase):
    """UI-тесты для страницы Search Filter"""

    # Папка для скриншотов
    SCREENSHOTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "screenshots")

    def setUp(self):
        """Инициализация браузера перед каждым тестом"""
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        self.driver.implicitly_wait(5)
        self.page = SearchFilterPage(self.driver).open()

        # Создаём папку для скриншотов если её нет
        os.makedirs(self.SCREENSHOTS_DIR, exist_ok=True)

    def tearDown(self):
        """Закрытие сессии браузера после каждого теста"""
        # Делаем скриншот после каждого теста
        self.take_screenshot()

        if self.driver:
            self.driver.quit()

    def take_screenshot(self, name: str = None):
        """
        Создаёт скриншот текущего состояния браузера

        Args:
            name: Имя файла (по умолчанию используется имя теста)
        """
        if not name:
            # Используем имя текущего теста
            name = self._testMethodName

        # Формируем имя файла с датой и временем
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = os.path.join(self.SCREENSHOTS_DIR, filename)

        # Делаем скриншот
        self.driver.save_screenshot(filepath)
        print(f"📸 Скриншот сохранён: {filepath}")

    def take_screenshot_on_failure(self):
        """Делает скриншот только если тест упал"""
        if self._outcome.errors:
            # Проверяем есть ли ошибки
            for test, error in self._outcome.errors:
                if error:
                    self.take_screenshot(name=f"FAILED_{self._testMethodName}")
                    break

    # ========== Тесты ==========

    def test_default_state_shows_all_rows(self):
        """По умолчанию таблица содержит все 5 записей"""
        self.assertEqual(5, self.page.get_row_count())
        self.take_screenshot()  # Скриншот в конце теста

    def test_default_rows_content(self):
        """Проверка содержимого таблицы по умолчанию"""
        rows = self.page.get_all_rows_text()
        self.assertEqual(5, len(rows))
        self.assertIn("HouseRent", rows[0])
        self.assertIn("Salary", rows[3])
        self.assertIn("PowerBill", rows[4])

    def test_search_by_payee_salary(self):
        """Поиск по Payee 'Salary' возвращает 1 запись"""
        self.page.enter_payee("Salary")
        self.assertEqual(1, self.page.get_row_count())
        self.assertTrue(self.page.is_result_present("5000"))

    def test_search_by_payee_internet_bill(self):
        """Поиск по Payee 'InternetBill' возвращает 2 записи"""
        self.page.enter_payee("InternetBill")
        self.assertEqual(2, self.page.get_row_count())

    def test_search_by_payee_no_results(self):
        """Поиск по несуществующему Payee возвращает 0 записей"""
        self.page.enter_payee("NonExistentPerson")
        self.assertTrue(self.page.is_table_empty())

    def test_filter_account_cash(self):
        """Фильтр 'Cash' возвращает 3 записи"""
        self.page.select_account("Cash")
        self.assertEqual(3, self.page.get_row_count())

    def test_filter_account_bank_savings(self):
        """Фильтр 'Bank Savings' возвращает 2 записи"""
        self.page.select_account("Bank Savings")
        self.assertEqual(2, self.page.get_row_count())

    def test_filter_account_all(self):
        """Выбор 'All Accounts' возвращает все 5 записей"""
        self.page.select_account("Cash")
        self.page.select_account("All Accounts")
        self.assertEqual(5, self.page.get_row_count())

    def test_filter_type_income(self):
        """Фильтр 'INCOME' возвращает 1 запись (Salary)"""
        self.page.select_type("INCOME")
        self.assertEqual(1, self.page.get_row_count())
        self.assertTrue(self.page.is_result_present("Salary"))

    def test_filter_type_expenditure(self):
        """Фильтр 'EXPENDITURE' возвращает 4 записи"""
        self.page.select_type("EXPENDITURE")
        self.assertEqual(4, self.page.get_row_count())

    def test_filter_type_all(self):
        """Выбор 'All Types' возвращает все записи"""
        self.page.select_type("INCOME")
        self.page.select_type("All Types")
        self.assertEqual(5, self.page.get_row_count())

    def test_filter_expenditure_payee(self):
        """Фильтр по Expenditure Payees 'InternetBill' возвращает 2 записи"""
        self.page.enter_expenditure_payee("InternetBill")
        self.assertEqual(2, self.page.get_row_count())

    def test_filter_expenditure_payee_house_rent(self):
        """Фильтр по Expenditure Payees 'HouseRent' возвращает 1 запись"""
        self.page.enter_expenditure_payee("HouseRent")
        self.assertEqual(1, self.page.get_row_count())
        self.assertTrue(self.page.is_result_present("1000"))

    def test_combined_account_and_type(self):
        """Комбинация 'Bank Savings' + 'EXPENDITURE' = 1 запись (InternetBill 500)"""
        self.page.select_account("Bank Savings").select_type("EXPENDITURE")
        self.assertEqual(1, self.page.get_row_count())
        self.assertTrue(self.page.is_result_present("500"))

    def test_combined_payee_and_account(self):
        """Payee 'InternetBill' + Account 'Cash' = 1 запись (1200)"""
        self.page.enter_payee("InternetBill").select_account("Cash")
        self.assertEqual(1, self.page.get_row_count())
        self.assertTrue(self.page.is_result_present("1200"))

    def test_combined_all_filters(self):
        """Все фильтры одновременно: Cash + EXPENDITURE + InternetBill = 1 запись"""
        self.page.select_account("Cash") \
            .select_type("EXPENDITURE") \
            .enter_payee("InternetBill")
        self.assertEqual(1, self.page.get_row_count())
        self.assertTrue(self.page.is_result_present("1200"))

    def test_reset_payee_filter(self):
        """Сброс фильтра Payee возвращает все записи"""
        self.page.enter_payee("Salary")
        self.assertEqual(1, self.page.get_row_count())
        self.page.clear_payee()
        self.assertEqual(5, self.page.get_row_count())

    def test_reset_expenditure_filter(self):
        """Сброс фильтра Expenditure Payees возвращает все записи"""
        self.page.enter_expenditure_payee("PowerBill")
        self.assertEqual(1, self.page.get_row_count())
        self.page.clear_expenditure_payee()
        self.assertEqual(5, self.page.get_row_count())


if __name__ == '__main__':
    unittest.main(verbosity=2)