from typing import Any, Dict, List, Optional


def filter_by_state(operations: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """
    Функция фильтрует список словарей по параметру 'state'.
    state = 'EXECUTED' по умолчанию.
    Функция возвращает отфильтрованный список.
    """
    return [operation for operation in operations if operation.get("state") == state]


def sort_by_date(sort_operations: List[Dict], date_key: Optional[str] = "date", reverse: bool = True) -> List[Dict]:
    """
    Функция сортирует список словарей по параметру 'date' на убывание.
    Условие функции: параметр 'reverse' = True.
    Возвращает отсортированный список по дате.
    """
    return sorted(sort_operations, key=lambda operation: operation.get(date_key) or "", reverse=reverse)


def filter_rub_only(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Фильтрация по рублям
    """

    result = []

    for op in data:
        currency_code = None

        if "currency_code" in op:
            currency_code = op.get("currency_code")

        if not currency_code and "operationAmount" in op:
            currency_data = op["operationAmount"].get("currency")
            if isinstance(currency_data, dict):
                currency_code = currency_data.get("code")

        if not currency_code and isinstance(op.get("currency"), str):
            currency_code = op.get("currency")

        if not currency_code and isinstance(op.get("currency"), dict):
            currency_code = op["currency"].get("code")

        if isinstance(currency_code, str) and currency_code.upper() == "RUB":
            result.append(op)

    return result


def get_amount(transaction: dict) -> float | None:
    """Возвращает сумму из JSON/CSV/XLSX."""
    if "amount" in transaction:  # CSV/XLSX
        return transaction["amount"]

    if "operationAmount" in transaction:  # JSON
        return transaction["operationAmount"].get("amount")

    return None


def get_currency_code(transaction: dict) -> str | None:
    """Возвращает код валюты из JSON/CSV/XLSX."""
    if "currency_code" in transaction:  # CSV/XLSX
        return transaction["currency_code"]

    if "operationAmount" in transaction:  # JSON
        currency = transaction["operationAmount"].get("currency")
        if isinstance(currency, dict):
            return currency.get("code")

    return None
