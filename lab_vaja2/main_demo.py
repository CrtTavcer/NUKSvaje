from typing import Union
from fastapi import FastAPI
#from database import engine, Base, ToDo 
#from sqlalchemy.orm import Session
#Base.metadata.create_all(engine)
import shemas_demo

app = FastAPI()

@app.get("/")
def read_root():
    return "TODO app"

@app.post("/add")
def add_todo(todo: shemas_demo.ToDo):
   
    
    session = Session(bind = engine, expire_on_commit = False)
    todoDB = ToDo(task = todo.task)
    session.add(todoDB)
    session.commit()
    id = todoDB.id
    session.close()
    

    return f"created new TODO item with id{id}"

