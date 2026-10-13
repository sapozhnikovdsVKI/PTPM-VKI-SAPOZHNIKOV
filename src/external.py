from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)

class IExternalService(ABC):
    """Абстрактный класс внешней зависимости"""
    
    @abstractmethod
    def send_data(self, data: dict) -> bool:
        """Отправляет данные внешнему сервису"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Проверяет доступность сервиса"""
        pass

class EmailService(IExternalService):
    """Реальный сервис отправки email (имитация)"""
    
    def __init__(self, server_address: str = "smtp.example.com"):
        self.server_address = server_address
        self.is_connected = False
    
    def send_data(self, data: dict) -> bool:
        """Имитирует отправку email"""
        try:
            logger.info(f"Отправка данных на {self.server_address}: {data}")
            # Здесь был бы реальный код отправки email
            self.is_connected = True
            return True
        except Exception as e:
            logger.error(f"Ошибка отправки: {e}")
            return False
    
    def is_available(self) -> bool:
        """Проверяет доступность сервера"""
        # Имитация проверки доступности
        return True

class MockExternalService(IExternalService):
    """Тестовая заглушка для внешнего сервиса"""
    
    def __init__(self, should_succeed: bool = True):
        self.should_succeed = should_succeed
        self.sent_data = []
        self.call_count = 0
    
    def send_data(self, data: dict) -> bool:
        """Имитирует отправку (успешную или нет)"""
        self.call_count += 1
        self.sent_data.append(data)
        logger.info(f"[MOCK] Отправка данных: {data}")
        return self.should_succeed
    
    def is_available(self) -> bool:
        """Всегда доступен в тестах"""
        return True