from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///Avtodatabase.db")

Base = declarative_base()


class Avto(Base):
    __tablename__ = "avtotable"
    id = Column(Integer, primary_key = True)
    name = Column(String(50))
    year = Column(Integer(4))
    milage = Column(Integer(6))
    price = Column(Integer(6))
