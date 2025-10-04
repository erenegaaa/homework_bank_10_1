import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    ("card_number", "expected"),
    [
        ("1234567812345678", "1234 56** **** 5678"),
        ("1111222233334444", "1111 22** **** 4444"),
    ],
)
def test_get_mask_card_number_valid(card_number: str, expected: str) -> None:
    """Проверка корректной маскировки номера карты"""
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    "invalid_card",
    [
        "1234",
        "12345678901234567",
        "",
        "abcdabcdabcdabcd",
    ],
)
def test_get_mask_card_number_invalid(invalid_card: str) -> None:
    """Проверка, что выбрасывается ValueError при некорректной длине"""
    with pytest.raises(ValueError):
        get_mask_card_number(invalid_card)


@pytest.mark.parametrize(
    ("account_number", "expected"),
    [
        ("123456789", "**6789"),
        ("00001234", "**1234"),
        ("9876", "**9876"),
    ],
)
def test_get_mask_account_valid(account_number: str, expected: str) -> None:
    """Проверка корректной маскировки номера счёта"""
    assert get_mask_account(account_number) == expected


@pytest.mark.parametrize(
    "invalid_account",
    [
        "12",
        "",
    ],
)
def test_get_mask_account_invalid(invalid_account: str) -> None:
    """Проверка выброса ValueError при коротком номере счёта"""
    with pytest.raises(ValueError):
        get_mask_account(invalid_account)
