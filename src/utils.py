import json
import logging
import os
from typing import Any

# Путь к корню проекта
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "utils.log")


os.makedirs(LOG_DIR, exist_ok=True)

# Настройка логера для модуля utils
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


if not any(isinstance(h, logging.FileHandler) and getattr(h, "baseFilename", "") == LOG_FILE for h in logger.handlers):
    file_handler = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8")
    file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


def read_json(file_path: str) -> list[dict[str, Any]]:
    """
    Читает JSON-файл и возвращает список словарей с данными о транзакциях.
    Если файл пустой, не найден или содержит не список — возвращает пустой список.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            logger.error(f"Файл {file_path} не содержит список JSON")
            return []

        logger.debug(f"Файл {file_path} успешно прочитан")
        return data

    except FileNotFoundError:
        logger.error(f"Файл {file_path} не найден")
        return []

    except json.JSONDecodeError:
        logger.error(f"Ошибка декодирования JSON в файле {file_path}")
        return []
