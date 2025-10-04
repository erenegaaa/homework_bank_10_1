import pytest

@pytest.fixture
def transactions():
    """Функция с тестами для модулей - тесты операций"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2022-05-20T10:30:00.000000"},
        {"id": 2, "state": "CANCELED", "date": "2021-09-15T09:10:00.000000"},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-01T12:00:00.000000"},
    ]