import json
from typing import Any


def read_json(file_path: str) -> list[dict[str, Any]]:
    """
    Читает JSON-файл и возвращает список словарей с данными о транзакциях.
    Если файл пустой, не найден или содержит не список — возвращает пустой список.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            return []
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []
