def test_create_new_list(get_client):
    result = get_client.put("/lists", json={"name": "foo"})

    assert result.status_code == 201
    assert len(get_client.app.todos) == 1
    assert "foo" in get_client.app.todos.keys()
    assert result.json() == {"foo": []}


def test_add_list_with_duplicated_name(get_client):
    get_client.app.todos = {"foo": []}
    result = get_client.put("/lists", json={"name": "foo"})

    assert result.status_code == 409


def test_get_all_items(get_client):
    get_client.app.todos = {"foo": {}, "bar": {}}

    result = get_client.get("/lists")
    assert result.status_code == 200
    assert result.json() == ["foo", "bar"]


def test_update_list(get_client):
    get_client.app.todos = {
        "foo": [],
    }

    result = get_client.post("/lists", json={"old": "foo", "new": "bar"})
    assert result.status_code == 200
    assert "bar" in get_client.app.todos.keys()
    assert len(get_client.app.todos.keys()) == 1
    assert result.json() == {"bar": []}


def test_update_list_when_name_is_the_same(get_client):
    get_client.app.todos = {"foo": []}

    result = get_client.post("/lists", json={"old": "foo", "new": "foo"})
    assert result.status_code == 400


def test_update_list_when_list_with_given_name_exists(get_client):
    get_client.app.todos = {"foo": [], "bar": []}

    result = get_client.post("/lists", json={"old": "foo", "new": "bar"})
    assert result.status_code == 409


def test_delete_list(get_client):
    get_client.app.todos = {
        "foo": {},
    }
    result = get_client.request("DELETE", "/lists", json={"name": "foo"})
    assert result.status_code == 204
    assert len(get_client.app.todos.keys()) == 0


def test_delete_list_when_list_does_not_exist(get_client):
    get_client.app.todos = {}
    result = get_client.request("DELETE", "/lists", json={"name": "foo"})
    assert result.status_code == 404
