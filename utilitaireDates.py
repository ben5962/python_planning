import calendar
import datetime
import devpy.develop as log

def contrainte(e,mn, mx):
    """vérifie que e est bien dans dans l'intervalle mn mx """
    log.info("lancement de contrainte avec e = {} de type{}, mn = {} de type{}, mx= {} de type {}".format(e, type(e), mn, type(mn), mx, type(mx)))
    if e < mn or e > mx:
        raise ValueError('valeur hors de l intervalle ', e, mn, mx)

def _acces_nb_jours(liste):
    return liste[1]

def nb_jours_of_month(aaaa,m):
    contrainte(aaaa, 2010, 2020)
    contrainte(m, 1, 12)
    return _acces_nb_jours(calendar.monthrange(aaaa,m))

def date_dernier_jour_mois(aaaa,m):
    contrainte(aaaa, 2010, 2020)
    contrainte(m, 1, 12)
    
    return datetime.date(aaaa,
                         m,
                         nb_jours_of_month(aaaa,m)
                         )


def _acces_derniere_semaine(liste):
    return liste[-1]

def _acces_dernier_jour_semaine(liste):
    return liste[-1]

def _acces_premier_jour_semaine(liste):
    return liste[0]

def listes_dates_semaines_commencees_ou_terminees_du_mois(aaaa,m):
    return calendar.Calendar().monthdatescalendar(aaaa,m)


def _acces_num_semaine(liste):
    return liste[1]

def _acces_annee(liste):
    return liste[0]

def annee(une_date):
    return _acces_annee(une_date.isocalendar())

def numero_semaine(une_date):
    return _acces_num_semaine(une_date.isocalendar())

def iter_semaine_comptable_de_mois(aaaa,m):
    """seulement les semaines terminées dans le mois -> (aaaa, num_sem)"""
    contrainte(aaaa, 2010,2020)
    contrainte(m, 1,12)
    for liste_dates_semaine in listes_dates_semaines_commencees_ou_terminees_du_mois(aaaa,m):
        if _acces_dernier_jour_semaine(liste_dates_semaine) < date_dernier_jour_mois(aaaa,m):
            yield (annee(
                _acces_premier_jour_semaine(liste_dates_semaine)
                ),
                numero_semaine(
                _acces_premier_jour_semaine(liste_dates_semaine)
                ))

def iterSemaine(aaaa,m):
    """seulement les semaines terminées dans le mois  -> num_sem"""
    aaaa = int(aaaa)
    contrainte(aaaa, 2010,2020)
    contrainte(m, 1,12)
    for liste_dates_semaine in listes_dates_semaines_commencees_ou_terminees_du_mois(aaaa,m):
        if _acces_dernier_jour_semaine(liste_dates_semaine) < date_dernier_jour_mois(aaaa,m):
            yield numero_semaine(
                _acces_premier_jour_semaine(liste_dates_semaine)
                )                   


##def 
##
##        import datetime
##        import calendar
##        cal = calendar.Calendar()
##        return ((semaine[0].isocalendar()[0],semaine[0].isocalendar()[1])
##                for semaine
##                in cal.monthdatescalendar(self.annee,self.mois)
##                if semaine[6] <= datetime.date(self.annee,
##                                               self.mois,
##                                               calendar.monthrange(self.annee,self.mois)[1]
##                                               )
##                )

