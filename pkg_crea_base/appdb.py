'''
Created on 20 juil. 2017

@author: Utilisateur
'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///alembictest.db')