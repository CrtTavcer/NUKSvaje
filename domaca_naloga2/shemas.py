from pydantic import BaseModel

"""
class PosteBase(BaseModel):
    title: str
    content: str
"""
class Car(BaseModel):
    id: int
    owner_id: int
    #date_created: 
    brand: str
    model: str
    year: int
    milage: int
    price: int

    class config: #proti lazyloading
        orm_mode = True
"""
class UserBase(BaseModel):
    email: str
"""
class User(BaseModel):
    name: str
    surname: str
    email: str
