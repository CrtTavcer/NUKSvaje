from typing import Union
from fastapi import FastAPI, HTTPException, status, File, UploadFile, Response
from fastapi.responses import StreamingResponse
from database import engine, Base, Car, Car_img
import shemas
from sqlalchemy.orm import Session
from fastapi_versioning import VersionedFastAPI, version

from sqlalchemy import inspect, insert, update
from typing import Optional



from io import BytesIO
from PIL import Image

from starlette.responses import RedirectResponse

from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://0.0.0.0:8081",
    "http://localhost:8081",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#--------------------options-------------------------------
@app.options("/add/car")
async def handle_options():
    return {"Allow": "POST"}

@app.options("/add/car/img")
async def handle_options():
    return {"Allow": "POST"}

@app.options("/delete/car/{id}")
async def handle_options():
    return {"Allow": "DELETE"}


#@app.options("/update/car/{id}/{brand}/{model}/{year}/{milage}/{price}")
@app.options("/update/car/{id}/{brand}")
async def handle_options():
    return {"Allow": "PUT"}

#----------------------------------------------------


@app.get("/")
@version(2)
def read_root():
    return "AvtoNet app"


#-----------------------slika----------------------------------------------------------------------

@app.post("/add/car/img", tags = ["car image"], status_code = status.HTTP_201_CREATED)
@version(2)
def add_car_img(image: UploadFile = File(...)):
# def add_car(image: shemas.Car_img_sch):

    """
    API call for posting new car
    """ 
    # Convert image data to binary format
    binary_data = BytesIO(image.file.read()).getvalue()
    print("TESTTT")
    print(image)
    print("binary image: ", binary_data)

    session = Session(bind = engine, expire_on_commit = False)

    # avtoDB = Car_img(slika = binary_data, image = binary_data)
    session.execute(
     insert(Car_img),
     [
         {"image": binary_data},
     ],
     )

    session.commit()
    print("PRINTING ID: ", id)

    session.close()

    return f"created new image for id {id}"


@app.post("/update/car/image/{id}", tags = ["car image"], status_code = status.HTTP_201_CREATED)
@version(2)
def update_car_image(id: int, image_data: UploadFile = File(...)):
    # Search for the car by ID
    binary_data = BytesIO(image_data.file.read()).getvalue()
    session = Session(bind=engine, expire_on_commit=False)
    car = session.query(Car_img).filter_by(id=id).first()

    if car is None:
        raise ValueError(f"Car with id {id} not found in database.")

    # Update the car's image data
    session.execute(
        update(Car).where(Car.id == id).values(image=image_data)
    )
    session.commit()
  

    session.close()

    return f"created new image for id {id}"


@app.delete("/delete/car/img/{id}", tags = ["car"])
@version(2)
def delete_car(id:int):
    session = Session(bind=engine, expire_on_commit=False)
    car_db = session.query(Car_img).get(id)
    if not car_db:
        raise HTTPException(status_code=404, detail="Car not found")
    #id = car_db.id
    session.delete(car_db)
    session.commit()
    session.close()
    return "Img with id {id} deleted"



@app.get("/get/img/{id}", tags = ["car image"])
@version(2)
def get_car_img(id:int):
    """
    API call for getting car image
    """ 
    print("Searching for car with ID: ", id)

    # Search database
    session = Session(bind=engine, expire_on_commit=False)
    car = session.query(Car_img).filter_by(id=id).first()
    session.close()

    # Respond to client
    if not car.image:
        raise HTTPException(status_code = 404, detail = f"Car image with id {id} doesen't exsist")
    return Response(content=car.image, media_type="image/jpeg")

"""
@app.get("/get/all/{id}", tags = ["car image"])
@version(2)
def get_car_img(id:int):
   
    print("Searching for car with ID: ", id)

    # Search database
    session = Session(bind=engine, expire_on_commit=False)
    car = session.query(Car_img).filter_by(id=id).first()
    session.close()

    # Create multipart response
    response = StreamingResponse(
        self._generate_parts(car),
        media_type="multipart/mixed; boundary=1234567890"
    )

    return response

def _generate_parts(car):
    # Part 1: JSON data
    yield b'--1234567890\r\n'
    yield b'Content-Type: application/json\r\n\r\n'
    yield json.dumps({"car_id": car.id, "make": car.make, "model": car.model}).encode('utf-8')
    yield b'\r\n'

    # Part 2: JPEG image data
    yield b'--1234567890\r\n'
    yield b'Content-Type: image/jpeg\r\n\r\n'
    yield car.image
    yield b'\r\n'

    # End of multipart response
    yield b'--1234567890--'  return Response(content=car.image, media_type="image/jpeg")

"""


