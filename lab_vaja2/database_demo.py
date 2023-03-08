from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///todobatabase.db")

Base = declarative_base()


class ToDo(Base):
    __tablename__ = "todotable"
    id = Column(Integer, primary_key = True)
    task = Column(String(50))

