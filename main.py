"""
Главный скрипт для запуска программы.
"""

from typing import Any, Dict, List

from src.financial_transactions import read_transactions_csv, read_transactions_excel
from src.processing import filter_by_state, filter_rub_only, get_amount, get_currency_code, sort_by_date
from src.search import process_bank_search
from src.utils import read_json


def choose_file_source() -> List[Dict[str, Any]]:
    """
    Запрашивает у пользователя формат входных данных (JSON/CSV/XLSX)
    и возвращает список транзакций.
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
            return read_transactions_csv("data/transactions.csv")
        elif choice == "3":
            print("Для обработки выбран XLSX-файл.")
            return read_transactions_excel("data/transactions_excel.xlsx")
        else:
            print("Введите корректный пункт меню (1, 2 или 3).")


def choose_status() -> str:
    """
    Запрашивает статус транзакций от пользователя.
    """
    valid_statuses = {"EXECUTED", "CANCELED", "PENDING"}

    while True:
        print("Введите статус для фильтрации.")
        print("Доступные статусы: EXECUTED, CANCELED, PENDING")
        status = input("Статус: ").strip().upper()

        if status in valid_statuses:
            print(f'Операции отфильтрованы по статусу "{status}".')
            return status

        print(f'Статус операции "{status}" недоступен.')


def choose_sorting() -> bool | None:
    """
    Запрашивает необходимость сортировки и направление.
    """
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


def format_transaction(transaction: Dict[str, Any]) -> str:
    """
    Форматирует транзакцию для вывода.
    """
    date = transaction.get("date", "—")
    description = transaction.get("description", "—")

    from_acc = transaction.get("from", "")
    to_acc = transaction.get("to", "")

    amount = get_amount(transaction)
    currency = get_currency_code(transaction)

    amount_text = f"{amount} {currency}" if amount and currency else "— —"

    lines = [
        f"{date} {description}",
        f"{from_acc} -> {to_acc}" if from_acc or to_acc else "",
        f"Сумма: {amount_text}",
        "",
    ]

    return "\n".join(line for line in lines if line)


def main() -> None:
    """
    Основная функция программы.
    """
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

    # Сортировка по дате
    sorting = choose_sorting()
    if sorting is not None:
        data = sort_by_date(data, reverse=sorting)

    # Фильтрация по рублям
    only_rub = input("Выводить только рублевые транзакции? (Да/Нет): ").strip().lower()
    if only_rub == "да":
        data = filter_rub_only(data)

    search_choice = (
        input("Отфильтровать список транзакций по определенному слову в описании? (Да/Нет): ").strip().lower()
    )

    if search_choice == "да":
        keyword = input("Введите слово для поиска: ").strip()
        data = process_bank_search(data, keyword)

    # Итоговый вывод
    if not data:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    print("\nРаспечатываю итоговый список транзакций...")
    print(f"\nВсего банковских операций в выборке: {len(data)}\n")

    for transaction in data:
        print(format_transaction(transaction))


if __name__ == "__main__":
    main()
