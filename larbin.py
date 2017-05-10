import db
from metier import Entree

class larbin (object):
    """a la resp de
    remplir la base de postes
    depuis les fichiers texte
    a la resp de remplir la base
    de fiches de p reelles
    a la resp de converting depuis la base les postes en journees trav
    a la resp de remplir la base de journees travaillees
    """
    def __init__(self):
        self.bdd = db.bdd()

    def getBdd(self):
        return self.bdd
        

##    def getDb(self):
##        return self.db
##
##    def getBibliothecaireDba(self):
##        return self.bib
    
    def a_saisir(self):
        import xpld
        
        fichiers_larbin = ["2014.txt","2015.txt","2016.txt"]
        for fichier in fichiers_larbin:
            with open(fichier) as f:
                for ligne_fichier in f:
                    for ligne_poste in xpld.xpld().xplode_ite(ligne_fichier):
                        print(Entree(ligne_poste).representation())

    def a_saisir_test_dico(self):
        import xpld
        
##        fichiers_larbin = ["2014.txt","2015.txt","2016.txt"]
##        for fichier in fichiers_larbin:
##            with open(fichier) as f:
##                for ligne_fichier in f:
        for ligne_fichier in self.bdd.iterLignesFichiersPostes():
            for ligne_poste in xpld.xpld().xplode_ite(ligne_fichier):
                print(Entree(ligne_poste).to_dict())

    def gen_dico_entree_ite(self):
        import xpld
        
##        fichiers_larbin = ["2014.txt","2015.txt","2016.txt"]
##        for fichier in fichiers_larbin:
##            with open(fichier) as f:
##                for ligne_fichier in f:
        for ligne_fichier in self.bdd.iterLignesFichiersPostes():
            for ligne_poste in xpld.xpld().xplode_ite(ligne_fichier):
                yield Entree(ligne_poste)

    def gen_tuple_entree_ite(self):
        import xpld
        for ligne_fichier in self.bdd.iterLignesFichiersPostes():
            for ligne_poste in xpld.xpld().xplode_ite(ligne_fichier):
                yield Entree(ligne_poste).to_tuple()

    def saisir(self):
        self.getBdd().saisirToutesEntrees(self.gen_tuple_entree_ite())
        
        


    def test_saisir(self):
        for entree in self.gen_dico_entree_ite():
            print(entree.getDebutPoste(), entree.getFinPoste(), entree.getNomPoste(), entree.getCategorie())

    def verifier_travail(self):
        """verifie que le nombre de saisies dans la base n est pas nul"""
        tuple_resultat = self.getDb().getCnx().execute(self.getBibliothecaireDba()
                                    .getRequeteMetaByName('nombre_postes_saisis')
                                    ).fetchone()
        nb = tuple_resultat[0] #le nombre doit etre extrait du tuple
        for member in tuple_resultat:
            print("le nombre d elements de planning saisis est de : {}"
                  .format(nb)
                  )
        if nb:  #vrai si non nul
            return True
        else:
            return False
        

##Traceback (most recent call last):
##  File "<pyshell#38>", line 1, in <module>
##    a.saisir()
##  File "C:\Users\Utilisateur\Documents\GitHub\python_planning\db.py", line 430, in saisir
##    (entree.to_dict()['debut_poste'], entree.to_dict()['fin_poste'], entree.to_dict['nom_poste'],
##TypeError: 'method' object is not subscriptable
##>>> import sqlite3
##>>> a = sqlite3.connect(":memory:")
##>>> a.execute("create table essai (dt datetime)")
##<sqlite3.Cursor object at 0x02326C60>
##>>> a.commit()
##>>> import datetime
##>>> a = { le_datetime : datetime.datetime.now() }
##Traceback (most recent call last):
##  File "<pyshell#44>", line 1, in <module>
##    a = { le_datetime : datetime.datetime.now() }
##NameError: name 'le_datetime' is not defined
##>>> a = { "le_datetime" : datetime.datetime.now() }
##>>> a
##{'le_datetime': datetime.datetime(2017, 4, 15, 9, 8, 19, 169198)}
##>>> a = sqlite3.connect(":memory:")
##>>> a.execute("create table essai (dt datetime)")
##<sqlite3.Cursor object at 0x02326C20>
##>>> a.commit()
##>>> dico = { "le_datetime" : datetime.datetime.now() }
##>>> a.execute("insert into essai values (dt =: le_datetime) ", dico)
##Traceback (most recent call last):
##  File "<pyshell#51>", line 1, in <module>
##    a.execute("insert into essai values (dt =: le_datetime) ", dico)
##sqlite3.OperationalError: unrecognized token: ":"
##            
        
