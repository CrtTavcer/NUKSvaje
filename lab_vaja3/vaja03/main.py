from typing import Union
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from database import engine, Base, ToDo
import shemas
from sqlalchemy.orm import Session

from fastapi_versioning import VersionedFastAPI, version

Base.metadata.create_all(engine)

app = FastAPI()


@app.get("/")
def read_root():
    return "TODO app" 

@app.post("/add", status_code = status.HTTP_201_CREATED)
@version(1)
def add_todo(todo: shemas.ToDo):

    session = Session(bind = engine, expire_on_commit = False)
    todoDB = ToDo(task = todo.task)
    session.add(todoDB)
    session.commit()
    id = todoDB.id
    session.close()
    

    return f"created new TODO item with id {id}"

@app.post("/img", status_code = status.HTTP_201_CREATED)
@version(1)
def add_todo(image: UploadFile = File(...)):

    session = Session(bind = engine, expire_on_commit = False)
# Convert image data to base64-encoded string
    image_data = base64.b64encode(image_file.file.read()).decode("utf-8")

    todoDB = ToDo(image=image_data)
    session.add(todoDB)
    session.commit()
    img= todoDB.img
    session.close()
    

    return f"created new img {img}"


@app.delete("/delete/{id}")
@version(1)
def delete_todo(id:int):
    return "Delete TODO"


@app.delete("/delete/{id}")
@version(2)
def delete_todo(id:int):

    session = Session(bind = engine, expire_on_commit = False)
    todo = session.query(ToDo).get(id)
    
    if todo:
        session.delete(todo)
        session.commit()
        session.close()
    else:
        session.close()
        raise HTTPException(status_code = 404, detail = f"Todo itedm with id {id} doesen't exsist")

    return f"Delete TODO with id {id}"



@app.put("/update/{id}")
@version(1)
def update_todo(id:int):
    return "update TODO"



@app.put("/update/{id}")
@version(2)
def update_todo(id:int, task: str):

    session = Session(bind = engine, expire_on_commit = False)
    todo = session.query(ToDo).get(id)
    
    if todo:
        todo.task = task
        session.commit()
    session.close()
    
    if not todo:
        raise HTTPException(status_code = 404, detail = f"Todo itedm with id {id} doesen't exsist")
    return todo



@app.get("/get/{id}")
@version(1)
def get_todo(id:int):
    return "get TODO"
    """
    API call for getting TODO item
    """

@app.get("/get/{id}")
@version(2)
def get_todo(id:int):

    session = Session(bind = engine, expire_on_commit = False)
    todo = session.query(ToDo).get(id)
    session.close()

    if not todo:
        raise HTTPException(status_code = 404, detail = f"Todo itedm with id {id} doesen't exsist")
    
    return todo
    """
    API call for getting TODO item
    """


@app.get("/list")
@version(1)
def get_all_todo():
    return "get all TODO"   

@app.get("/list")
@version(2)
def get_all_todo():

    session = Session(bind = engine, expire_on_commit = False)
    todoall = session.query(ToDo).all()
    session.close()

    return todoall  


app = VersionedFastAPI(app, version_format = '{major}', prefix_format = '/v{major}')