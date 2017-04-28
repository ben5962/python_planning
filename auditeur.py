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
    """
    def __init__(self,annee):
        self.setAnnee(annee)
        self.setBdd()
        

    def setBdd(self):
        self.bdd = bdd()
        
    def setAnnee(self, annee):
        self.annee = annee

    def getAnnee(self):
        return self.annee
        
    def getBdd(self):
        return self.bdd

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

    def _deleguer_travail_verif(self):
        month_range = range (1,13)
        
        for month in month_range:
            self.setMois(month)
            
            self.rapporter(self.renvoyer_entete_rapport())
            for tache in self.getBdd().getListeNomsEtapesVerificationMensuelle():
                assistant_comptable = Larbin()
                assistant_comptable.setAnnee(self.getAnnee())
                assistant_comptable.setMois(self.getMois())
                # assistant comptable va le saisir dans la bd des anomalies
                assistant_comptable.setAnomalies(tache)

    def _deleguer_travail_saisie(self):
        secretaire = Secretaire()
        secretaire.setAnnee(self.getAnnee())
        secretaire.creerRapport()
        for type_rapport in bdd.getTypesAnomalies(self.getAnnee()):
            secretaire.setTypeRapport(type_rapport)
            secretaire.ajouterAuRapport(self.getAnnee(),self.getTypeRapport())
        secretaire.fermerRapport()       
            

    def auditer(self):
        """ lance les taches de verif de fiches de paye sur l annee"""
        # liste_annees = bdd.getListeAnneesDispo() # pour patron, ca.
        self._deleguer_travail_verif()
        self._deleguer_travail_saisie()


        
            
            
            
                
        
            
            