from fastapi.responses import StreamingResponse
import io

@app.get("/get/img/list", tags=["car image"])
@version(2)
def get_car_img_all():
    """
    API call for getting car images
    """
    print("getting all car images")

    session = Session(bind=engine, expire_on_commit=False)
    car_images = session.query(Car_img).all()
    session.close()

    if not car_images:
        raise HTTPException(status_code=404, detail="No car images found")

    # Create a list of StreamingResponse objects, each containing an image in binary format
    response_list = []
    for img in car_images:
        if not img.image:
            raise HTTPException(status_code=404, detail=f"Car image with id {img.id} doesn't exist")
        img_bytes = io.BytesIO(img.image)
        response = StreamingResponse(img_bytes, media_type="image/jpeg")
        response_list.append(response)

    return response_list

#---------------------------------------------------------------------------------------------------





#--------------------------------------V2------------------------------------------------------



@app.get("/get/{id}")
@version(2)
def get_car(id:int):
    """
    API call for getting car
    """ 
    session = Session(bind=engine, expire_on_commit=False)
    car = session.query(Car).get(id)
    session.close()
    if not car:
        raise HTTPException(status_code = 404, detail = f"Car with id {id} doesen't exsist")

    return car
"""
@app.get("/get/{brand}", tags = ["car"])
@version(2)
def get_car_brand(brand: str):
   
    session = Session(bind=engine, expire_on_commit=False)
    car_brand = session.query(Car).filter(Car.brand == brand).all()
    session.close()
    if not car_brand:
        raise HTTPException(status_code = 404, detail = f"Car brand doesen't exsist")
        
    return car_brand
"""
@app.get("/list", tags = ["car"])
@version(2)
def get_all_cars():
    """
    API call for getting all cars
    """ 
    print("Test")
    session = Session(bind=engine, expire_on_commit=False)
    cars = session.query(Car).all()
    session.close()

    if not cars:
        raise HTTPException(status_code = 404, detail = f"car list doesen't exsist")

    return [car.__dict__ for car in cars]   
      
@app.options("/list", tags = ["car"])
@version(2)
def get_all_cars():
    """
    API call for getting all cars
    """ 
    print("OPTIONS")
    session = Session(bind=engine, expire_on_commit=False)
    cars = session.query(Car).all()
    session.close()

    if not cars:
        raise HTTPException(status_code = 404, detail = f"car list doesen't exsist")

    return [car.__dict__ for car in cars]     

@app.post("/add/car", tags = ["car"], status_code = status.HTTP_201_CREATED)
@version(2)
def add_car(car: shemas.Car):

    #API call for posting new car

    session = Session(bind = engine, expire_on_commit = False)
    
    avtoDB = Car(brand = car.brand, model = car.model,
    year= car.year, milage = car.milage, price = car.price)
    

    session.add(avtoDB)
    session.commit()
    id = avtoDB.id
    brand = avtoDB.brand
    session.close()

    return f"created new car {brand} with id {id}"
"""


@app.post("/add/car", tags = ["car"], status_code = status.HTTP_201_CREATED)
@version(2)
def add_car(car: shemas.Car, image: UploadFile = File(...)):
    
    #API call for posting new car
    
    session = Session(bind = engine, expire_on_commit = False)
    
    #avtoDB = Car(brand = car.brand, model = car.model,
    #year= car.year, milage = car.milage, price = car.price)
    
    session.execute(
     insert(Car),
     [
         {  "brand": car.brand,
            "model": car.model,
            "year": car.year,
            "milage": car.milage,
            "price": car.price,
            "image": binary_data
            },
     ],
     )

    #session.add(avtoDB)
    session.commit()
    id = avtoDB.id
    brand = avtoDB.brand
    session.close()

    return f"created new car {brand} with id {id}"
"""



