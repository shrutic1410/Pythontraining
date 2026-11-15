import json

import pytest
from fastapi.testclient import TestClient

from src import main


@pytest.fixture
def client(tmp_path, monkeypatch):
    data_file = tmp_path / "employees.json"
    data_file.write_text(
        json.dumps([{"name": "Aarav", "salary": 55000}]),
        encoding="utf-8",
    )
    monkeypatch.setattr(main, "EMPLOYEES_FILE", data_file)
    return TestClient(main.app)
