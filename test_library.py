import pytest
from src.library import Library


# ========== ЗАДАНИЕ 1 - @pytest.mark.parametrize ==========

@pytest.mark.parametrize("title, author", [
    ("Маленький принц", "Сент-Экзюпери"),
    ("Три товарища", "Ремарк"),
    ("Над пропастью во ржи", "Сэлинджер"),
    ("Старик и море", "Хемингуэй")
])
def test_add_book_valid(empty_library, title, author):
    """Параметризованный тест для корректного добавления книг"""
    empty_library.add_book(title, author)
    book_info = empty_library.get_book_info(title)
    
    assert book_info is not None
    assert book_info["author"] == author
    assert book_info["available"] is True
    assert empty_library.get_available_count() == 1


@pytest.mark.parametrize("title, author, expected_error", [
    ("", "Толстой", "название и автор не могут быть пустыми"),
    ("Война и мир", "", "название и автор не могут быть пустыми"),
    ("", "", "название и автор не могут быть пустыми"),
    ("Война и мир", "Толстой", "уже существует")
])
def test_add_book_invalid(empty_library, title, author, expected_error):
    """Параметризованный тест для невалидного добавления книг"""
    if title == "Война и мир" and author == "Толстой":
        empty_library.add_book("Война и мир", "Толстой")
    
    with pytest.raises(ValueError) as exc_info:
        empty_library.add_book(title, author)
    
    assert expected_error.lower() in str(exc_info.value).lower()


@pytest.mark.parametrize("books_to_add, expected_available", [
    ([], 0),
    ([("book1", "author1")], 1),
    ([("book1", "author1"), ("book2", "author2")], 2),
    ([("book1", "author1"), ("book2", "author2"), ("book3", "author3")], 3)
])
def test_get_available_count(empty_library, books_to_add, expected_available):
    """Параметризованный тест для проверки количества доступных книг"""
    for title, author in books_to_add:
        empty_library.add_book(title, author)
    
    assert empty_library.get_available_count() == expected_available


# ========== ЗАДАНИЕ 2 - scope ==========

def test_readonly_first(library_readonly):
    """Первый тест с library_readonly (module scope)"""
    print(f"ID библиотеки (первый тест): {id(library_readonly)}")
    assert library_readonly.get_available_count() == 5


def test_readonly_second(library_readonly):
    """Второй тест с library_readonly (module scope)"""
    print(f"ID библиотеки (второй тест): {id(library_readonly)}")
    assert library_readonly.get_available_count() == 5
    
    book_info = library_readonly.get_book_info("Мастер и Маргарита")
    assert book_info is not None
    assert book_info["author"] == "Булгаков"


def test_empty_first(empty_library):
    """Первый тест с empty_library (function scope)"""
    print(f"ID пустой библиотеки (первый тест): {id(empty_library)}")
    assert empty_library.get_available_count() == 0
    
    empty_library.add_book("Тестовая книга", "Тестовый автор")
    assert empty_library.get_available_count() == 1


def test_empty_second(empty_library):
    """Второй тест с empty_library (function scope) - должна быть новой"""
    print(f"ID пустой библиотеки (второй тест): {id(empty_library)}")
    assert empty_library.get_available_count() == 0 


# ========== ЗАДАНИЕ 3 - yield ==========

def test_issue_book_from_yield_fixture(library):
    """Тест выдачи книги с использованием yield-фикстуры"""
    print(f"Доступно книг: {library.get_available_count()}")
    assert library.get_available_count() == 3
    
    library.issue_book("1984")
    
    assert library.get_available_count() == 2
    assert library.get_issued_count() == 1
    
    book_info = library.get_book_info("1984")
    assert book_info["available"] is False


def test_return_book_to_yield_fixture(library):
    """Тест возврата книги с использованием yield-фикстуры"""
    print(f"Доступно книг: {library.get_available_count()}")
    assert library.get_available_count() == 3
    
    library.issue_book("Война и мир")
    assert library.get_available_count() == 2
    
    library.return_book("Война и мир")
    assert library.get_available_count() == 3
    
    book_info = library.get_book_info("Война и мир")
    assert book_info["available"] is True


def test_complex_operations_with_yield_fixture(library):
    """Сложные операции с библиотекой, использующей yield-фикстуру"""
    print(f"Начальное состояние: {library.get_available_count()} доступно")
    assert library.get_available_count() == 3
    
    library.issue_book("1984")
    library.issue_book("Гарри Поттер и отсутствие Фролова")
    
    assert library.get_available_count() == 1
    assert library.get_issued_count() == 2
    
    library.return_book("1984")
    
    assert library.get_available_count() == 2
    assert library.get_issued_count() == 1


# ========== ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ ==========

def test_get_book_info_none(empty_library):
    """Тест получения информации о несуществующей книге"""
    assert empty_library.get_book_info("Несуществующая книга") is None


def test_issue_nonexistent_book(library):
    """Тест выдачи несуществующей книги"""
    with pytest.raises(ValueError, match="не найдена"):
        library.issue_book("Несуществующая книга")


def test_return_nonexistent_book(library):
    """Тест возврата несуществующей книги"""
    with pytest.raises(ValueError, match="не найдена"):
        library.return_book("Несуществующая книга")


def test_return_not_issued_book(library):
    """Тест возврата книги, которая не была выдана"""
    with pytest.raises(ValueError, match="не была выдана"):
        library.return_book("Война и мир")