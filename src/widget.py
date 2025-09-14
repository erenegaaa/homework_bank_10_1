import re


def mask_account_card(account_number: str) -> str:
    """Функция, обрабатывающая тип карты или счета"""
    # Убираем все лишние символы кроме цифр
    text = re.sub(r"[^а-яА-Яa-zA-Z\s]", '', account_number, flags=re.UNICODE)
    # Убираем все лишние символы кроме букв
    digins = re.sub(r"\D", "", account_number)

    # Проверка схожих символов для подставки типа операции
    if re.search(r'[а-яА-Я]', account_number):
        return str(text + masks.get_mask_card_number(int(digins)))


# def get_date(new_date: str) -> str:
#   """Функция меняет формат даты"""
#    # срезами меняем формат даты
#   return f"{new_date[8:10]} {new_date[5:7]} {new_date[:4]}"
