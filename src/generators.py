from typing import Iterator, Any


def filter_by_currency(transactions: list[dict[str, Any]], currency: str) -> Iterator[dict[str, Any]]:
    """
    Фильтрует операции по заданной валюте.
    Возвращает генератор словарей с нужной валютой.
    """
    for transaction in transactions:
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency:
            yield transaction


def transaction_descriptions(transactions: list[dict[str, Any]]) -> Iterator[str]:
    """
    Генератор, который возвращает по одному описанию операции за раз.
    """
    for transaction in transactions:
        description = transaction.get("description")
        if description:
            yield description


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """
    Генератор, возвращающий последовательность номеров карт
    Каждый номер форматируется в виде XXXX XXXX XXXX XXXX.
    """
    for number in range(start, stop + 1):
        yield f"{number:016d}"[:4] + " " + f"{number:016d}"[4:8] + " " + f"{number:016d}"[8:12] + " " + f"{number:016d}"[12:]


# get_transactions = [
#     {"date": "2022-05-20", "description": "Перевод организации", "amount": 1000},
#     {"date": "2022-06-01", "description": "Оплата услуг", "amount": 200},
#     {"date": "2022-07-15", "description": "Покупка продуктов", "amount": 300},
# ]
#

# for desc in transaction_descriptions(get_transactions):
#     print(desc)
#
#
# for card in card_number_generator(1, 5):
#     print(card)
