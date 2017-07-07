#-*-coding:utf8;-*-
class auditeur  (object):
    """a la rep de lancer sur l annee demandee
    une verif des fiches de paye mensuelles.
    - chaque verif de fiche de paye se compose d etapes fournies
    par bdd.getEtapesVerificationMensuelle()
    - comme l annee et le mois ne sont connus qu'à l interieur d auditeur,
    il faut modifier la valeur de annees et de mois de etapeverif au runtime.
    pas tres tres malin car instanciation à deux endroits
    mais pas mieux pour l instant.
    peut etre déplacer l instanciation dans auditeur?



    mode emploi: a = auditeur(annee) ou a = auditeur(annee, inst_de_bdd)
    a.auditer()
    """
    def __init__(self,annee,bdd=None):
        self.setAnnee(annee)
        # l inst d' objet bdd() peut etre passée par un tiers, notamment boss
        # comme cela une seule instance de bdd()
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

   
        
    def setAnnee(self, annee):
        self.annee = annee

    def getAnnee(self):
        return self.annee
        

    def setMois(self,mois):
        self.mois = mois

    def getMois(self):
        return self.mois

    def renvoyer_entete_rapport(self):
        return ''.join(["vérif fiche paye mois ", str(self.getMois()),
                        " annee ", str(self.getAnnee())])

    def rapporter(self,chaine):
        """ doit rapporter.
pour l isntrant print. peut etre TODO logger.log"""
        print(chaine)

    def iterMois(self):
        month_range = range (1,13)
        return month_range


    def setObjetRapport(self):
        """met un objet rapport odf dansl e contexte commun
        - parce  que plus pratique à manipuler"""
        if self.getTypeSortie() == 'odf':
            pass
            #self.Rapport = odfpy_wrapper.Rapport(self.getNomFichierDestination())
        if self.getTypeSortie() == 'text':
            pass # trouver une representation arborescente à la con

    def getObjetRapport(self):
        return self.Rapport

    def r(self):
        return self.getRapport()

##    def _deleguer_travail_verif(self):
##        month_range = range (1,13)
##        
##        for month in self.iterMois():
##            self.setMois(month)
##            
##            self.rapporter(self.renvoyer_entete_rapport())
##            for tache in self.getBdd().iterNomsEtapesVerificationMensuelle():
##                assistant_comptable = Larbin()
##                assistant_comptable.setAnnee(self.getAnnee())
##                assistant_comptable.setMois(self.getMois())
##                # assistant comptable va le saisir dans la bd des anomalies
##                assistant_comptable.setAnomalies(tache)
##
##    def _deleguer_travail_saisie(self):
##        secretaire = Secretaire()
##        secretaire.setAnnee(self.getAnnee())
##        secretaire.creerRapport()
##        for type_rapport in bdd.getTypesAnomalies(self.getAnnee()):
##            secretaire.setTypeRapport(type_rapport)
##            secretaire.ajouterAuRapport(self.getAnnee(),self.getTypeRapport())
##        secretaire.fermerRapport()       
    def setTypeSortie(self,chaine):
        self.typeSortie = self.getBdd().creerTypeSortieParNom(chaine)

    def getTypeSortie(self):
        return self.typeSortie

    def auditer(self):
        """ lance les taches de verif de fiches de paye sur l annee"""
        # liste_annees = bdd.getListeAnneesDispo() # pour patron, ca.
        self.setTypeSortie('odf')
        self.setObjetRapport()
        for NomTache in self.getBdd().iterNomTache(): 
            t = self.getBdd().creerTypeTacheParNom(NomTache, self.getTypeSortie(),self.getObjetRapport(), self.getAnnee()).ajouterAuRapport()
        
            
        self._deleguer_travail_verif()
        self._deleguer_travail_saisie()


        
            
            
            
                
        
            
            
