from __future__ import annotations

import re
from datetime import datetime
from typing import Any, Dict, List, Optional

from src.financial_transactions import read_transactions_csv, read_transactions_excel
from src.processing import filter_by_state, filter_rub_only, get_amount, get_currency_code, sort_by_date
from src.search import process_bank_search
from src.utils import read_json


def format_date(date_str: str) -> str:
    """Преобразует ISO8601 в DD.MM.YYYY."""
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00")).strftime("%d.%m.%Y")
    except Exception:
        return date_str


def get_mask_card_number(card: str) -> str:
    """XXXX XX** **** 1234"""
    digits = re.sub(r"\D", "", card)
    if len(digits) != 16:
        raise ValueError("not a 16-digit card")
    return f"{digits[:4]} {digits[4:6]}** **** {digits[-4:]}"


def get_mask_account(account: str) -> str:
    """**1234"""
    digits = re.sub(r"\D", "", account)
    if len(digits) < 4:
        raise ValueError("invalid account")
    return "**" + digits[-4:]


def _mask_card_in_text(text: str) -> str:
    def repl(match: re.Match) -> str:
        digits = re.sub(r"\D", "", match.group(0))
        try:
            return get_mask_card_number(digits)
        except ValueError:
            return match.group(0)  # type: ignore

    return re.sub(r"(?:\d[ -]?){16}", repl, text)


def _mask_accounts_in_text(text: str) -> str:
    def repl(match: re.Match) -> str:
        digits = re.sub(r"\D", "", match.group(1))
        try:
            return "Счет " + get_mask_account(digits)
        except ValueError:
            return match.group(0)  # type: ignore

    return re.sub(r"(?i)\bСчет\s*([0-9\s]{4,})", repl, text)


def format_accounts(transaction: Dict[str, Any]) -> str:
    from_acc = transaction.get("from", "")
    to_acc = transaction.get("to", "")

    def mask(value: Any) -> str:
        if not value:
            return ""
        s = str(value)
        s = _mask_accounts_in_text(s)
        s = _mask_card_in_text(s)
        return s

    fm = mask(from_acc)
    tm = mask(to_acc)

    if fm and tm:
        return f"{fm} -> {tm}"
    if fm:
        return f"{fm} ->"
    if tm:
        return f"-> {tm}"
    return ""


def format_transaction(transaction: Dict[str, Any]) -> str:
    date_txt = format_date(transaction.get("date", "—"))
    description = transaction.get("description", "—")

    amount = get_amount(transaction)
    currency = get_currency_code(transaction)

    amount_text = f"{amount} {currency}" if amount is not None and currency else "— —"

    accounts_line = format_accounts(transaction)

    lines = [
        f"{date_txt} {description}",
        accounts_line if accounts_line else "",
        f"Сумма: {amount_text}",
        "",
    ]

    return "\n".join(line for line in lines if line)


def choose_file_source() -> List[Dict[str, Any]]:
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию из JSON")
    print("2. Получить информацию из CSV")
    print("3. Получить информацию из XLSX")

    while True:
        choice = input("Ваш выбор: ").strip()

        if choice == "1":
            print("Формат JSON выбран.")
            return read_json("data/operations.json")

        elif choice == "2":
            print("Формат CSV выбран.")
            data = read_transactions_csv("data/transactions.csv")
            return [{str(k): v for k, v in row.items()} for row in data]

        elif choice == "3":
            print("Формат XLSX выбран.")
            data = read_transactions_excel("data/transactions_excel.xlsx")
            return [{str(k): v for k, v in row.items()} for row in data]

        print("Введите 1, 2 или 3.")


def choose_status() -> str:
    valid = {"EXECUTED", "CANCELED", "PENDING"}

    while True:
        print("Введите статус EXECUTED CANCELED PENDING")
        status = input("Ваш выбор: ").strip().upper()
        if status in valid:
            print(f'Фильтрация по статусу "{status}".')
            return status
        print("Некорректный статус.")


def choose_sorting() -> Optional[bool]:
    ans = input("Отсортировать по дате? (Да/Нет): ").strip().lower()

    if ans != "да":
        return None

    while True:
        d = input("По возрастанию или по убыванию? ").strip().lower()
        if d.startswith("по возрастанию"):
            return False
        if d.startswith("по убыванию"):
            return True
        print("Введите корректный вариант.")


def main() -> None:
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    data = choose_file_source()
    if not data:
        print("Нет данных.")
        return

    status = choose_status()
    data = filter_by_state(data, status)

    if not data:
        print("Нет данных после фильтрации.")
        return

    sorting = choose_sorting()
    if sorting is not None:
        data = sort_by_date(data, reverse=sorting)

    only_rub = input("Только рублевые? (Да/Нет): ").strip().lower()
    if only_rub == "да":
        data = filter_rub_only(data)

    search = input("Фильтровать по слову из описания? (Да/Нет): ").strip().lower()
    if search == "да":
        keyword = input("Введите слово: ").strip()
        data = process_bank_search(data, keyword)

    if not data:
        print("Нет транзакций после всех фильтров.")
        return

    print("\nРаспечатываю итоговый список транзакций...")
    print(f"\nВсего банковских операций: {len(data)}\n")

    for t in data:
        print(format_transaction(t))


if __name__ == "__main__":
    main()
