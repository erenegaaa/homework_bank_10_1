import json
from src.utils import read_json


def test_read_json_valid(tmp_path) -> None:
    """Тест корректного чтения JSON"""
    test_file = tmp_path / "data.json"
    data = [{"id": 1, "state": "EXECUTED"}]
    test_file.write_text(json.dumps(data), encoding="utf-8")
    assert read_json(str(test_file)) == data


def test_read_json_not_found() -> None:
    """Тест для отсутствующего файла"""
    assert read_json("non_existing.json") == []


def test_read_json_invalid_json(tmp_path) -> None:
    """Тест для битого JSON"""
    test_file = tmp_path / "invalid.json"
    test_file.write_text("{invalid_json}", encoding="utf-8")
    assert read_json(str(test_file)) == []


def test_read_json_not_list(tmp_path) -> None:
    """Тест для JSON, не содержащего список"""
    test_file = tmp_path / "data.json"
    test_file.write_text(json.dumps({"id": 1}), encoding="utf-8")
    assert read_json(str(test_file)) == []

