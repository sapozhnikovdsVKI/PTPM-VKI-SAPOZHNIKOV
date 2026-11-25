from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class SearchFilterPage:
    """Page Object для страницы Search Filter"""

    URL = "https://www.globalsqa.com/angularJs-protractor/SearchFilter/"

    # === Локаторы элементов (приватные) ===
    _PAYEE_INPUT = (By.ID, "input1")
    _ACCOUNT_SELECT = (By.ID, "input2")
    _TYPE_SELECT = (By.ID, "input3")
    _EXPENDITURE_INPUT = (By.ID, "input4")

    _RESULTS_TABLE = (
        By.XPATH,
        "//h3[normalize-space()='Search Results']/following::table[1]",
    )
    _TABLE_ROWS = (By.CSS_SELECTOR, "tbody tr:has(td)")

    def _get_rows(self):
        table = self.wait.until(
            EC.visibility_of_element_located(self._RESULTS_TABLE)
        )
        return table.find_elements(*self._TABLE_ROWS)

    def get_row_count(self) -> int:
        return len(self._get_rows())

    def get_row_text(self, index: int) -> str:
        return self._get_rows()[index].text

    def get_all_rows_text(self) -> list[str]:
        return [row.text for row in self._get_rows()]


    def __init__(self, driver):
        """Инициализация Page Object"""
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self) -> 'SearchFilterPage':
        """Открыть страницу"""
        self.driver.get(self.URL)
        self.wait.until(EC.presence_of_element_located(self._PAYEE_INPUT))
        return self

    def enter_payee(self, text: str) -> 'SearchFilterPage':
        """Ввести имя получателя (Payee Name)"""
        field = self.wait.until(EC.presence_of_element_located(self._PAYEE_INPUT))
        field.clear()
        field.send_keys(text)
        return self

    def select_account(self, account: str) -> 'SearchFilterPage':
        """Выбрать счёт (All Accounts / Cash / Bank Savings)"""
        select = Select(self.wait.until(EC.presence_of_element_located(self._ACCOUNT_SELECT)))
        select.select_by_visible_text(account)
        return self

    def select_type(self, type_: str) -> 'SearchFilterPage':
        """Выбрать тип (All Types / EXPENDITURE / INCOME)"""
        select = Select(self.wait.until(EC.presence_of_element_located(self._TYPE_SELECT)))
        select.select_by_visible_text(type_)
        return self

    def enter_expenditure_payee(self, text: str) -> 'SearchFilterPage':
        """Ввести получателя расходов (Expenditure Payees)"""
        field = self.wait.until(EC.presence_of_element_located(self._EXPENDITURE_INPUT))
        field.clear()
        field.send_keys(text)
        return self

    def clear_payee(self) -> 'SearchFilterPage':
        """Очистить поле Payee"""
        field = self.wait.until(EC.presence_of_element_located(self._PAYEE_INPUT))
        field.clear()
        return self

    def clear_expenditure_payee(self) -> 'SearchFilterPage':
        """Очистить поле Expenditure Payees"""
        field = self.wait.until(EC.presence_of_element_located(self._EXPENDITURE_INPUT))
        field.clear()
        return self


    def is_result_present(self, expected_text: str) -> bool:
        """Проверить, есть ли в результатах строка с ожидаемым текстом"""
        rows_text = self.get_all_rows_text()
        return any(expected_text in row for row in rows_text)

    def is_table_empty(self) -> bool:
        """Проверить, что таблица результатов пуста"""
        return self.get_row_count() == 0