@app.post("/add/user", tags = ["user"], status_code = status.HTTP_201_CREATED)
@version(2)
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

#@app.put("/update/car/{id}/{brand}/{model}/{year}/{milage}/{price}", tags = ["car"])
@app.put("/update/car/{id}/{brand}", tags = ["car"])
@version(2)
def update_car(id: int, brand: Optional[str] = None, model: Optional[str] = None, year: Optional[int] = None, milage: Optional[int] = None, price: Optional[int] = None):
    """
    API call for updating car attributes
    """ 
    session = Session(bind=engine, expire_on_commit=False)
    car_db = session.query(Car).get(id)

    if car_db:
        if brand is not None:
            car_db.brand = brand
        if model is not None:
            car_db.model = model
        if year is not None:
            car_db.year = year
        if milage is not None:
            car_db.milage = milage
        if price is not None:
            car_db.price = price
        session.commit()
    session.close()
    
    if not car_db:
        raise HTTPException(status_code=404, detail=f"Car item with id {id} doesn't exist")
        return car_dbception(status_code = 404, detail = f"car item with id {id} doesen't exsist")
    return car_db

@app.delete("/delete/car/{id}", tags = ["car"])
@version(2)
def delete_car(id:int):
    session = Session(bind=engine, expire_on_commit=False)
    car_db = session.query(Car).get(id)
    if not car_db:
        raise HTTPException(status_code=404, detail="Car not found")
    #id = car_db.id
    session.delete(car_db)
    session.commit()
    session.close()
    return "Car with id {id} deleted"

@app.delete("/delete/user/{id}", tags = ["user"])
@version(2)
def delete_user(id:int):
    session = Session(bind=engine, expire_on_commit=False)
    user_db = session.query(user).get(id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user_db)
    session.commit()
    session.close()
    return "User deleted"

#------------------------------V1--------------------------------------------

@app.get("/")
@version(1)
def read_root(): 
    return "hello"

@app.get("/get/{id}")
@version(1)
def get_car(id:int):
    """
    API call for getting car
    """ 
    session = Session(bind=engine, expire_on_commit=False)
    car = session.query(Car).get(id)
    session.close()
    if not car:
        raise HTTPException(status_code = 404, detail = f"Car with id {id} doesen't exsist")

    return car
"""
@app.get("/get/{brand}", tags = ["car"])
@version(1)
def get_car_brand(brand: str):
    
    session = Session(bind=engine, expire_on_commit=False)
    car_brand = session.query(Car).filter(Car.brand == brand).all()
    session.close()
    if not car_brand:
        raise HTTPException(status_code = 404, detail = f"Car brand doesen't exsist")
        
    return car_brand
"""
@app.get("/list", tags = ["car"])
@version(1)
def get_all_cars():
    """
    API call for getting all cars
    """ 

    session = Session(bind=engine, expire_on_commit=False)
    cars = session.query(Car).all()
    session.close()
    return [car.__dict__ for car in cars]     

@app.post("/add/car", tags = ["car image"], status_code = status.HTTP_201_CREATED)
@version(1)
def add_car(car: shemas.Car):
    """
    API call for posting new car
    """ 
    session = Session(bind = engine, expire_on_commit = False)
    
    avtoDB = Car(brand = car.brand, model = car.model,
    year= car.year, milage = car.milage, price = car.price)

    session.add(avtoDB)
    session.commit()
    id = avtoDB.id
    brand = avtoDB.brand
    session.close()

    return f"created new car {brand} with id {id}"

@app.post("/add/user", tags = ["user"])
@version(1)
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




@app.delete("/delete/car/{id}")
@version(1)
def delete_car(id:int):
    session = Session(bind=engine, expire_on_commit=False)
    car_db = session.query(Car).get(id)
    if not car_db:
        raise HTTPException(status_code=404, detail="Car not found")
    id = car_db.id
    session.delete(car_db)
    session.commit()
    session.close()
    return "Car with id {id} deleted"

@app.delete("/delete/user/{id}", tags = ["user"])
@version(1)
def delete_user(id:int):
    session = Session(bind=engine, expire_on_commit=False)
    user_db = session.query(user).get(id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user_db)
    session.commit()
    session.close()
    return "User deleted"



