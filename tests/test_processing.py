import pytest
from typing import Any
from src.processing import filter_by_state, sort_by_date

@pytest.mark.parametrize('state, expected', [
    ("EXECUTED", 2),
    ("CANCELED", 1),
    ("PENDING", 0),
])
def test_filter_by_state(transactions: list[dict[str, Any]], state: str, expected: int) -> None:
    """Тест по параметризации"""
    result = filter_by_state(transactions, state)
    assert len(result) == expected


def test_filter_by_date_decrease(transactions: list[dict[str, Any]]) -> None:
    """Тест фильтрации по убыванию"""
    sorted_operation = sort_by_date(transactions)
    assert sorted_operation[0]["date"] > sorted_operation[-1]["date"]


def test_filter_by_date_increase(transactions: list[dict[str, Any]]) -> None:
    """Тест фильтрации по возрастанию"""
    sorted_operation = sort_by_date(transactions, reverse=False)
    assert sorted_operation[0]["date"] < sorted_operation[-1]["date"]
