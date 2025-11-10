import logging
import os
from typing import Union

# Настройка логирования для masks
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "masks.log")

os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("src.masks")
logger.setLevel(logging.DEBUG)

if not any(isinstance(h, logging.FileHandler) and getattr(h, "baseFilename", "") == LOG_FILE for h in logger.handlers):
    file_handler = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def get_mask_card_number(number_card: Union[str]) -> str:
    """
    Маскирует номер карты. Функция принимает на вход номер карты,
    которая в процессе должна вывести номер карты с маской.
    XXXX XX12** **** XXXX
    """
    str_number = str(number_card).replace(" ", "")

    if not str_number.isdigit():
        logger.error("Номер карты содержит недопустимые символы")
        raise ValueError("Номер карты должен состоять только из цифр!")

    if len(str_number) != 16:
        logger.error("Длина номера карты некорректна")
        raise ValueError("Номер карты должен содержать 16 цифр!")

    masked = f"{str_number[:4]} {str_number[4:6]}** **** {str_number[-4:]}"
    logger.debug(f"Номер карты успешно замаскирован: {masked}")
    return masked


def get_mask_account(number_account: Union[str]) -> str:
    """
    Маскирует номер счёта. Функция принимает на вход номер счёта,
    которая в процессе должна вывести номер счёта с маской.
    **XXXX
    """
    str_account = str(number_account).replace(" ", "")
    if len(str_account) < 4:
        logger.error("Номер счёта слишком короткий")
        raise ValueError("Номер счёта должен содержать минимум 4 цифры")

    masked = f"**{str_account[-4:]}"
    logger.debug(f"Номер счёта успешно замаскирован: {masked}")
    return masked
