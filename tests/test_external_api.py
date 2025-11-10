from unittest.mock import Mock, patch

import pytest

from src.external_api import convert_to_rub


def test_rub_returns_amount_without_api() -> None:
    """Если валюта RUB — возвращается сумма без запроса к API."""
    transaction = {"operationAmount": {"amount": 1000, "currency": {"code": "RUB"}}}
    result = convert_to_rub(transaction)
    assert result == 1000


@patch("src.external_api.requests.get")
def test_usd_to_rub(mock_get: Mock) -> None:
    """Тест корректного пересчёта USD в RUB."""
    transaction = {"operationAmount": {"amount": 10, "currency": {"code": "USD"}}}

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 900}
    mock_get.return_value = mock_response

    result = convert_to_rub(transaction)
    assert result == 900
    mock_get.assert_called_once()


@patch("src.external_api.requests.get")
def test_eur_to_rub(mock_get: Mock) -> None:
    """Тест корректного пересчёта EUR в RUB."""
    transaction = {"operationAmount": {"amount": 5, "currency": {"code": "EUR"}}}

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 500}
    mock_get.return_value = mock_response

    result = convert_to_rub(transaction)
    assert result == 500
    mock_get.assert_called_once()


@patch("src.external_api.requests.get")
def test_api_error(mock_get: Mock) -> None:
    """Тест: выбрасывается ошибка при проблеме с API."""
    transaction = {"operationAmount": {"amount": 1, "currency": {"code": "USD"}}}

    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.text = "Bad Request"
    mock_get.return_value = mock_response

    with pytest.raises(ConnectionError):
        convert_to_rub(transaction)


@patch("src.external_api.os.getenv", return_value=None)
def test_missing_api_key(_: Mock) -> None:
    """Тест: ошибка, если нет API_KEY в окружении."""
    transaction = {"operationAmount": {"amount": 10, "currency": {"code": "USD"}}}
    with pytest.raises(ValueError, match="API_KEY отсутствует"):
        convert_to_rub(transaction)


def test_no_currency() -> None:
    """Тест: ошибка при отсутствии валютного кода."""
    transaction = {"operationAmount": {"amount": 100, "currency": {}}}
    with pytest.raises(ValueError, match="Не удалось определить валюту"):
        convert_to_rub(transaction)


class TransactionObj:
    def __init__(self) -> None:
        self.operationAmount = type(
            "Amount", (), {"amount": 50, "currency": type("Currency", (), {"code": "RUB"})()}
        )()


def test_with_object_input() -> None:
    """Тест: функция работает с объектом с атрибутами."""
    t = TransactionObj()
    result = convert_to_rub(t)
    assert result == 50
