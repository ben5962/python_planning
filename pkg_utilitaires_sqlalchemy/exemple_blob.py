'''
Created on 17 sept. 2017

@author: Utilisateur
https://stackoverflow.com/questions/1779701/example-using-blob-in-sqlalchemy
'''
from sqlalchemy import *
from sqlalchemy.orm import mapper, sessionmaker
import os

engine = create_engine('sqlite://', echo=True)
metadata = MetaData(engine)

sample = Table(
    'sample', metadata,
    Column('id', Integer, primary_key=True),
    Column('lob', Binary),
)

class Sample(object):

    def __init__(self, lob):
        self.lob = lob

mapper(Sample, sample)

metadata.create_all()

session = sessionmaker(engine)()

# Creating new object
blob = os.urandom(100000)
obj = Sample(lob=blob)
session.add(obj)
session.commit()
obj_id = obj.id
session.expunge_all()

# Retrieving existing object
obj = session.query(Sample).get(obj_id)
assert obj.lob==blob
if __name__ == '__main__':
    pass