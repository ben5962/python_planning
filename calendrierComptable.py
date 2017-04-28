#-*-coding:utf8;-*-
import calendar
import datetime



def toutesLesSemainesCommenceesOuTermineesDansLeMois(year, month):
    """ builtin renommee pour plus de clarte
renvoie les semaines commencees ou terminees dans le mois
brique de base pour consruire des mois comptables de semaines de
39h pour les heures sup. """
    cal = calendar.Calendar()
    return cal.monthdatescalendar(year, month)


def accesDerniereSemaine(ListeMensuelleDeListeDeSemaines):
    """ accede à la derniere semaine d une liste de semaine
permetra de verifier si la date du dernier jour de la derniere
semaine déborde. si c est le cas la tronquer.
"""
    return accesDernierElement(ListeMensuelleDeListeDeSemaines)

def accesDernierJourSemaine(ListeSemaine):
    """ accede au dernier jour d une semaine pour verfier si
le dernier jour d une liste de semaine deborde du mois"""
    return accesDernierElement(ListeSemaine)

def accesDernierElement(liste):
    return liste[-1]


def listeTousElementsSaufDernier(liste):
    """renvoie liste excluant le dernier element"""
    return liste[0:-1]

def dernierJourDuMois(year, month):
    """builin renomme pour plus de clarte
renvoie le dernier jour du mois saisi.
comme monthrange renvoie le jour du 1er jour et le nb de jour,
je ne prends que la deuxieme partie"""
    return accesDernierElement(calendar.monthrange(year,month))

def ExclureDerniereSemaine(ListeMensuelleDeListeDeSemaines):
    """renvoie la liste sans le dernier element pour produire un mois
comptable du point de vue des 39h:
- ensemble de semaines entieres puisque decompte heures sup à la semaine
- deborde avant : ok puisque decompte des heures sup lorsque semaine terminee.
- deborde apres exclus puisque semaine pas terminee
ici la logique se contente de l exclusion. rajouter un swith ensuite
"""
    return listeTousElementsSaufDernier(ListeMensuelleDeListeDeSemaines)

def getDateDernierJourMois(year,month):
    """cree une date depuis dernier jours du mois
sert à verifier si debordement à droite"""
    return datetime.date(year,month,dernierJourDuMois(year,month))



def predVerifierSiDebordement(year,month):
    """ renvoie vrai si debordement :
si derniere date de la listemensuelle de listeSemaines > derniere date du mois"""
    if getDateDernierJourMois(year,month) < accesDernierJourSemaine(
        accesDerniereSemaine(toutesLesSemainesCommenceesOuTermineesDansLeMois(year,month)
                             )
        ):
        print("debordement")
        return True
    else:
        print("pas de debordement")
        return False

def getSemainesMoisComptable39SansDepassementADroite(year,month):
    """renvoie mois  comptable de 39 sous forme de liste
de liste de semaines. exclue derniere semaine si débordement"""
    semainesMois = toutesLesSemainesCommenceesOuTermineesDansLeMois(year,month)
    if predVerifierSiDebordement(year,month):
        return ExclureDerniereSemaine(semainesMois)
    else:
        return semainesMois

def getNumeroDeJourFromDate(year, month, day):
    """wrapper d un builtin encore
recupere le numero de jour d une date
reste à le traduire
"""
    return calendar.weekday(year,month,day)


def getNumeroSemaine(y,m,d):
    """recupere le numero de semaine d une date"""
    return getIsoWeekNumber(y,m,d)

def getListeNumerosSemainesDuMoisComptable(year,month):
    """renvoie la liste des numeros de semaines iso8601
pour un mois comptable 39 souhaité.
"""
    debut = getNumeroSemaine(year,month,1)
    fin = getNumeroSemaine(year,month,dernierJourDumois(year,month))
    

def createBorneDebutSemaineFromIsoCalendar(annee, semaine):
    pass
                         

def createBornesDatesSemaineFromIsoCalendar(annee, semaine):
    """renvoie liste contenant le debut et la fin de semaine
d une semaine iso
"""
    pass

def getIsoWeekNumber(y,m,d):
    """renvoie numero de semaine iso d une date"""
    return datetime.date(y,m,d).isocalendar()[1]
    
    
    
    
