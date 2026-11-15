import json
import shutil
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app import main


@pytest.fixture
def client(tmp_path, monkeypatch):
    data_file = tmp_path / "employees.json"
    shutil.copy(Path(main.__file__).parent / "data" / "employees.json", data_file)
    monkeypatch.setattr(main, "DATA_FILE", data_file)
    return TestClient(main.app)
