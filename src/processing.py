from typing import Dict, List, Optional


def filter_by_state(operations: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """
    Функция фильтрует список словарей по параметру 'state'.
    state = 'EXECUTED' по умолчанию.
    Функция возвращает отфильтрованный список.
    """
    return [operation for operation in operations if operation.get("state") == state]


# data = [
#     {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
#     {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
#     {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
#     {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
#     ]
# print(filter_by_state(data))


def sort_by_date(sort_operations: List[Dict], date_key: Optional[str] = "date", reverse: bool = True) -> List[Dict]:
    """
    Функция сортирует список словарей по параметру 'date' на убывание.
    Условие функции: параметр 'reverse' = True.
    Возвращает отсортированный список по дате.
    """
    return sorted(sort_operations, key=lambda operation: operation.get(date_key) or "", reverse=reverse)


# data = [
#     {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
#     {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
#     {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
#     {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
#     ]
# print(sort_by_date(data))
