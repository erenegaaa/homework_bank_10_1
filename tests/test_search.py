import pytest
from src.search import process_bank_search, process_bank_operations


@pytest.fixture
def data():
    return [
        {"description": "Оплата мобильной связи"},
        {"description": "Перевод на карту"},
        {"description": "Оплата услуг"},
        {"description": "Покупка продуктов"},
    ]


def test_process_bank_search_found(data):
    result = process_bank_search(data, "оплата")
    assert len(result) == 2
    assert all("оплата" in item["description"].lower() for item in result)


def test_process_bank_search_not_found(data):
    assert process_bank_search(data, "крипта") == []


def test_process_bank_operations(data):
    categories = ["оплата", "перевод"]
    result = process_bank_operations(data, categories)
    assert result == {"оплата": 2, "перевод": 1}


def test_process_bank_operations_empty():
    assert process_bank_operations([], ["test"]) == {}
