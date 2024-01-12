from datetime import datetime

from pydantic import BaseModel, Field
from enum import IntEnum


class Priority(IntEnum):
    Non: int = 0
    Low: int = 1
    Medium: int = 2
    High: int = 3


class TodoListRequest(BaseModel):
    name: str


class TodoListRenameRequest(BaseModel):
    old: str
    new: str


class TodoItemRequest(BaseModel):
    name: str
    description: str = ""
    priority: int = Priority.Non


class TodoItemModify(TodoItemRequest):
    id: int
    name: str = ""
    done: bool = False


class TodoItem(TodoItemRequest):
    done: bool = False
    creation_time: datetime = Field(default_factory=datetime.now)
    update_time: datetime = Field(default_factory=datetime.now)


class TodoItemList(TodoItem):
    id: int
