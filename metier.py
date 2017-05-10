""" contient les objets metier cad la description d une
-Entree Planning
- jourTravaille

et ce que je trouverai pertinent ensuite"""
class Entree(object):
    
    """{'day': 13, 'month': 12, 'year': 2014, 'poste': 'P1'}
une entree est une a deux dates et un un type de pose et
une categorie de poste il a la responsabilite de renvovyer une representation
exte et qqch qui lui permettra d etre envoye et retour dans la base de donnees"""
    import constantes
    import datetime
    def __init__(self,ligne_poste):
        self.ligne_poste = ligne_poste
        self.setNomPoste()
        self.setDebutPoste()
        self.setFinPoste()
        self.setCategorie()

    def getLignePoste(self):
        return self.ligne_poste

    def getYear(self):
        return self.getLignePoste()['year']

    def getMonth(self):
        return self.getLignePoste()['month']

    def getDay(self):
        return self.getLignePoste()['day']

    def setNomPoste(self):
        self.nom_poste = self.getLignePoste()['poste']

    def getNomPoste(self):
        return self.nom_poste

    def getHeureDebut(self):
        return self.constantesGetHeureDebutFromNomPoste(self.getNomPoste())

    def constantesGetHeureDebutFromNomPoste(self,nomposte):
        import constantes
        return constantes.postes[nomposte]['heure_debut']

    def setDebutPoste(self):
        import datetime
        
        date_debut_poste = datetime.date(
            self.getYear(),
            self.getMonth(),
            self.getDay()
            )                                        
        heure_debut_poste = datetime.time(self.getHeureDebut())
        self.debut_poste = datetime.datetime.combine(date_debut_poste,
                                                     heure_debut_poste)
    def getDebutPoste(self):
        return self.debut_poste

    def constantesGetDureeFromNomPoste(self,nomposte):
        import constantes
        return constantes.postes[nomposte]['duree']

    def getDureePoste(self):
        return self.constantesGetDureeFromNomPoste(self.getNomPoste())

    def setFinPoste(self):
        import datetime
        self.fin_poste = self.getDebutPoste() + datetime.timedelta(hours = self.getDureePoste())

    def getFinPoste(self):
        return self.fin_poste

    def setCategorie(self):
        self.categorie = self.constantesGetCategorieFromNomPoste(self.getNomPoste())

    def constantesGetCategorieFromNomPoste(self, nomposte):
        import constantes
        return constantes.postes[nomposte]['categ']

    def getCategorie(self):
        return self.categorie
    
    def representation(self):
        return "{},{},{}, {}".format(self.getDebutPoste(), self.getFinPoste(), self.getNomPoste(), self.getCategorie())

    def to_dict(self):
        return { 'debut_poste' : self.getDebutPoste(), 'fin_poste' : self.getFinPoste(), 'nom_poste' : self.getNomPoste(), 'categorie' : self.getCategorie() }

    def to_tuple(self):
        return ( self.getDebutPoste(), self.getFinPoste(), self.getNomPoste(), self.getCategorie() )

    
        


class Regle(object):
    """ a la responsabilité:
- de creer une regle sous forme de champ d init dans fpaie reelle
- de creer un seuil
- de calculer le delta
- de chiffrer le delta
"""


    
                
                
        
    
    



class jourTravaille(object):
    """ doit representer la pkus petite
unite dont sont composees
les semaines 39 (dc besoin num sem
et num mois)
et les annees annu (ts jrs depuis 1er 
jan au 31 dec)
liste de periodes de trav (deb fin)
sur 24h
-connait le num de sem auquel il 
appartient
-connait le num mois auquel il 
appartient
    		- connait le num annee ausuel il 
    		appartient
"""
    
    pass

class semaineTravaillee(object):
    """pour les 39h regroupe les jours
travaillés de la semaine
chaque semaine comporte 7 jours
et doit etre rattachee a un mois.
cas limite: la semaine a cheval 
sur deux mois. doit elle etre rattachee
au mois ou elle commence ou au mois ou elle
se termine?
1er cas alors il faut inclure la semaine
de postes pas terminee au 31 dec
et exclure la 1ere semaine de jan
si elle est incomplete (commence pas par
	lundi).
2eme cas alors il faut inclure a la
1ere semaine de janvier, incomplete,
les jours de la dern sem de dec, incomplete
en effet annee du 1er jan au 31 dec.
donc exclusion des sem incomplete au 31
de l annee en cours
donc regul sur mois annee suivante
donc regul prec rattache au mois de janvier
"""
    pass
