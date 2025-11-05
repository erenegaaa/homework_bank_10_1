import pytest
from unittest.mock import patch, Mock
from src.external_api import convert_to_rub

# Тест для RUB должно возвращать сумму без изменений
def test_convert_rub_no_api_call():
    transaction = {
        "operation_amount": {
            "amount": 1000,
            "currency": {"code": "RUB"}
        }
    }
    result = convert_to_rub(transaction)
    assert result == 1000

# Тест для USD подменяем API ответ
@patch("src.external_api.requests.get")
def test_convert_usd_to_rub(mock_get):
    transaction = {
        "operation_amount": {
            "amount": 10,
            "currency": {"code": "USD"}
        }
    }

    # Настраиваем mock ответа API
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 900}
    mock_get.return_value = mock_response

    result = convert_to_rub(transaction)
    assert result == 900
    mock_get.assert_called_once()

# Тест для EUR подменяем API ответ
@patch("src.external_api.requests.get")
def test_convert_eur_to_rub(mock_get):
    transaction = {
        "operation_amount": {
            "amount": 5,
            "currency": {"code": "EUR"}
        }
    }

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 500}
    mock_get.return_value = mock_response

    result = convert_to_rub(transaction)
    assert result == 500
    mock_get.assert_called_once()

# Тест ошибки API
@patch("src.external_api.requests.get")
def test_convert_api_error(mock_get):
    transaction = {
        "operation_amount": {
            "amount": 1,
            "currency": {"code": "USD"}
        }
    }

    mock_response = Mock()
    mock_response.status_code = 400  # Симулируем ошибку API
    mock_get.return_value = mock_response

    import pytest
    with pytest.raises(ConnectionError):
        convert_to_rub(transaction)


