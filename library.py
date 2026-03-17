class Library:
    """Класс для управления библиотекой книг"""
    
    def __init__(self):
        self._books = {}  # {title: {"author": author, "available": bool}}
    
    def add_book(self, title: str, author: str) -> None:
        """Добавляет книгу в библиотеку"""
        if not title or not author:
            raise ValueError("Название и автор не могут быть пустыми")
        
        if title in self._books:
            raise ValueError(f"Книга '{title}' уже существует в библиотеке")
        
        self._books[title] = {"author": author, "available": True}
        print(f"Книга добавлена: '{title}' - {author}")
    
    def issue_book(self, title: str) -> None:
        """Выдаёт книгу читателю"""
        if title not in self._books:
            raise ValueError(f"Книга '{title}' не найдена в библиотеке")
        
        if not self._books[title]["available"]:
            raise ValueError(f"Книга '{title}' уже выдана")
        
        self._books[title]["available"] = False
        print(f"Книга выдана: '{title}'")
    
    def return_book(self, title: str) -> None:
        """Возвращает книгу в библиотеку"""
        if title not in self._books:
            raise ValueError(f"Книга '{title}' не найдена в библиотеке")
        
        if self._books[title]["available"]:
            raise ValueError(f"Книга '{title}' не была выдана")
        
        self._books[title]["available"] = True
        print(f"Книга возвращена: '{title}'")
    
    def get_available_count(self) -> int:
        """Возвращает количество доступных книг"""
        return sum(1 for book in self._books.values() if book["available"])
    
    def get_issued_count(self) -> int:
        """Возвращает количество выданных книг"""
        return sum(1 for book in self._books.values() if not book["available"])
    
    def get_book_info(self, title: str) -> dict | None:
        """Возвращает информацию о книге или None"""
        return self._books.get(title)
    
    def clear(self) -> None:
        """Очищает библиотеку (для teardown)"""
        self._books.clear()
        print("Библиотека очищена")