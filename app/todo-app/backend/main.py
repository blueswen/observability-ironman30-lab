import logging
import os
from typing import List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

EXPOSE_PORT = os.environ.get("EXPOSE_PORT", 8000)


class ToDoCreate(BaseModel):
    title: str
    description: str
    completed: bool = False


class ToDoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class ToDoInDB(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

    class Config:
        orm_mode = True


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# In-memory storage for ToDo items
todos = {}
current_id = 0


@app.post("/todos/", response_model=ToDoInDB)
def create_todo(todo: ToDoCreate):
    global current_id
    current_id += 1
    todo_item = ToDoInDB(id=current_id, **todo.dict())
    todos[current_id] = todo_item
    logging.error(f"Create todo: {current_id}")
    return todo_item


@app.get("/todos/{todo_id}", response_model=ToDoInDB)
def read_todo(todo_id: int):
    todo_item = todos.get(todo_id)
    if todo_item is None:
        logging.error(f"Read todo: {todo_id} not found")
        raise HTTPException(status_code=404, detail="ToDo not found")
    logging.error(f"Read todo: {todo_id}")
    return todo_item


@app.put("/todos/{todo_id}", response_model=ToDoInDB)
def update_todo(todo_id: int, todo: ToDoUpdate):
    todo_item = todos.get(todo_id)
    if todo_item is None:
        logging.error(f"Update todo: {todo_id} not found")
        raise HTTPException(status_code=404, detail="ToDo not found")
    update_data = todo.dict(exclude_unset=True)
    updated_todo = todo_item.copy(update=update_data)
    todos[todo_id] = updated_todo
    logging.error(f"Update todo: {todo_id}")
    return updated_todo


@app.delete("/todos/{todo_id}", response_model=ToDoInDB)
def delete_todo(todo_id: int):
    todo_item = todos.pop(todo_id, None)
    if todo_item is None:
        logging.error(f"Delete todo: {todo_id} not found")
        raise HTTPException(status_code=404, detail="ToDo not found")
    logging.error(f"Delete todo: {todo_id}")
    return todo_item


@app.get("/todos/", response_model=List[ToDoInDB])
def list_todos(skip: int = 0, limit: int = 10):
    todo_list = list(todos.values())[skip : skip + limit]
    return todo_list


@app.get("/error")
def error():
    raise HTTPException(status_code=500, detail="This is an error")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=EXPOSE_PORT)
