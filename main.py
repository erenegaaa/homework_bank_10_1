"""
Главный скрипт для запуска программы.
"""

from src.masks import get_mask_account, get_mask_card_number
from src.widget import mask_account_card


def main() -> None:
    """Функция управления и вывода"""
    print("Банковский виджет - маскировка данных")
    card = input("Введите наименование и номер карты: ")
    account = input("Введите номер счёта: ")

    try:
        print(mask_account_card(card))
        print(get_mask_account(account))
    except ValueError as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
