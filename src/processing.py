from typing import List, Dict


def filter_by_state(date: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """
    Функция фильтрует список словарей по параметру 'state'.
    state = 'EXECUTED' по умолчанию.
    Функция возвращает отфильтрованный список
    """
    return [item for item in date if item.get("state") == state]





