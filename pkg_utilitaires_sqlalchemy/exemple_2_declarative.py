'''
Created on 17 sept. 2017

@author: Utilisateur
'''


from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from struct import *

_DeclarativeBase = declarative_base()

class MyTable(_DeclarativeBase):
    __tablename__ = 'mytable'
    id = Column(Integer, Sequence('my_table_id_seq'), primary_key=True)
    my_blob = Column(BLOB)

DB_NAME = 'sqlite:///C:/BlobbingTest.db'
db = create_engine(DB_NAME)
#self.__db.echo = True
_DeclarativeBase.metadata.create_all(db)
Session = sessionmaker(bind=db)
session = Session()

session.add(MyTable(my_blob=pack('H', 365)))
l = [n + 1 for n in xrange(10)]
session.add(MyTable(my_blob=pack('H'*len(l), *l)))
session.commit()

query = session.query(MyTable)
for mt in query.all():
    print unpack('H'*(len(mt.my_blob)/2), mt.my_blob)
if __name__ == '__main__':
    pass