import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()


def convert_to_rub(transaction: Any) -> float:
    """
    Конвертирует сумму транзакции в рубли.
    Если валюта RUB — возвращает сумму как есть.
    Если USD или EUR — делает запрос к API для получения курса.
    Работает как со словарём, так и с объектом с атрибутами.
    """
    def get_attr_or_key(obj, key, default=None):
        """Помощник: достает значение по ключу или атрибуту."""
        if isinstance(obj, dict):
            return obj.get(key, default)
        return getattr(obj, key, default)

    amount_data = (
        get_attr_or_key(transaction, "operationAmount")
        or get_attr_or_key(transaction, "operation_amount", {})
    )

    amount = float(get_attr_or_key(amount_data, "amount", 0))

    currency_data = get_attr_or_key(amount_data, "currency", {})
    currency = get_attr_or_key(currency_data, "code")

    if not currency:
        raise ValueError("Не удалось определить валюту транзакции")

    if currency == "RUB":
        return amount

    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY отсутствует в .env файле")

    url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={amount}"
    headers = {"apikey": api_key}

    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        raise ConnectionError(f"Ошибка при обращении к API: {response.status_code} - {response.text}")

    data = response.json()
    return float(data.get("result", 0))
