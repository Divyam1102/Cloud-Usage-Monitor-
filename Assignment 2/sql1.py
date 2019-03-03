from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey, Column, Date, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


engine = create_engine('sqlite:///tutorial.db', echo = True)
Base = declarative_base()

class VirtualMachineUsage(Base):
    __tablename__ = "virtualmachineusage"

    id = Column(Integer, primary_key = True, nullable = False)
    instanceid = Column(Integer, nullable = False)
    plan = Column(String)
    starttime = Column(DateTime, nullable = False)
    stoptime = Column(DateTime)
    usage = Column(Integer)
    charges = Column(Integer)
    

def __init__(self, instanceid, plan, starttime, stoptime, usage, charges ):
    self.instanceid = instanceid 
    self.plan = plan
    self.starttime = starttime
    self.stoptime = stoptime
    self.usage = usage
    self.charges = charges
    

Base.metadata.create_all(engine)
