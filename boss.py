import auditeur
import 
class boss(object):
    """decide sur quelle annee(s) l audit de fiche de paie sera
lancee"""

    def setAnnees(self, *annees):
        if not hasattr(self, annees):
            self.annees = []
        self.annees = list(annees)

    def getAnnees(self):
        if not hasattr(self,annees):
            raise AttributeError("avant d appeler doit lancez setAnnees sinon self.annees existe pas")
        else:
            return self.annees

    def doit(self):
        for annee in self.getAnnees():
            p_et_g = auditeur.Auditeur(annee)
            p_et_g.auditer()
            
        
