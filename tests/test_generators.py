import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


def test_filter_by_currency_usd(sample_transactions: list[dict]) -> None:
    result = list(filter_by_currency(sample_transactions, "USD"))
    assert len(result) == 2
    assert all(item["operationAmount"]["currency"]["code"] == "USD" for item in result)


def test_filter_by_currency_empty(sample_transactions: list[dict]) -> None:
    result = list(filter_by_currency(sample_transactions, "RUB"))
    assert result == []


def test_transaction_descriptions(sample_transactions: list[dict]) -> None:
    result = list(transaction_descriptions(sample_transactions))
    assert result == ["Перевод на карту", "Оплата услуг", "Покупка товаров"]


@pytest.mark.parametrize("start,stop,expected_first,expected_last", [
    (1, 3, "0000 0000 0000 0001", "0000 0000 0000 0003"),
])
def test_card_number_generator(start: int, stop: int, expected_first: str, expected_last: str) -> None:
    gen = card_number_generator(start, stop)
    numbers = list(gen)
    assert numbers[0] == expected_first
    assert numbers[-1] == expected_last
    assert len(numbers) == stop - start + 1
