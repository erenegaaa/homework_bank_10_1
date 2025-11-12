from pathlib import Path

import pandas as pd
import pytest

from src.financial_transactions import read_transactions_csv, read_transactions_excel


@pytest.fixture
def sample_csv(tmp_path: Path) -> str:
    """Создаёт временный CSV-файл с тестовыми данными."""
    file = tmp_path / "transactions.csv"
    file.write_text(
        "id;state;date;amount;currency_name;currency_code;from;to;description\n"
        "1;EXECUTED;2023-01-01T00:00:00Z;1000;Euro;EUR;Счет 1;Счет 2;Перевод\n",
        encoding="utf-8",
    )
    return str(file)


@pytest.fixture
def sample_excel(tmp_path: Path) -> str:
    """Создаёт временный Excel-файл с тестовыми данными."""
    df = pd.DataFrame(
        [
            {
                "id": 1,
                "state": "EXECUTED",
                "date": "2023-01-01T00:00:00Z",
                "amount": 1000,
                "currency_name": "Euro",
                "currency_code": "EUR",
                "from": "Счет 1",
                "to": "Счет 2",
                "description": "Перевод",
            }
        ]
    )
    file = tmp_path / "transactions_excel.xlsx"
    df.to_excel(file, index=False)
    return str(file)


def test_read_transactions_csv(sample_csv: str) -> None:
    result = read_transactions_csv(sample_csv)
    assert isinstance(result, list)
    assert result[0]["amount"] == 1000
    assert result[0]["currency_code"] == "EUR"


def test_read_transactions_excel(sample_excel: str) -> None:
    result = read_transactions_excel(sample_excel)
    assert isinstance(result, list)
    assert result[0]["currency_name"] == "Euro"
    assert result[0]["to"] == "Счет 2"
