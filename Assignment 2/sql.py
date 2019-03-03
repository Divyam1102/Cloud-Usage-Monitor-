from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey, Column, Date, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


engine = create_engine('sqlite:///tutorial.db', echo = True)
Base = declarative_base()

class CreateVirtualMachine(Base):
    __tablename__ = "virtualmachine"

    id = Column(Integer, primary_key = True, nullable = False)
    plan = Column(String)
    
    

def __init__(self, plan):
    self.plan = plan
    
    

Base.metadata.create_all(engine)
