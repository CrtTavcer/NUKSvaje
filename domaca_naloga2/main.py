from typing import Union
from fastapi import FastAPI
from database import engine, Base, Car
import shemas
from sqlalchemy.orm import session

Base.metadata.create_all(engine)

app = FastAPI()


@app.get("/", tags = ["ROOT"])
def read_root():
    return "AvtoNet app"

@app.get("/get/{id}", tags = ["car"])
def get_car(id:int):
    """
    API call for getting car
    """ 
    session = Session(bind=engine, expire_on_commit=False)
    car = session.query(Car).filter(Car.id == id).first()
    session.close()
    if not car:
        return {"error": "Car not found"}

    return car.__dict__

@app.get("/get/{brand}", tags = ["car"])
def get_car_brand(brand: str):
    """
    API call for getting cars by brand
    """ 
    session = Session(bind=engine, expire_on_commit=False)
    car_brand = session.query(Car).filter(Car.brand == brand).all()
    session.close()
    if not car_brand:
        return {"error": "Car brand not found"}

    return car.__dict__

@app.get("/list", tags = ["car"])
def get_all_cars():
    """
    API call for getting all cars
    """ 
    session = Session(bind=engine, expire_on_commit=False)
    cars = session.query(Car).all()
    session.close()
    return [car.__dict__ for car in cars]     

@app.post("/add/car", tags = ["car"])
def add_car(car: shemas.Car):
    """
    API call for posting new car
    """ 
    session = Session(bind = engine, expire_on_commit = False)
    avtoDB = Car(name = car.brand, model = car.model,
    year= car.year, milage = car.milage, price = car.price )

    session.add(avtoDB)
    session.commit()
    id = avtoDB.id
    session.close()

    return f"created new car with id{id}"

@app.post("/add/user", tags = ["user"])
def add_user(user: shemas.User):
    """
    API call for creating new user
    """ 
    session = Session(bind = engine, expire_on_commit = False)
    userDB = User(name = user.name, surname = user.surname, email = user.email )

    session.add(userDB)
    session.commit()
    id = userDB.id
    session.close()

    return f"created new user with id{id}"



@app.put("/update/{id}/brand", tags = ["update"])
def update_car_brand(id:int, car: shemas.Car):
    """
    API call for updating car brand
    """ 
    car_db = session.query(Car).get(id)
    if not car_db:
        raise HTTPException(status_code=404, detail="Car not found")
    car_db.brand = car.brand
    session.commit()
    session.close()

    return "updated car brand to"

@app.put("/update/{id}/milage", tags = ["update"])
def update_car_milage(id:int, car: shemas.Car):
    """
    API call for updating car milage
    """ 
    # Retrieve the car object from the database based on the ID
    car_db = session.query(Car).get(id)
    # If the car object does not exist, return a 404 error
    if not car_db:
        raise HTTPException(status_code=404, detail="Car not found")
    # Update the car object with the new milage
    car_db.milage = car.milage
    # Commit the changes to the database
    session.commit()
    session.close()
    return "updated car milage"

@app.put("/update/{id}/year", tags = ["update"])
def update_car_year(id:int):
    car_db = session.query(Car).get(id)
    
    if not car_db:
        raise HTTPException(status_code=404, detail="Car not found")
    
    car_db.year = car.year
    session.commit()
    session.close()
    return "updated car year"

@app.put("/update/{id}/price", tags = ["update"])
def update_car_price(id:int):
    car_db = session.query(Car).get(id)
    
    if not car_db:
        raise HTTPException(status_code=404, detail="Car not found")
    
    car_db.price = car.price
    session.commit()
    session.close()
    return "updated car price"

@app.put("/update/{id}", tags = ["update"])
def update_car_all(id:int):
    car_db = session.query(Car).get(id)
    
    if not car_db:
        raise HTTPException(status_code=404, detail="Car not found")
    
    car_db.all = car.all()
    session.commit()
    session.close()
    return "updated car info"


@app.delete("/delete/car/{id}")
def delete_car(id:int):
    car_db = session.query(Car).get(id)
    if not car_db:
        raise HTTPException(status_code=404, detail="Car not found")
    car_db.delete()
    session.commit()
    session.close()
    return "Car deleted"

@app.delete("/delete/user/{id}", tags = ["user"])
def delete_user(id:int):
    user_db = session.query(user).get(id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    user_db.delete()
    session.commit()
    session.close()
    return "User deleted"
  

