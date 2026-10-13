import sqlite3
import json
from typing import Optional, Tuple, List

class DatabaseManager:
    """Класс для работы с базой данных треугольников"""
    
    def __init__(self, db_path: str = "triangles.db"):
        self.db_path = db_path
        self._create_table()
    
    def _get_connection(self):
        """Создает подключение к БД"""
        return sqlite3.connect(self.db_path)
    
    def _create_table(self):
        """Создает таблицу треугольников"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS triangles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    side_a REAL NOT NULL,
                    side_b REAL NOT NULL,
                    side_c REAL NOT NULL,
                    triangle_type TEXT,
                    coordinates TEXT,
                    error_message TEXT,
                    UNIQUE(side_a, side_b, side_c)
                )
            ''')
            conn.commit()
    
    def add_triangle(self, side_a: float, side_b: float, side_c: float,
                    triangle_type: str, coordinates: List[Tuple], 
                    error_message: str = "") -> bool:
        """
        Добавляет треугольник в БД.
        Возвращает True если успешно, False если уже существует.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR IGNORE INTO triangles 
                    (side_a, side_b, side_c, triangle_type, coordinates, error_message)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (side_a, side_b, side_c, triangle_type, 
                      json.dumps(coordinates), error_message))
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Ошибка БД: {e}")
            return False
    
    def get_triangle(self, side_a: float, side_b: float, side_c: float) -> Optional[dict]:
        """
        Получает треугольник из БД по сторонам.
        Возвращает dict с данными или None если не найдено.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT triangle_type, coordinates, error_message
                    FROM triangles
                    WHERE side_a = ? AND side_b = ? AND side_c = ?
                ''', (side_a, side_b, side_c))
                
                row = cursor.fetchone()
                if row:
                    return {
                        'triangle_type': row[0],
                        'coordinates': json.loads(row[1]),
                        'error_message': row[2]
                    }
                return None
        except sqlite3.Error as e:
            print(f"Ошибка БД: {e}")
            return None
    
    def delete_triangle(self, side_a: float, side_b: float, side_c: float) -> bool:
        """
        Удаляет треугольник из БД.
        Возвращает True если удалено, False если не найдено.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    DELETE FROM triangles
                    WHERE side_a = ? AND side_b = ? AND side_c = ?
                ''', (side_a, side_b, side_c))
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Ошибка БД: {e}")
            return False
    
    def clear_all(self):
        """Очищает всю таблицу (для тестов)"""
        with self._get_connection() as conn:
            conn.execute("DELETE FROM triangles")