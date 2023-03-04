from typing import Union
from fastapi import FastAPI
from database import engine, Base, ToDo
import shemas
from sqlalchemy.orm import session

base.metadata.create_all(engine)

app = FastAPI()


@app.get("/")
def read_root():
    return "TODO app"

@app.post("/add")
def add_todo(todo: shemas.ToDO):

    session = Session(bind = engine, expire_on_commit = False)
    todoDB = ToDo(task = todo.task)
    session.add(todoDB)
    session.commit()
    id = todoDB.id
    session.close()


    return f"created new TODO item with id{id}"


@app.delete("/delete/{id}")
def delete_todo(id:int):
    return "Delete TODO"

@app.put("/update/{id}")
def update_todo(id:int):
    return "update TODO"

@app.get("/get/{id}")
def get_todo(id:int):
    return "get TODO"
    """
    API call for getting TODO item
    """

@app.put("/list")
def get_all_todo():
    return "get all TODO"    

