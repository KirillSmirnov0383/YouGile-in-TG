from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import hashlib

Base = declarative_base()

def create_tables():
    engine = create_engine("postgresql://postgres:KlimKva22@localhost/YouGile_Managment")
    Base.metadata.create_all(engine)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    Telegram_id = Column(String, unique=True)
    email = Column(String)
    password = Column(String)
    company_name = Column(String)

    api_companies = relationship("ApiCompany", back_populates="user")



class ApiCompany(Base):
    __tablename__ = 'api_company'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    company_id = Column(String, ForeignKey('company.id'))
    api_key = Column(String)

    user = relationship("User")
    company = relationship("Company")

class Company(Base):
    __tablename__ = 'company'

    id = Column(String, primary_key=True)
    name = Column(String)


