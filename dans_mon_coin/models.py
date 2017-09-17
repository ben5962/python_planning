'''
Created on 29 août 2017

@author: Utilisateur
'''



from pathlib import Path
import csv
from dateutil.parser import *

#imports de cochon
import sys
chemin_mail = Path(r'C:\Users\Utilisateur\Documents\GitHub\parse_email').resolve()
chemin_imports_de_cochon = Path(r'C:\Users\Utilisateur\Documents\GitHub\import_de_cochon').resolve()
chemin_pdf = Path(r'C:\Users\Utilisateur\Documents\GitHub\parse_pdf').resolve()
for chemin in [chemin_mail, chemin_imports_de_cochon, chemin_pdf]:
    sys.path.append(str(chemin))
#go!
from module_objet_pdf import Objet_pdf
from module_objet_mail import Objet_mail




from sqlalchemy import Table, Column, Integer, Numeric, String, Date, Boolean, DateTime, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
from sqlalchemy.sql.sqltypes import DateTime


Base = declarative_base()



dbg = False
def print_dbg(msg):
    if dbg:
        print(msg)

class Emails(Base): 
    __tablename__ = 'Emails'
    email_id = Column(Integer(), primary_key=True)
    fichier_email = Column(BLOB(), nullable=False)
    nom_fichier_mail = Column(String(), nullable=False)
    date_objet_mail = Column(Date(),nullable=False)
    def __repr__(self):
        return "Emails(email_id={self.email_id}, "\
            "nom_fichier_mail={self.nom_fichier_mail} ,"\
            "date_objet_mail={self.date_objet_mail})".format(self=self)
    
           
class Documents(Base):
    __tablename__ = 'Documents'
    documents_id = Column(Integer(), primary_key=True)
    date_document = Column(Date(), nullable = False)
    titre_document= Column(String(100), nullable = False)
    type_document = Column(String(2), nullable = False)
    origine = Column(String(150), nullable = False)
    a_ete_verifie= Column(Boolean(), default = False)
    est_pertinent = Column(Boolean())
    date_debut_periode_couverte = Column(Date())
    horo_debut_periode_couverte = Column(DateTime())
    date_fin_periode_couverte = Column(Date())
    remarques = Column(String(150))
    #nom_document_a_traiter = Column(String(150))
    #type_document_a_traiter = Column(String(150))

    def __repr__(self):
        chaine = "Documents(document_id = {self.documents_id}, "\
                 "date_document = {self.date_document}, "\
                 "titre_document = {self.titre_document}, "\
                 "type_document = {self.type_document}, "\
                 "origine ={self.origine},"\
                 "debut_periode_couverte = {self.date_debut_periode_couverte},"\
                 "fin_periode_couverte = {self.date_fin_periode_couverte}".format(self=self)
        return chaine
    
class SourceDocumentairePertinente(Base):
    __tablename__ = 'SourceDocumentairePertinente'
    source_pertinente_id = Column(Integer(), primary_key=True)
    date_document = Column(Date(), nullable=False)
    titre_document= Column(String(100), nullable = False)
    type_document = Column(String(2), nullable = False)
    origine = Column(String(150), nullable = False)
    date_debut_periode_couverte = Column(Date())
    horo_debut_periode_couverte = Column(DateTime())
    date_fin_periode_couverte = Column(Date())
    remarques = Column(String(150))
    
engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def insert_initial_values(*args, **kwargs):
    fichier = "documents.csv"
    # pour nommer les argumentsde reader
    keys = [ 'date_document', 'titre_document', 'type_document', 'origine']
    with open(fichier, 'r') as f:
        reader = csv.reader(f)
        next(reader, None) # skip header
        for values in reader:
            dico = dict(zip(keys,values))
            print_dbg(dico['date_document'])
            date_iso = dico['date_document'][0:-3]
            session.add(Documents(date_document = parse(date_iso),
                              titre_document = dico['titre_document'],
                              type_document = dico['type_document'],
                              origine = dico['origine'])
                        )
        session.flush()


#insert_initial_values()

def inserer_documents_pertinents_apres_sophie(*args, **kwargs):
    pass

def choisir_documents_pertinents(*args, **kwargs):
    """ ceux dans avant sophie et apres sophie"""
    pass


def insert_mails(*args, **kwargs):
    chemin_fichiers_mails = Path(r'C:\Users\Utilisateur\Documents\GitHub\mails_plannings\pertinent normalisé').resolve().glob('*.eml')
    
    for fichier in chemin_fichiers_mails:
        m = Objet_mail(str(fichier))
        with open(str(fichier),'rb') as f:
            session.add(
                Emails(
                    fichier_email=f.read(),
                    nom_fichier_mail=fichier.name,
                    date_objet_mail = m.getDate()
                    
                    )
                        )

def lire_mails(*args, **kwargs):
    pass
    

#print(session.query(Documents).all())       
insert_mails()
print(session.query(Emails).all())
