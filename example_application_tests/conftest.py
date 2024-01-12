import datetime

import pytest
from fastapi.testclient import TestClient
from example_application.main import app
from example_application.schemas import TodoItem, Priority


@pytest.fixture
def get_app():
    app.todos = {}
    return app


@pytest.fixture
def get_client(get_app):
    return TestClient(get_app)


@pytest.fixture
def get_todo_item():
    return TodoItem(
        name="Test",
        description="Item to tests",
        prioirty=Priority.Non,
        done=False,
        creation_time=datetime.datetime(2023, 6, 1),
        update_time=datetime.datetime(2023, 6, 1),
    )
