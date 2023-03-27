import sqlalchemy as sql
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
import datetime as dt


#
engine = create_engine("sqlite:///Avtodatabase.db")
#za user modele
Base = declarative_base()

#tabele
class Car(Base):
    __tablename__ = "car_table"
    id = Column(Integer, primary_key = True)
    brand = Column(String(50)) 
    model = Column(String(50))
    year = Column(Integer())
    milage = Column(Integer())
    price = Column(Integer())
    #image = Column(LargeBinary()) #kao ne obstaja?
    #poskus povezovanja tabel
    #images = relationship("Car_img", backref="car", cascade="all, delete-orphan")

    #owner_id = Column(Integer, ForeignKey("user_table.id"))
    #date_created = Column(DateTime, default = dt.datetime.utcnow) 
    #date_updated = Column(DateTime, default = dt.datetime.utcnow)
    #owner = relationship("User", back_populates = "Car")

class Car_img(Base):
    __tablename__ = "car_images"
    id = Column(Integer, primary_key = True)
    image = Column(LargeBinary())

    #poskus povezovanja tabel
    car_id = Column(Integer, ForeignKey("car_table.id"))


class User(Base):
    __tablename__ = "user_table"
    id = Column(Integer, primary_key = True)
    email = Column(String, unique = True)
    name = Column(String(50))
    surname = Column(String(50))
    #katere objave mima user
    #posts = relationship("Car", back_populates = "owner")
 
    
