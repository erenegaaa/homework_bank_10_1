"""
Главный скрипт для запуска программы.
"""

# from src.masks import get_mask_account, get_mask_card_number
from src.widget import mask_account_card,get_date


def main() -> None:
    """Функция управления и вывода"""
    print("Банковский виджет - маскировка данных")
    card = input("Введите наименование карты или счет и номер: ")
    enter_date = input("Введите дату в формате: '2024-03-11T02:26:18.671407': ")
    # account = input("Введите номер счёта: ")
    try:
        print(mask_account_card(card))
        print(get_date(enter_date))
    except ValueError as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
