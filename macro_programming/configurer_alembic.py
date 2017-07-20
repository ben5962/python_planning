'''
Created on 18 juil. 2017

@author: Utilisateur
'''
import configparser
import distutils
from distutils.file_util import copy_file
config = configparser.ConfigParser()
config.read('alembic.ini')
chemin_base = r"C:\Users\Utilisateur\git\python_planning"

if __name__ == '__main__':
    print(config.get('alembic', 'sqlalchemy.url'))
    valeur_initiale = "driver://user:pass@localhost/dbname"
    if config.get('alembic', 'sqlalchemy.url') == valeur_initiale:
        config.set('alembic','sqlalchemy.urlback', valeur_initiale)
        config.set('alembic','sqlalchemy.url','sqlite:///' + chemin_base)
        distutils.file_util.copy_file('alembic.ini','alembic.ini.bak')
        with open('alembic.ini','w') as f:
            config.write(f)
            
        
