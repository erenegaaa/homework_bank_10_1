import re
from datetime import datetime


def mask_account_card(account_number: str) -> str:
    """Функция, обрабатывающая тип карты или счета"""
    # проверка на тип данных
    if not isinstance(account_number, str):
        raise ValueError("Нужно ввести строку")

    # Убираем все кроме цифр
    digits = re.sub(r"\D", "", account_number)
    if not digits:
        raise ValueError("Не найден номер карты или счета")

    # Обработка запроса счета
    text = re.sub(r"\d", "", account_number).strip()
    if text.lower().startswith("счет") or text.lower().startswith("счёт"):
        return f"{text}: **{digits[-4:]}"

    # Обработка запроса номера карт
    if len(digits) == 16:
        text_display = text if text else "Карта"
        return f"{text_display}: {digits[:4]} {digits[4:6]}** **** {digits[-4:]}"

    raise ValueError(
        "Не верно введены данные: ожидается формат (тип карты и 16 цифр или пометка 'счет' и номер)"
    )


def get_date(date_str: str) -> str:
    """Функция меняет формат даты"""
    try:
        date_format = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
        # Задаем формат даты
        return date_format.strftime("%d.%m.%Y")
    except ValueError:
        raise ValueError("Неверный формат даты")
