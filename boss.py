import auditeur
import db
from db import bdd
import collections
class boss(object):
    """decide sur quelle annee(s) l audit de fiche de paie sera
lancee"""

    

    def iterAnnees(self):
        """ renvoie de man iterative les annees dispo ds db"""
        generateur = bdd.iterAnneesDisponibles()
        if isinstance(generateur(), collections.Iterable):
            return bdd.iterAnneesDisponibles()
        

    def doit(self):
        for tuple_annee in self.iterAnnees():
            annee = tuple_annee[0]
            p_et_g = auditeur.Auditeur(annee)
            p_et_g.auditer()
            
        
