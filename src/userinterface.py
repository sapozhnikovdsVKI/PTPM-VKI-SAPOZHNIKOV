from abc import ABC, abstractmethod

class IUserInterface(ABC):
    """Абстрактный класс интерфейса пользователя"""
    
    @abstractmethod
    def get_input(self, prompt: str) -> str:
        """Получает ввод от пользователя"""
        pass
    
    @abstractmethod
    def show_result(self, message: str):
        """Показывает результат"""
        pass
    
    @abstractmethod
    def show_error(self, message: str):
        """Показывает ошибку"""
        pass

class ConsoleInterface(IUserInterface):
    """Консольный интерфейс"""
    
    def get_input(self, prompt: str) -> str:
        """Получает ввод из консоли"""
        return input(prompt)
    
    def show_result(self, message: str):
        """Выводит результат в консоль"""
        print(f"\n✅ Результат: {message}")
    
    def show_error(self, message: str):
        """Выводит ошибку в консоль"""
        print(f"\n❌ Ошибка: {message}")

class MockUserInterface(IUserInterface):
    """Тестовый интерфейс (заглушка)"""
    
    def __init__(self, inputs: list = None):
        self.inputs = inputs or []
        self.input_index = 0
        self.outputs = []
        self.errors = []
    
    def get_input(self, prompt: str) -> str:
        """Возвращает заранее заданный ввод"""
        if self.input_index < len(self.inputs):
            value = self.inputs[self.input_index]
            self.input_index += 1
            return value
        return ""
    
    def show_result(self, message: str):
        """Сохраняет результат"""
        self.outputs.append(message)
    
    def show_error(self, message: str):
        """Сохраняет ошибку"""
        self.errors.append(message)