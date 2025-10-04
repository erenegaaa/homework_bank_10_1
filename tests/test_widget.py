import pytest
from src.widget import mask_account_card, get_date


@pytest.mark.parametrize("input_data,expected", [
    ("Visa Classic 1234567812345678", "Visa Classic: 1234 56** **** 5678"),
    ("MasterCard 5555444433331111", "MasterCard: 5555 44** **** 1111"),
    ("Счет 12345678901234567890", "Счет: **7890"),
])
def test_mask_account_card_valid(input_data, expected):
    """Проверка корректной маскировки карт и счетов"""
    assert mask_account_card(input_data) == expected


@pytest.mark.parametrize("invalid_data", [
    12345,
    "Visa Classic",
    "Счет ABCD",
    "Карта 12345",
])
def test_mask_account_card_invalid(invalid_data):
    """Проверка, что для некорректных данных выбрасывается ValueError"""
    with pytest.raises(ValueError):
        mask_account_card(invalid_data)


@pytest.mark.parametrize("input_date,expected", [
    ("2019-07-03T18:35:29.512364", "03.07.2019"),
    ("2022-01-01T00:00:00.000000", "01.01.2022"),
])
def test_get_date_valid(input_date, expected):
    """Проверка корректного преобразования формата даты"""
    assert get_date(input_date) == expected


@pytest.mark.parametrize("invalid_date", [
    "2019/07/03",
    "03.07.2019",
    "text",
    "",
])
def test_get_date_invalid(invalid_date):
    """Проверка, что для некорректного формата выбрасывается ValueError"""
    with pytest.raises(ValueError):
        get_date(invalid_date)

