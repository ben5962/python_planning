'''
Created on 7 juil. 2017

@author: Utilisateur
'''
import unittest
import devpy.develop as log
import pkg_date_heure
import os
from fileDoesNotExist import FileDoesNotExist
import devpy
from sqlalchemy.sql.schema import Table
log = devpy.autolog()

class Test(unittest.TestCase):
    pass


def cree_fonctiondetest(description, date_sqlite, semaine_iso_sqlite, semaine_iso_python):
    def teste_valeur(self):
        """vrai si le numero de semaine iso calculé par sqlite est le même que celui
        généré par math_date.Date().numero_semaine """
        self.assertEquals(semaine_iso_sqlite,pkg_date_heure.math_date.Date(date_sqlite).num_semaine)


if __name__ == "__main__":
#     from sqlalchemy.ext.automap import automap_base
#     from sqlalchemy.orm import Session
#     from sqlalchemy import create_engine
# 
#     Base = automap_base()
#     sqlite_db_path = "C:\\Users\\Utilisateur\\git\\python_planning\\planning.db"
#     
#     if os.path.isfile(sqlite_db_path):
#         log.info("le fichier {} existe".format(sqlite_db_path))
#         engine = create_engine("sqlite:///" + sqlite_db_path)
#     else:
#         raise FileDoesNotExist
#     # reflect the tables
#     Base.prepare(engine, reflect=True)
#     Base.classes.keys()
# 
#     session = Session(bind = engine)
    

    from sqlalchemy import MetaData, create_engine
    metadata = MetaData()
    sqlite_db_path = "C:\\Users\\Utilisateur\\git\\python_planning\\planning.db"
     
    if os.path.isfile(sqlite_db_path):
        log.info("le fichier {} existe".format(sqlite_db_path))
        engine = create_engine("sqlite:///" + sqlite_db_path)
    else:
        raise FileDoesNotExist
    from sqlalchemy import Table
    vue_48_heures = Table('plus_de_48', metadata, autoload=True, autoload_with=engine)
    print(vue_48_heures.columns.keys())
    from sqlalchemy import select
    s = select([vue_48_heures]).limit(10)
    print(engine.execute(s).fetchall())

    #import sys;sys.argv = ['', 'Test.testName']
    # au niveau des tests, on va se gaver  comme des oies: on a une base de données.
    # elle va nous fournir les tests, bah tiens!
    unittest.main()
