from typing import Optional, List, Union
from pydantic import BaseModel, Field, HttpUrl

"""
class PosteBase(BaseModel):
    title: str
    content: str
"""
class Car(BaseModel):

    brand: str
    model: str
    year: int
    milage: int
    price: int 
    

class Car_img_sch(BaseModel):
    image: bytes

"""
    class config: #proti lazyloading
        orm_mode = True

class UserBase(BaseModel):
    email: str
"""
class User(BaseModel):
    name: str
    surname: str
    email: str
