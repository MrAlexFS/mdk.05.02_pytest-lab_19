import pytest


@pytest.fixture
def library():
    """Фикстура с yield: создаёт библиотеку с тремя книгами"""
    from src.library import Library
    
    print("\nSetup: библиотека готова")
    lib = Library()
    
    lib.add_book("Война и мир", "Толстой")
    lib.add_book("1984", "Оруэлл")
    lib.add_book("Гарри Поттер и отсутствие Фролова", "Роулинг")
    
    yield lib
    
    lib.clear()
    print("Teardown: библиотека очищена")


@pytest.fixture(scope="function")
def empty_library():
    """Фикстура с scope=function: пустая библиотека"""
    from src.library import Library
    
    lib = Library()
    print(f"Создана пустая библиотека (id: {id(lib)})")
    return lib


@pytest.fixture(scope="module")
def library_readonly():
    """Фикстура с scope=module: библиотека с пятью книгами"""
    from src.library import Library
    
    lib = Library()
    books = [
        ("Мастер и Маргарита", "Булгаков"),
        ("Преступление и наказание", "Достоевский"),
        ("Анна Каренина", "Толстой"),
        ("Собачье сердце", "Булгаков"),
        ("Идиот", "Достоевский")
    ]
    
    for title, author in books:
        lib.add_book(title, author)
    
    print(f"\nСоздана библиотека для чтения (id: {id(lib)})")
    return lib


@pytest.fixture(autouse=True)
def log_tests(request):
    """Фикстура с autouse=True: логирует начало и конец каждого теста"""
    print("\n" + "="*50)
    print(f"Запуск теста: {request.node.name}")
    print("="*50)
    
    yield
    
    print(f"\nЗавершён: {request.node.name}")
    print("="*50 + "\n")