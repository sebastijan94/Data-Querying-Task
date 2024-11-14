from unittest.mock import MagicMock
import pytest
from src.db import get_db
from src.main import app

@pytest.fixture
def mock_db():
    mock_db_instance = MagicMock()
    app.dependency_overrides[get_db] = lambda: mock_db_instance
    yield mock_db_instance
    app.dependency_overrides = {}
