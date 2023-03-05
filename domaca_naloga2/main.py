from typing import Union
from fastapi import FastAPI
from database import engine, Base, Avto
import shemas
from sqlalchemy.orm import session

base.metadata.create_all(engine)

app = FastAPI()


@app.get("/")
def read_root():
    return "AvtoNet app"

@app.post("/add")
def add_car(car: shemas.Avto):

    session = Session(bind = engine, expire_on_commit = False)
    avtoDB = Avto(name = avto.name)
    session.add(avtoDB)
    session.commit()
    id = avtoDB.id
    session.close()

    return f"created new car with id{id}"


@app.delete("/delete/{id}")
def delete_car(id:int):
    return "Delete TODO"

@app.put("/update/{id}")
def update_car(id:int):
    return "update TODO"

@app.get("/get/{id}")
def get_car(id:int):
    return "get TODO"
    """
    API call for getting TODO item
    """

@app.put("/list")
def get_all_cars():
    return "get all TODO"    

