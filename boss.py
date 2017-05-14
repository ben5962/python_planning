#-*-coding:utf8;-*-
import auditeur

from db import bdd
import collections
class boss(object):
    """decide sur quelle annee(s) l audit de fiche de paie sera
lancee"""

    def __init__(self):
        self.setBdd()

    def setBdd(self):
        self.bdd = bdd()

    def getBdd(self):
        if hasattr(self,'bdd'):
            return self.bdd
        else:
            self.setBdd()
            return self.bdd

    def iterAnnees(self):
        """ renvoie de man iterative les annees dispo ds db"""
        generateur = self.getBdd().iterAnneesDisponibles()
        if isinstance(generateur(), collections.Iterable):
            return generateur()
        

    def doit(self):
        for tuple_annee in self.iterAnnees():
            annee = tuple_annee[0]
            p_et_g = auditeur.Auditeur(annee,bdd=self.getBdd())
            p_et_g.auditer()
            
        
