from typing import List, Dict, Generator

from fastapi import FastAPI, HTTPException, status
from example_application.schemas import (
    TodoListRequest,
    TodoListRenameRequest,
    TodoItemRequest,
    TodoItem,
    TodoItemModify,
    TodoItemList,
)

app = FastAPI(
    title="Todo APP",
)

app.todos = {}


def get_todo_items(todo_list_name: str):
    for item_id, todo_item in enumerate(app.todos[todo_list_name]):
        data = todo_item.model_dump()
        data.update({"id": item_id})
        yield data


@app.get("/lists")
def get_all_lists() -> List[str]:
    return list(app.todos.keys())


@app.put("/lists", status_code=status.HTTP_201_CREATED)
def create_new_list(new_list: TodoListRequest) -> Dict[str, List[TodoItem]]:
    if new_list.name in app.todos:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Todo list with given name exists",
        )
    app.todos[new_list.name] = []
    return {new_list.name: []}


@app.post("/lists")
def update_list_name(
    rename_list: TodoListRenameRequest,
) -> Dict[str, List[TodoItemList]]:
    if rename_list.old == rename_list.new:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New name, and old name must be different",
        )
    if rename_list.new in app.todos:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Todo list with given new name, already exist",
        )

    app.todos[rename_list.new] = app.todos[rename_list.old]
    del app.todos[rename_list.old]
    return {rename_list.new: get_todo_items(rename_list.new)}


@app.delete("/lists", status_code=status.HTTP_204_NO_CONTENT)
def remove_list(list_to_remove: TodoListRequest) -> None:
    try:
        del app.todos[list_to_remove.name]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo list with given name, doesn't exist",
        )
    return


@app.get("/lists/{todo_list_name}")
def get_tasks_from_todo_list(todo_list_name: str) -> List[TodoItemList]:
    try:
        return list(get_todo_items(todo_list_name))
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given list doesn't exists"
        )


@app.put("/lists/{todo_list_name}", status_code=status.HTTP_201_CREATED)
def add_new_todo_item_to_list(
    todo_list_name: str, todo_item_request: TodoItemRequest
) -> TodoItem:
    new_item: TodoItem = TodoItem(**todo_item_request.model_dump())

    try:
        app.todos[todo_list_name].append(new_item)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given list doesn't exists"
        )
    return new_item


@app.post("/lists/{todo_list_name}")
def modify_todo_item(todo_list_name: str, todo_item: TodoItemModify) -> TodoItem:
    try:
        current_item: dict = app.todos[todo_list_name][todo_item.id].model_dump()
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given list doesn't exists"
        )
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given item doesn't exists"
        )
    todo_item.name = todo_item.name if todo_item.name else current_item["name"]

    current_item.update(todo_item.model_dump())

    del current_item["id"]
    del current_item["update_time"]
    new_item: TodoItem = TodoItem(**current_item)
    app.todos[todo_list_name][todo_item.id] = new_item
    return new_item


@app.delete("/lists/{todo_list_name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(todo_list_name: str, todo_item: TodoItemModify) -> None:
    try:
        del app.todos[todo_list_name][todo_item.id]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given list doesn't exists"
        )
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given item doesn't exists"
        )
    return
