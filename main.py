"""
Главный скрипт для запуска программы.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from src.financial_transactions import read_transactions_csv, read_transactions_excel
from src.processing import filter_by_state, filter_rub_only, get_amount, get_currency_code, sort_by_date
from src.search import process_bank_search
from src.utils import read_json


def format_date(date_str: str) -> str:
    """Преобразует дату из ISO в DD.MM.YYYY."""
    try:
        return datetime.fromisoformat(date_str).strftime("%d.%m.%Y")
    except Exception:
        return date_str


def format_accounts(transaction: dict) -> str:
    """Вывод отправителя и получателя."""
    from_acc = transaction.get("from")
    to_acc = transaction.get("to")

    if from_acc and to_acc:
        return f"{from_acc} -> {to_acc}"
    if from_acc and not to_acc:
        return f"{from_acc} ->"
    if not from_acc and to_acc:
        return f"-> {to_acc}"

    return ""


def format_transaction(transaction: Dict[str, Any]) -> str:
    """Форматирует транзакцию для вывода."""

    date_raw = transaction.get("date", "—")
    date_txt = format_date(date_raw)

    description = transaction.get("description", "—")

    amount = get_amount(transaction)
    currency = get_currency_code(transaction)

    if amount is not None and currency:
        amount_text = f"{amount} {currency}"
    else:
        amount_text = "— —"

    accounts_line = format_accounts(transaction)

    lines = [
        f"{date_txt} {description}",
        accounts_line if accounts_line else "",
        f"Сумма: {amount_text}",
        "",
    ]

    return "\n".join(line for line in lines if line)


def choose_file_source() -> List[Dict[str, Any]]:
    """
    Запрашивает у пользователя формат входных данных JSON/CSV/XLSX
    """
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    while True:
        choice = input("Ваш выбор: ").strip()
        if choice == "1":
            print("Для обработки выбран JSON-файл.")
            return read_json("data/operations.json")
        elif choice == "2":
            print("Для обработки выбран CSV-файл.")
            data = read_transactions_csv("data/transactions.csv")
            return [{str(k): v for k, v in item.items()} for item in data]
        elif choice == "3":
            print("Для обработки выбран XLSX-файл.")
            data = read_transactions_excel("data/transactions_excel.xlsx")
            return [{str(k): v for k, v in item.items()} for item in data]
        else:
            print("Введите корректный пункт меню (1, 2 или 3).")


def choose_status() -> str:
    """Выбор статуса транзакций."""

    valid_statuses = {"EXECUTED", "CANCELED", "PENDING"}

    while True:
        print("Введите статус для фильтрации.")
        print("Доступные статусы: EXECUTED, CANCELED, PENDING")
        status = input("Статус: ").strip().upper()

        if status in valid_statuses:
            print(f'Операции отфильтрованы по статусу "{status}".')
            return status

        print(f'Статус операции "{status}" недоступен.')


def choose_sorting() -> Optional[bool]:
    """Запрашивает необходимость сортировки по дате."""
    choice = input("Отсортировать операции по дате? (Да/Нет): ").strip().lower()

    if choice not in ("да", "нет"):
        return None

    if choice == "нет":
        return None

    while True:
        direction = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
        if direction in ("по возрастанию", "возрастание"):
            return False
        if direction in ("по убыванию", "убывание"):
            return True
        print("Введите корректный вариант.")


def main() -> None:
    """Основная функция программы."""

    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    data = choose_file_source()
    if not data:
        print("Файл пустой или не содержит корректных данных.")
        return

    # Фильтрация по статусу
    status = choose_status()
    data = filter_by_state(data, status)

    if not data:
        print("Не найдено ни одной транзакции после фильтрации по статусу.")
        return

    # Сортировка
    sorting = choose_sorting()
    if sorting is not None:
        data = sort_by_date(data, reverse=sorting)

    # Фильтр RUB
    only_rub = input("Выводить только рублевые транзакции? (Да/Нет): ").strip().lower()
    if only_rub == "да":
        data = filter_rub_only(data)

    # Поиск
    search_choice = input(
        "Отфильтровать список транзакций по слову в описании? (Да/Нет): "
    ).strip().lower()

    if search_choice == "да":
        keyword = input("Введите слово: ").strip()
        data = process_bank_search(data, keyword)

    # Результат
    if not data:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    print("\nРаспечатываю итоговый список транзакций...")
    print(f"\nВсего банковских операций: {len(data)}\n")

    for transaction in data:
        print(format_transaction(transaction))


if __name__ == "__main__":
    main()
