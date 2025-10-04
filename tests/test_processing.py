import pytest

from src.processing import filter_by_state, sort_by_date

@pytest.mark.parametrize('state, expected', [
    ("EXECUTED", 2),
    ("CANCELED", 1),
    ("PENDING", 0),
])
def test_filter_by_state(transactions, state, expected):
    """Тест по параметризации"""
    result = filter_by_state(transactions, state)
    assert len(result) == expected


def test_filter_by_date_decrease(transactions):
    """Тест фильтрации по убыванию"""
    sorted_operation = sort_by_date(transactions)
    assert sorted_operation[0]["date"] > sorted_operation[-1]["date"]


def test_filter_by_date_increase(transactions):
    """Тест фильтрации по возрастанию"""
    sorted_operation = sort_by_date(transactions, reverse=False)
    assert sorted_operation[0]["date"] < sorted_operation[-1]["date"]
