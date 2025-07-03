from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer)
    amount = Column(Float)
    currency = Column(String)
    country = Column(String)
    timestamp = Column(DateTime)

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    country = Column(String)
    risk_score = Column(Integer)
    business_type = Column(String)
