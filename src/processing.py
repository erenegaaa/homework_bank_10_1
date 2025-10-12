from typing import Dict, List, Optional


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
