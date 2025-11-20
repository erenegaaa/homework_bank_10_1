from typing import Any, Dict, List

import pytest

from src.search import process_bank_operations, process_bank_search


@pytest.fixture
def data() -> List[Dict[str, Any]]:
    return [
        {"description": "Оплата мобильной связи"},
        {"description": "Перевод на карту"},
        {"description": "Оплата услуг"},
        {"description": "Покупка продуктов"},
    ]


def test_process_bank_search_found(data: List[Dict[str, Any]]) -> None:
    result = process_bank_search(data, "оплата")
    assert len(result) == 2
    assert all("оплата" in str(item["description"]).lower() for item in result)


def test_process_bank_search_not_found(data: List[Dict[str, Any]]) -> None:
    assert process_bank_search(data, "крипта") == []


def test_process_bank_operations(data: List[Dict[str, Any]]) -> None:
    categories = ["оплата", "перевод"]
    result = process_bank_operations(data, categories)
    assert result == {"оплата": 2, "перевод": 1}


def test_process_bank_operations_empty() -> None:
    assert process_bank_operations([], ["test"]) == {}
