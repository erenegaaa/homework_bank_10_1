"""
Главный скрипт для запуска программы.
"""

from src.masks import get_mask_account, get_mask_card_number
from src.widget import mask_account_card, get_date


def main() -> None:
    """Основная функция."""
    print("Банковский виджет - маскировка данных")

    try:
        card = input("Введите наименование и номер карты: ")
        print(mask_account_card(card))

        account = input("Введите номер счёта: ")
        print(get_mask_account(account))

        banking_transaction = input("Введите дату операции: ")
        print(get_date(date))

    except ValueError as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
