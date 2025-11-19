from typing import Any

import pytest

from src.processing import filter_by_state, sort_by_date, get_amount, get_currency_code, filter_rub_only


@pytest.mark.parametrize(
    "state, expected",
    [
        ("EXECUTED", 2),
        ("CANCELED", 1),
        ("PENDING", 0),
    ],
)
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


def test_get_amount_from_csv():
    transaction = {
        "amount": 8200.0,
        "currency_code": "EUR",
        "description": "Test CSV"
    }
    assert get_amount(transaction) == 8200.0


def test_get_amount_from_json():
    transaction = {
        "operationAmount": {
            "amount": 1500.55,
            "currency": {"code": "USD"}
        }
    }
    assert get_amount(transaction) == 1500.55


def test_get_amount_missing():
    transaction = {"description": "no amount"}
    assert get_amount(transaction) is None


def test_get_currency_code_from_csv():
    transaction = {
        "amount": 8200.0,
        "currency_code": "EUR",
        "description": "Test CSV"
    }
    assert get_currency_code(transaction) == "EUR"


def test_get_currency_code_from_json():
    transaction = {
        "operationAmount": {
            "amount": 1500.55,
            "currency": {"code": "USD"}
        }
    }
    assert get_currency_code(transaction) == "USD"


def test_get_currency_code_no_currency():
    transaction = {"amount": 100}
    assert get_currency_code(transaction) is None


def test_get_currency_code_invalid_json_currency_format():
    # currency не dict → должно вернуть None
    transaction = {
        "operationAmount": {
            "amount": 100,
            "currency": "USD"
        }
    }
    assert get_currency_code(transaction) is None


def test_filter_rub_from_csv():
    data = [
        {"amount": 100, "currency_code": "RUB"},
        {"amount": 200, "currency_code": "USD"},
    ]
    result = filter_rub_only(data)
    assert len(result) == 1
    assert result[0]["currency_code"] == "RUB"


def test_filter_rub_from_json():
    data = [
        {"operationAmount": {"amount": 100, "currency": {"code": "RUB"}}},
        {"operationAmount": {"amount": 200, "currency": {"code": "EUR"}}},
    ]
    result = filter_rub_only(data)
    assert len(result) == 1


def test_filter_rub_with_currency_string():
    data = [
        {"amount": 100, "currency": "RUB"},
        {"amount": 200, "currency": "GBP"},
    ]
    result = filter_rub_only(data)
    assert len(result) == 1


def test_filter_rub_with_currency_dict():
    data = [
        {"currency": {"code": "RUB"}},
        {"currency": {"code": "USD"}},
    ]
    result = filter_rub_only(data)
    assert len(result) == 1


def test_filter_rub_empty():
    assert filter_rub_only([]) == []
