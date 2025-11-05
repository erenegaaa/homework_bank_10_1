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
    try:
        amount_data = transaction.get("operation_amount", {})
        amount = float(amount_data.get("amount", 0))
    except AttributeError:
        amount_data = getattr(transaction, "operation_amount", None)
        amount = float(getattr(amount_data, "amount", 0)) if amount_data else 0

    try:
        currency_data = amount_data.get("currency", {})
        currency = currency_data.get("code")
    except AttributeError:
        currency_data = getattr(amount_data, "currency", None)
        currency = getattr(currency_data, "code", None) if currency_data else None

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


# if __name__ == "__main__":
#     transaction = {
#         "operation_amount": {
#             "amount": "100",
#             "currency": {"code": "USD"}
#         }
#     }
#
#     result = convert_to_rub(transaction)
#     print("Конвертированная сумма в RUB:", result)
