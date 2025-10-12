import pytest
from src.decorators import log


def test_log_to_console_success(capsys) -> None:
    """Проверяет успешный вызов и вывод в консоль"""
    @log()
    def add(a: int, b: int) -> int:
        return a + b

    add(1, 2)
    captured = capsys.readouterr()
    assert "add ok" in captured.out


def test_log_to_console_error(capsys) -> None:
    """Проверяет логирование ошибки в консоль"""
    @log()
    def div(a: int, b: int) -> float:
        return a / b

    with pytest.raises(ZeroDivisionError):
        div(1, 0)

    captured = capsys.readouterr()
    assert "div error" in captured.out
    assert "ZeroDivisionError" in captured.out


def test_log_to_file(tmp_path) -> None:
    """Проверяет запись логов в файл"""
    log_file = tmp_path / "test_log.txt"

    @log(filename=str(log_file))
    def mul(a: int, b: int) -> int:
        return a * b

    mul(3, 4)
    text = log_file.read_text(encoding="utf-8")
    assert "mul ok" in text

def test_log_to_file_error(tmp_path) -> None:
    """Проверяет логирование ошибки в файл"""
    log_file = tmp_path / "error_log.txt"

    @log(filename=str(log_file))
    def div(a: int, b: int) -> float:
        return a / b

    with pytest.raises(ZeroDivisionError):
        div(10, 0)

    text = log_file.read_text(encoding="utf-8")
    assert "div error" in text
    assert "ZeroDivisionError" in text
