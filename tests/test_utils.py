import json
import logging
from src.utils import LOG_FILE
from pathlib import Path
from typing import Iterator

import pytest
from src.utils import read_json


def test_read_json_valid(tmp_path: Path) -> None:
    """Тест корректного чтения JSON"""
    test_file = tmp_path / "data.json"
    data = [{"id": 1, "state": "EXECUTED"}]
    test_file.write_text(json.dumps(data), encoding="utf-8")

    assert read_json(str(test_file)) == data


def test_read_json_not_found() -> None:
    """Тест для отсутствующего файла"""
    assert read_json("non_existing.json") == []


def test_read_json_invalid_json(tmp_path: Path) -> None:
    """Тест для битого JSON"""
    test_file = tmp_path / "invalid.json"
    test_file.write_text("{invalid_json}", encoding="utf-8")
    assert read_json(str(test_file)) == []


def test_read_json_not_list(tmp_path: Path) -> None:
    """Тест для JSON, не содержащего список"""
    test_file = tmp_path / "data.json"
    test_file.write_text(json.dumps({"id": 1}), encoding="utf-8")
    assert read_json(str(test_file)) == []

LOGGER_NAME = "src.utils"


@pytest.fixture
def temp_log_handler(tmp_path: Path) -> Iterator[Path]:
    """
    Фикстура подменяет handlers логера src.utils на временный FileHandler.
    Возвращает путь к временному лог-файлу.
    """
    log_path = tmp_path / "utils.log"

    file_handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(LOGGER_NAME)
    try:
        for h in list(logger.handlers):
            logger.removeHandler(h)
        logger.addHandler(file_handler)
        logger.setLevel(logging.DEBUG)

        yield log_path
    finally:
        try:
            file_handler.flush()
            file_handler.close()
        except OSError as e:
            logger.warning(f"Не удалось закрыть временный лог-файл: {e}")

def _read_log_text(path: Path) -> str:
    """Удобный ридер лог-файла; ждёт данных и возвращает содержимое."""
    return path.read_text(encoding="utf-8")


def test_log_file_created_on_valid_read(temp_log_handler: Path, tmp_path: Path) -> None:
    """Проверяет, что при успешном чтении JSON пишется DEBUG лог"""
    test_file = tmp_path / "data.json"
    data = [{"id": 1}]
    test_file.write_text(json.dumps(data), encoding="utf-8")
    result = read_json(str(test_file))
    assert result == data

    for h in logging.getLogger(LOGGER_NAME).handlers:
        try:
            h.flush()
        except OSError:
            pass

    log_text = _read_log_text(temp_log_handler)
    assert "DEBUG" in log_text or "debug" in log_text.lower()
    assert "успешно" in log_text.lower()


def test_log_file_not_found(temp_log_handler: Path) -> None:
    """Проверяет, что при отсутствии файла пишется ERROR лог"""
    read_json("non_existing.json")
    for h in logging.getLogger(LOGGER_NAME).handlers:
        try:
            h.flush()
        except OSError:
            pass

    log_text = _read_log_text(temp_log_handler)
    assert "ERROR" in log_text or "error" in log_text.lower()
    assert "не найден" in log_text.lower()


def test_log_file_not_list(temp_log_handler: Path, tmp_path: Path) -> None:
    """Проверяет, что при JSON не являющемся списком пишется ERROR лог"""
    file_path = tmp_path / "data.json"
    file_path.write_text(json.dumps({"a": 1}), encoding="utf-8")
    read_json(str(file_path))

    for h in logging.getLogger(LOGGER_NAME).handlers:
        try:
            h.flush()
        except OSError:
            pass

    log_text = _read_log_text(temp_log_handler)
    assert "ERROR" in log_text or "error" in log_text.lower()
    assert "список" in log_text.lower()


def test_log_file_invalid_json(tmp_path: Path) -> None:
    """Проверяет, что при ошибке JSONDecodeError пишется ERROR лог"""
    bad_file = tmp_path / "broken.json"
    bad_file.write_text("{invalid_json}", encoding="utf-8")

    read_json(str(bad_file))

    logger = logging.getLogger("src.utils")
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            handler.flush()

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        log_text = f.read()

    assert "ERROR" in log_text or "error" in log_text.lower()
    assert "декодирован" in log_text.lower()


def _flush_logger() -> None:
    """Сбрасывает буферы всех FileHandler логера src.utils"""
    logger = logging.getLogger("src.utils")
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            handler.flush()


def test_read_json_invalid(tmp_path: Path) -> None:
    """Проверяет, что при некорректном JSON возвращается пустой список и пишется ERROR лог"""
    bad_file = tmp_path / "broken.json"
    bad_file.write_text("{invalid_json}", encoding="utf-8")

    result = read_json(str(bad_file))
    _flush_logger()

    assert result == []


    with open(LOG_FILE, "r", encoding="utf-8") as f:
        log_text = f.read()
    assert "ERROR" in log_text or "error" in log_text.lower()
    assert "декодирован" in log_text.lower()


def test_not_list_read_json(tmp_path: Path) -> None:
    """Проверяет, что если JSON есть, но это не список, возвращается пустой список и пишется ERROR лог"""
    not_list_file = tmp_path / "not_list.json"
    not_list_file.write_text(json.dumps({"a": 1}), encoding="utf-8")

    result = read_json(str(not_list_file))
    _flush_logger()

    assert result == []

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        log_text = f.read()
    assert "ERROR" in log_text or "error" in log_text.lower()
    assert "не содержит список" in log_text.lower()


def test_read_json_file_not_found(tmp_path: Path) -> None:
    """Проверяет, что при отсутствии файла возвращается пустой список и пишется ERROR лог"""
    missing_file = tmp_path / "nofile.json"

    result = read_json(str(missing_file))
    _flush_logger()

    assert result == []

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        log_text = f.read()
    assert "ERROR" in log_text or "error" in log_text.lower()
    assert "не найден" in log_text.lower()