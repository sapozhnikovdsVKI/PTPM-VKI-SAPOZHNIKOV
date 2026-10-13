from src.trianglecalc import TriangleCalculator
from src.database import DatabaseManager
from src.userinterface import ConsoleInterface
from src.external import EmailService
from src.controller import Controller

def main():
    """Главная функция приложения"""
    print("=" * 60)
    print("СИСТЕМА РАСЧЕТА ТРЕУГОЛЬНИКОВ")
    print("=" * 60)
    
    # Инициализация компонентов
    calculator = TriangleCalculator()
    db = DatabaseManager("triangles.db")
    userinterface = ConsoleInterface()
    external = EmailService()
    
    # Создание контроллера
    controller = Controller(
        calculator=calculator,
        db=db,
        user_interface=userinterface,
        external_service=external
    )
    
    # Основной цикл
    while True:
        try:
            controller.get_user_input_and_process()
            
            cont = input("\nПродолжить? (да/нет): ").lower()
            if cont not in ['да', 'd', 'yes', 'y']:
                break
                
        except KeyboardInterrupt:
            print("\n\nЗавершение работы...")
            break
        except Exception as e:
            userinterface.show_error(f"Неожиданная ошибка: {e}")
    
    print("\nСпасибо за использование системы!")

if __name__ == "__main__":
    main()