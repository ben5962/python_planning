#-*-coding:utf8;-*-
from metier import Entree

class larbin (object):
    """a la resp de
    1) remplir la base de postes
    depuis les fichiers texte
    -> fait
    2) a la resp de remplir la base
    de fiches de p reelles
    3) a la resp de convertir depuis la base les postes en journees trav
    -> fait (délégué au trigger)
    4) a la resp de remplir la base de journees travaillees
    """
    def __init__(self,bdd=None):
        self.setBdd(bdd)

   


    def setBdd(self,bdd):
        if bdd is not None:
            self.bdd = bdd
        else:
            from db import bdd
            self.bdd = bdd()

    def getBdd(self):
        if hasattr(self,'bdd'):
            return self.bdd
        else:
            self.setBdd()
            return self.bdd        

    



    def gen_tuple_entree_ite(self):
        import xpld
        for ligne_fichier in self.getBdd().iterLignesFichiersPostes():
            for ligne_poste in xpld.xpld().xplode_ite(ligne_fichier):
                yield Entree(ligne_poste).to_tuple()

    def saisir(self):
        for tuple_entree in self.gen_tuple_entree_ite():
            self.getBdd().saisir_entree(tuple_entree)
        self.getBdd().valider()
        #self.getBdd().saisirToutesEntrees(self.gen_tuple_entree_ite())
        self.getBdd().verifier_travail_saisie_planning()
        self.getBdd().verifier_travail_saisie_periodes_travaillees()
        
        





        


