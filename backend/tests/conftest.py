from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app import database
from app.main import create_app


@pytest.fixture()
def client(tmp_path) -> Generator[TestClient, None, None]:
    database_path = tmp_path / "test.db"
    database.configure_database(f"sqlite:///{database_path}")

    app = create_app()

    with TestClient(app) as test_client:
        yield test_client

    database.Base.metadata.drop_all(bind=database.engine)
