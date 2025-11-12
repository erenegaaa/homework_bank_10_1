from typing import Any, Hashable

import pandas as pd


def read_transactions_csv(file_path: str) -> list[dict[Hashable, Any]]:
    """
    Считывает финансовые операции из CSV-файла и возвращает список словарей.
    file_path: путь к CSV-файлу.
    список словарей с транзакциями.
    """
    df = pd.read_csv(file_path, sep=";", encoding="utf-8")
    return df.to_dict(orient="records")


def read_transactions_excel(file_path: str) -> list[dict[Hashable, Any]]:
    """
    Считывает финансовые операции из Excel-файла и возвращает список словарей.
    file_path: путь к Excel-файлу (.xlsx)
    список словарей с транзакциями.
    """
    df = pd.read_excel(file_path)
    return df.to_dict(orient="records")
