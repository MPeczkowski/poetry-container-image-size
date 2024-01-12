import datetime
import json


def test_get_items(get_client, get_todo_item):
    get_client.app.todos = {
        "foo": [
            get_todo_item,
            get_todo_item,
        ]
    }

    result = get_client.get("/lists/foo")
    assert result.status_code == 200
    assert result.json() == [
        {**json.loads(get_todo_item.model_dump_json()), "id": 0},
        {**json.loads(get_todo_item.model_dump_json()), "id": 1},
    ]


def test_get_items_when_list_not_exists(get_client):
    result = get_client.get("/lists/foo")
    assert result.status_code == 404


def test_put_new_item_to_todo_list(get_client):
    get_client.app.todos = {"foo": []}

    result = get_client.put(
        "/lists/foo", json={"name": "Test", "description": "Test", "priority": 2}
    )

    assert result.status_code == 201
    data = result.json()
    assert data["name"] == "Test"
    assert data["description"] == "Test"
    assert data["priority"] == 2
    assert data["creation_time"] != data["update_time"]
    assert datetime.datetime.fromisoformat(
        data["creation_time"]
    ) - datetime.datetime.now() < datetime.timedelta(minutes=1)


def test_put_new_when_list_does_not_exist(get_client):
    result = get_client.put(
        "/lists/foo", json={"name": "Test", "description": "Test", "priority": 2}
    )
    assert result.status_code == 404


def test_update_new_item(get_client, get_todo_item):
    get_client.app.todos = {
        "foo": [
            get_todo_item,
        ]
    }
    result = get_client.post("/lists/foo", json={"id": 0, "done": True})
    assert result.status_code == 200
    data = result.json()
    assert data["done"]
    assert data["name"] == get_todo_item.name
    assert data["update_time"] != str(get_todo_item.update_time)


def test_update_new_item_when_list_does_not_exist(get_client):
    result = get_client.post("/lists/foo", json={"id": 0, "done": True})
    assert result.status_code == 404


def test_update_new_item_when_item_does_not_exist(get_client):
    get_client.app.todos = {"foo": []}
    result = get_client.post("/lists/foo", json={"id": 0, "done": True})
    assert result.status_code == 404


def test_delete_item(get_client, get_todo_item):
    get_client.app.todos = {
        "foo": [
            get_todo_item,
        ]
    }
    result = get_client.request(
        "DELETE",
        "/lists/foo",
        json={
            "id": 0,
        },
    )
    assert result.status_code == 204
    assert len(get_client.app.todos["foo"]) == 0


def test_delete_item_when_list_does_not_exist(get_client, get_todo_item):
    result = get_client.request(
        "DELETE",
        "/lists/foo",
        json={
            "id": 0,
        },
    )
    assert result.status_code == 404
    assert result.json() == {"detail": "Given list doesn't exists"}


def test_delete_item_when_item_does_not_exist(get_client, get_todo_item):
    get_client.app.todos = {"foo": []}
    result = get_client.request(
        "DELETE",
        "/lists/foo",
        json={
            "id": 0,
        },
    )
    assert result.status_code == 404
    assert result.json() == {"detail": "Given item doesn't exists"}