"""
@app.put("/update/{id}/brand&model", tags = ["update"])
@version(1)
def update_car_brand(id:int, brand: str, model: str):
   
    session = Session(bind = engine, expire_on_commit = False)
    car_db = session.query(Car).get(id)

    if car_db:
        car_db.brand = brand
        car_db.model = model
        session.commit()
    session.close()
    
    if not car_db:
        raise HTTPException(status_code = 404, detail = f"car item with id {id} doesen't exsist")
    return car_db

@app.put("/update/{id}/milage", tags = ["update"])
@version(1)
def update_car_milage(id:int, milage: int):
   
    # Retrieve the car object from the database based on the ID
    session = Session(bind = engine, expire_on_commit = False)
    car_db = session.query(Car).get(id)
    # If the car object does not exist, return a 404 error
    if car_db:
        car_db.milage = milage
        session.commit()
    session.close()
    
    if not car_db:
        raise HTTPException(status_code = 404, detail = f"car item with id {id} doesen't exsist")
    return car_db

@app.put("/update/{id}/year", tags = ["update"])
@version(1)
def update_car_year(id:int, year: int):

    session = Session(bind=engine, expire_on_commit=False)
    car_db = session.query(Car).get(id)
    
    if car_db:
        car_db.year = year
        session.commit()
    session.close()
    
    if not car_db:
        raise HTTPException(status_code = 404, detail = f"car item with id {id} doesen't exsist")
    return car_db

@app.put("/update/{id}/price", tags = ["update"])
@version(1)
def update_car_price(id:int, price: int):
    session = Session(bind=engine, expire_on_commit=False)
    car_db = session.query(Car).get(id)
    
    if car_db:
        car_db.price = price
        session.commit()
    session.close()
    
    if not car_db:
        raise HTTPException(status_code = 404, detail = f"car item with id {id} doesen't exsist")
    return car_db


@app.put("/update/{id}", tags = ["update"])
@version(1)
def update_car_all(id:int, car: shemas.Car):
    session = Session(bind=engine, expire_on_commit=False)
    car_db = session.query(Car).get(id)
    
    if car_db:
        car_db.car = car
        session.commit()
    session.close()
    
    if not car_db:
        raise HTTPException(status_code = 404, detail = f"car item with id {id} doesen't exsist")
    return car_db
"""




"""

@app.put("/update/{id}/brand&model", tags = ["update"])
@version(2)
def update_car_brand(id:int, brand: str, model: str):
    
    session = Session(bind = engine, expire_on_commit = False)
    car_db = session.query(Car).get(id)

    if car_db:
        car_db.brand = brand
        car_db.model = model
        session.commit()
    session.close()
    
    if not car_db:
        raise HTTPException(status_code = 404, detail = f"car item with id {id} doesen't exsist")
    return car_db

@app.put("/update/{id}/milage", tags = ["update"])
@version(2)
def update_car_milage(id:int, milage: int):
    
    # Retrieve the car object from the database based on the ID
    session = Session(bind = engine, expire_on_commit = False)
    car_db = session.query(Car).get(id)
    # If the car object does not exist, return a 404 error
    if car_db:
        car_db.milage = milage
        session.commit()
    session.close()
    
    if not car_db:
        raise HTTPException(status_code = 404, detail = f"car item with id {id} doesen't exsist")
    return car_db

@app.put("/update/{id}/year", tags = ["update"])
@version(2)
def update_car_year(id:int, year: int):

    session = Session(bind=engine, expire_on_commit=False)
    car_db = session.query(Car).get(id)
    
    if car_db:
        car_db.year = year
        session.commit()
    session.close()
    
    if not car_db:
        raise HTTPException(status_code = 404, detail = f"car item with id {id} doesen't exsist")
    return car_db

@app.put("/update/{id}/price", tags = ["update"])
@version(2)
def update_car_price(id:int, price: int):
    session = Session(bind=engine, expire_on_commit=False)
    car_db = session.query(Car).get(id)
    
    if car_db:
        car_db.price = price
        session.commit()
    session.close()
    
    if not car_db:
        raise HTTPException(status_code = 404, detail = f"car item with id {id} doesen't exsist")
    return car_db

"""


  
app = VersionedFastAPI(app, version_format = '{major}', prefix_format = '/v{major}')
