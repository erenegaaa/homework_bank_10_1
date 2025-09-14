import re
from datetime import datetime


def mask_account_card(account_number: str) -> str:
    """Функция, обрабатывающая тип карты или счета"""
    # проверка на тип данных
    if not isinstance(account_number, str):
        raise ValueError("Нужно ввести строку")

    # Убираем все буквы
    text = re.sub(r"[^а-яА-ЯёЁa-zA-Z\s]", "", account_number, flags=re.UNICODE).strip()
    text = re.sub(r"\s+", " ", text)

    # Убираем все цифры
    digins = re.sub(r"\D", "", account_number)

    if not digins:
        raise ValueError("Не найден номер карты или счета")

    # Обработка запроса счета
    if text.lower().startswith("счет") or text.lower().startswith("счёт"):
        return f"{text}: **{digins[-4:]}"
    # Обработка запроса номера карты
    if len(digins) == 16:
        text_display = text if text else "Карта"
        return f"{text_display}: {digins[:4]} {digins[4:6]}** **** {digins[-4:]}"

    raise (ValueError(
        "Не верно введены данные: ожидается формат (тип карты и 16 цифр или пометка 'счет' и номер)"
    ))


def get_date(date_str: str) -> str:
    """Функция меняет формат даты"""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
        # Задаем формат даты
        return dt.strftime("%d.%m.%Y")
    except ValueError:
        raise ValueError("Неверный формат даты")
