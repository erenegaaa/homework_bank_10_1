import logging
from pathlib import Path
from typing import Iterator

import pytest

from src.masks import get_mask_account, get_mask_card_number, logger


@pytest.fixture
def temp_log_file(tmp_path: Path) -> Iterator[Path]:
    """Подменяет FileHandler для логгера src.masks на временный."""
    log_path = tmp_path / "masks_test.log"

    old_handlers = list(logger.handlers)
    for h in old_handlers:
        logger.removeHandler(h)

    file_handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    fmt = logging.Formatter("%(levelname)s - %(message)s")
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    yield log_path

    try:
        file_handler.flush()
        file_handler.close()
    except OSError:
        pass

    for h in list(logger.handlers):
        logger.removeHandler(h)
    for h in old_handlers:
        logger.addHandler(h)


def _read_log_text(path: Path) -> str:
    """Прочитать содержимое временного лога."""
    return path.read_text(encoding="utf-8") if path.exists() else ""


@pytest.mark.parametrize(
    ("card_number", "expected"),
    [
        ("1234567812345678", "1234 56** **** 5678"),
        ("1111222233334444", "1111 22** **** 4444"),
    ],
)
def test_get_mask_card_number_valid(card_number: str, expected: str, temp_log_file: Path) -> None:
    result = get_mask_card_number(card_number)
    assert result == expected

    for h in logger.handlers:
        if isinstance(h, logging.FileHandler):
            h.flush()

    log = _read_log_text(temp_log_file).lower()
    assert "debug" in log
    assert "замаскирован" in log


@pytest.mark.parametrize(
    "invalid_card",
    ["1234", "12345678901234567", "", "abcdabcdabcdabcd", "12 34abcd56"],
)
def test_get_mask_card_number_invalid_log(invalid_card: str, temp_log_file: Path) -> None:
    with pytest.raises(ValueError):
        get_mask_card_number(invalid_card)

    for h in logger.handlers:
        if isinstance(h, logging.FileHandler):
            h.flush()

    log = _read_log_text(temp_log_file).lower()
    assert "error" in log
    assert ("символ" in log) or ("длина" in log)


@pytest.mark.parametrize(
    ("account_number", "expected"),
    [
        ("123456789", "**6789"),
        ("00001234", "**1234"),
        ("9876", "**9876"),
        (123456, "**3456"),  # int → проверяем преобразование в строку
    ],
)
def test_get_mask_account_valid(account_number: str, expected: str, temp_log_file: Path) -> None:
    result = get_mask_account(account_number)
    assert result == expected

    for h in logger.handlers:
        if isinstance(h, logging.FileHandler):
            h.flush()

    log = _read_log_text(temp_log_file).lower()
    assert "debug" in log
    assert "замаскирован" in log


@pytest.mark.parametrize("invalid_account", ["12", "", "  "])
def test_get_mask_account_invalid_log(invalid_account: str, temp_log_file: Path) -> None:
    with pytest.raises(ValueError):
        get_mask_account(invalid_account)

    for h in logger.handlers:
        if isinstance(h, logging.FileHandler):
            h.flush()

    log = _read_log_text(temp_log_file).lower()
    assert "error" in log
    assert ("короткий" in log) or ("минимум" in log)
