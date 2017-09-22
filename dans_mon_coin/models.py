'''
Created on 29 août 2017

@author: Utilisateur
'''



from pathlib import Path
import csv
from dateutil.parser import *

import logging
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger(__name__)
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




from sqlalchemy import Table, Column, Integer, Numeric, String, Date, Boolean, DateTime, BLOB, ForeignKey
from sqlalchemy.orm import relationship
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
    chemin_fichier_mail = Column(String(),nullable=False)
    fichier_email = Column(BLOB(), nullable=False)
    nom_fichier_mail = Column(String(), nullable=False)
    date_objet_mail = Column(Date(),nullable=False)
    nb_pj = Column(Integer(),nullable=False)
    rel_pj = relationship("Attachments")
    
    def __repr__(self):
        return "Emails(email_id={self.email_id}, "\
            "nom_fichier_mail={self.nom_fichier_mail} ,"\
            "date_objet_mail={self.date_objet_mail})".format(self=self)

class Attachments(Base):
    __tablename__ = 'Attachments'
    attachment_id = Column(Integer(), primary_key=True)
    fichier_attachment = Column(BLOB(), nullable=False)
    nom_fichier_attachment = Column(String(), nullable=False)
    type_attachment = Column(String(), nullable=False)
    nb_pages = Column(Integer())
    emails_id = Column(Integer(), ForeignKey('Emails.email_id'))
    
           
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
    
#engine = create_engine('sqlite:///:memory:')
engine = create_engine('sqlite:///essai.db')
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
    chemin_fichiers_mails = Path(r'C:\Users\Utilisateur\Documents\GitHub\mails_plannings\pertinent normalisé').resolve().glob('2*.eml')
    logger.debug('insert_mails : entree ds la boucle')
    for fichier in chemin_fichiers_mails:
        m = Objet_mail(str(fichier) )
        logger.debug('creation de l objet mail de caracteristiques: {}'.format(repr(m)))
                   
        with open(str(fichier),'rb') as f:
            session.add(Emails(
                fichier_email=f.read(),
                nom_fichier_mail=fichier.name,
                chemin_fichier_mail = str(fichier),
                date_objet_mail = m.getDate(),
                nb_pj = m.getAttachmentCount()
                    )
                        )
    session.flush()
    logger.debug('insert_mails : flush effectue. les donnees devraient persister')
    logger.info('insertion de {} enregistrements'.format(session.query(Emails).count()))
            

def lire_mails(*args, **kwargs):
    pass
    
def insert_attachments(*args, **kwargs):
    try:
        if not session:
            raise ValueError('la session n existe pas')
    except ValueError as v1:
        print(v1.args[0])
        raise ValueError('la session n existe pas')
    try:
        if session.query(Emails).count() < 10:
                raise ValueError('les enr n existent pas. avez vous flushe les donnees?')
    except ValueError as v2:
        print(v2.args[0])
        raise ValueError('les enr n existent pas. avez vous flushe les donnees?')
    
    logger.debug('la session exise et il y a plus de 10 mails en base. on peut chch les pj')
    logger.debug('il y a {} messages comportant des pieces jointes'.format(session.query(Emails).filter(Emails.nb_pj > 0).count()))
    for Objet_mailSqlAlchemy in session.query(Emails).filter(Emails.nb_pj > 0):
        m = Objet_mail(Objet_mailSqlAlchemy.chemin_fichier_mail)
        #TODO:creer un rep nom_mail prive de eml
        for pj in m.getAllAttachments():
            logger.debug('entree ds attachment: {}'.format(pj.nom_fichier_attachment))
            
#             logger.debug('je cree un repertoire nomme {}'.format(Path(ml.chemin_fichier_mail).stem))
#             Path(
#                 Path(ml.chemin_fichier_mail).stem
#                 ).mkdir(exist_ok=True)
            logger.debug('j ajoute les champs necessaire dans la base')
            session.add(Attachments(
                fichier_attachment = pj.getRawData(),
                nom_fichier_attachment = pj.getFileName(),
                type_attachment = pj.getFileType(),
                nb_pages = pj.getParser(pj.getFileType()).parse(pj.getRawData()).getNumberOfPages(),
                emails_id = Objet_mailSqlAlchemy.id
                ))
        
#print(session.query(Documents).all())       
insert_mails()
#print("{} mails ont 0 pj".format(session.query(Emails).all()))
insert_attachments()
