import re
from collections import Counter
from typing import Dict, List


def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """
    Ищет операции, в чьём description встречается поисковая строка.
    Args:
        data: список словарей транзакций.
        search: строка поиска.
    Returns:
        Список словарей с совпадениями.
    """

    if not search:
        return []

    pattern = re.compile(re.escape(search), re.IGNORECASE)

    return [item for item in data if pattern.search(item.get("description", ""))]


def process_bank_operations(data: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по категориям (по полю description).
    Args:
        data: список транзакций.
        categories: список категорий для подсчёта.
    Returns:
        Словарь {категория: количество}.
    """

    counter = Counter()

    for item in data:
        desc = item.get("description", "").lower()
        for cat in categories:
            if cat.lower() in desc:
                counter[cat] += 1

    return dict(counter)
