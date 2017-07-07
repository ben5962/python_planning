""" contient les objets metier cad la description d une
-Entree Planning
- jourTravaille

et ce que je trouverai pertinent ensuite"""
from dateutil.relativedelta import *
from dateutil.parser import *
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

    
        
class moisCalendaire(object):
    """ le mois /d une annee/
    fournit itérateur sur les numeros de semaines:
     m = moisComptable(2014,1)
     for s in m.iterSemainesHsup30():
         print(s)
    #(2013, 53)
    # (2014, 1)
    # (2014, 2)
    #(2014, 3)"""
    def __init__(self, annee, num_mois):
        self.annee = annee
        self.mois = num_mois

    def iterSemainesHsup39(self):
        import datetime
        import calendar
        cal = calendar.Calendar()
        return ((semaine[0].isocalendar()[0],semaine[0].isocalendar()[1])
                for semaine
                in cal.monthdatescalendar(self.annee,self.mois)
                if semaine[6] <= datetime.date(self.annee,
                                               self.mois,
                                               calendar.monthrange(self.annee,self.mois)[1]
                                               )
                )


class semaineCalendaire(object):
    """ les bornes en date d une semaine /d une annee/
    fournit horodatage début et horodatage fin d une semaine:
    s = semaineCalendaire(2010,25)
    s.getHoroDebutEtHoroDebutSplus1BornantSemaine()
    ou:
    s = semaineCalendaire(2010,25).getBornesEnFrancais()
    # (datetime.datetime(2010,6,4,0,0,0),datetime.datetime(2010,6,11,0,0,0)
    la bornde de fin n est pas le dernier instant de la semaine mais
    le premier instant de la semaine suivante afin de partitionner le mois
    comptable"""
    def __init__(self, annee, num_semaine):
        self.annee = annee
        self.num_semaine = num_semaine

    def getHoroDebutEtHoroDebutSplus1BornantSemaine(self):
        """ doit fournir bornes d une semaine"""
        from datetime import datetime
        #from dateutil.relativedelta import * #remonté au module
        #from dateutil.parser import *        # remonté au module
        debut = datetime(self.annee,1,1) + relativedelta(
            day=4,  #la permiere SEMAINE ISO contient le 4 jan
            weekday=MO(-1), # rembobiner jusqu'au premier lundi de cette semaine iso
            weeks=+(self.num_semaine - 1)   # ajouter 19 semaines donc semaine 20
            )
        fin = debut + relativedelta(days=7)
        return (debut, fin)

    def getPremierEtDernierJourSemaine(self):
        """doit fournir bornes d une semaine """
        from datetime import timedelta
        bornes = self.getHoroDebutEtHoroDebutSplus1BornantSemaine()
        debut = bornes[0].date()
        fin = bornes[1].date() - timedelta(days=1)
        return (debut, fin)

    def getBornesEnFrancais(self):
        bornes = self.getHoroDebutEtHoroDebutSplus1BornantSemaine()
        ch = ' '.join([
            "du",
            date_en_francais(bornes[0]),
            "au",
            date_en_francais(bornes[1])
            ])
        return ch

def date_en_francais(la_date):
    """convertit une datetime en chaine en francais"""
    import locale
    locale.setlocale(locale.LC_ALL,'fra')
    import calendar
    """lundi"""
    nom_jour = calendar.day_name[
        calendar.weekday(
            la_date.year,
            la_date.month,
            la_date.day
            )
        ]
    "22"
    numero_ds_mois = str(la_date.day)
    "mai"
    nom_mois = calendar.month_name[la_date.month]
    "2017"
    annee = str(la_date.year)
    heure = str(la_date.hour)
    return ''.join([nom_jour," ", numero_ds_mois," ", nom_mois," ", annee, " ", heure, "h"])
    
        
def timedelta_to_hour(td):
    """prend un time delta renvoie un nb entier d heures.
        un time delta possede la méth total_seconds"""
    return td.total_seconds() / 3600

def diff_entre_deux_datestimes(d1,d2):
    """renvoie un timedelta de difference entre deux dates"""
    d1.hour
    d2.hour # si l un des deux échoue alors pas datetime
    return d2 - d1
        
 

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
