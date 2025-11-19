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
    Фильтрует только рублевые операции по валюте (RUB).
    Работает с JSON, CSV, XLSX форматами.
    """

    result: List[Dict[str, Any]] = []

    for op in data:
        currency_code: Optional[str] = None
        if isinstance(op.get("currency_code"), str):
            currency_code = op["currency_code"]
        if currency_code is None and "operationAmount" in op:
            currency_data = op["operationAmount"].get("currency")
            if isinstance(currency_data, dict):
                code = currency_data.get("code")
                if isinstance(code, str):
                    currency_code = code
        if currency_code is None and isinstance(op.get("currency"), str):
            currency_code = op["currency"]
        if currency_code is None and isinstance(op.get("currency"), dict):
            code = op["currency"].get("code")
            if isinstance(code, str):
                currency_code = code
        if isinstance(currency_code, str) and currency_code.upper() == "RUB":
            result.append(op)
    return result


def get_amount(transaction: dict) -> float | None:
    """Возвращает сумму из JSON/CSV/XLSX."""
    if "amount" in transaction:
        return float(transaction["amount"])

    if "operationAmount" in transaction:
        amount = transaction["operationAmount"].get("amount")
        if amount is not None:
            return float(amount)
    return None


def get_currency_code(transaction: dict) -> str | None:
    """Возвращает код валюты из JSON/CSV/XLSX."""

    if "currency_code" in transaction:
        code = transaction["currency_code"]
        return str(code) if code is not None else None

    if "operationAmount" in transaction:
        currency = transaction["operationAmount"].get("currency")
        if isinstance(currency, dict):
            code = currency.get("code")
            return str(code) if code is not None else None

    return None
