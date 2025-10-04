from typing import Union


def get_mask_card_number(number_card: Union[str]) -> str:
    """
    Маскирует номер карты. Функция принимает на вход номер карты,
    которая в процессе должна вывести номер карты с маской.
    XXXX XX12** **** XXXX
    """
    str_number = str(number_card).replace(" ", "")
    if len(str_number) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр!")
    return f"{str_number[:4]} {str_number[4:6]}** **** {str_number[-4:]}"


def get_mask_account(number_account: Union[str]) -> str:
    """
    Маскирует номер счёта. Функция принимает на вход номер счёта,
    которая в процессе должна вывести номер счёта с маской.
    **XXXX
    """
    str_account = str(number_account).replace(" ", "")
    if len(str_account) < 4:
        raise ValueError("Номер счёта должен содержать минимум 4 цифры")
    return f"**{str_account[-4:]}"
