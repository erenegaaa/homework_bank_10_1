import os
import requests
from typing import Any
from dotenv import load_dotenv

load_dotenv()


def convert_to_rub(transaction: dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли.
    Если валюта RUB — возвращает сумму как есть.
    Если USD или EUR — делает запрос к API для получения курса.
    """
    amount = float(transaction.get("operation_amount", {}).get("amount", 0))
    currency = transaction.get("operation_amount", {}).get("currency", {}).get("code")

    if currency == "RUB":
        return amount

    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY отсутствует в .env файле")

    url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={amount}"
    headers = {"apikey": api_key}

    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        raise ConnectionError(f"Ошибка при обращении к API: {response.status_code}")

    data = response.json()
    return float(data.get("result", 0))
