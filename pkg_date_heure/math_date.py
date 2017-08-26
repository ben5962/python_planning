# coding: utf-8
'''
Created on 6 juil. 2017

@author: Utilisateur
'''

import datetime

creedate = datetime.date


import locale
import calendar
locale.setlocale(locale.LC_ALL, '')




from pkg_date_heure.pkg_Calculer_jour.calcul_jour_dimanche_a_lundi import CalculJourDimancheALundi
from pkg_date_heure.pkg_Calculer_jour.calcul_jour_lundi_a_dimanche import CalculJourLundiADimanche

def Quantieme(unedate):
    try:
        variable_temoin = unedate.year
        liste_noms_mois = list(calendar.month_name)
        duree = [0, 31, 28, 31, 30, 31,30, 31, 31, 30, 31, 30, 31]
        if calendar.isleap(unedate.year):
            duree[liste_noms_mois.index('février')] = 29
        q = unedate.day
        index_mois_debut = liste_noms_mois.index('janvier')
        index_mois = index_mois_debut
        while index_mois < unedate.month:
            q = q + duree[index_mois]
            index_mois = index_mois + 1
        return q
    except AttributeError:
        print("quantieme prend une date")
        raise AttributeError

class Date(object):
    def __init__(self,a=None,m=None,j=None,ladate=None):
        if (a is not None) and (m is not None) and (j is not None):
            self.date = creedate(a,m,j)
            self.j = j
            self.m = m
            self.a = a
        else:
            if (a is None) or (m is None) or (j is None) and ladate is not None:
                self.date = ladate
                self.j = int(self.date.strftime('%d'))
                self.m = int(self.date.strftime('%m'))
                self.a = int(self.date.strftime('%Y'))
            else:
                raise ValueError("soit une date soit un triplet a m j")
        
        self.setObjetCalculJour()



    def setObjetCalculJour(self,objetCalculJour=CalculJourLundiADimanche):
        self.creeObjetCalculJour = objetCalculJour
        print(self.creeObjetCalculJour)
        # ces éléments doivent etre recalculés à chaque mise à jour de 
        # objetCalculJour
        
        self.numerojour = self.calculerjour()

        self.nomjour = self.nomJour()
        self.quantieme = self.Quantieme()

    def calculerjour(self):
        """Algorithme de Mike Keith wikipedia.
        0 = dimanche
        1 = lundi....
        """
        
        objet_calcul = self.creeObjetCalculJour(self.a,self.m, self.j)
        d = objet_calcul.calcul()
        return d





    def nomJour(self):
        """ calculer jour : 0 -> dimanche 1->lundi, .. , 6-> samedi
            calendar.day_name: 0 -> lundi 1->mardi, ..., 6-> dimanche.
            donc afficher les jours localisés grâce à locale et calendar.day_name.
            comme 1-> lundi  doit devenir 0 alors self.numerojour -1
            comme 0-> dimanche doit devenir 6 (alors self.numero jour - 1) % 7
            ! todo : tester avec un dimanche !!!"""
        if self.creeObjetCalculJour is CalculJourDimancheALundi:
            return list(calendar.day_name)[int((self.numerojour - 1) % 7)]
        if self.creeObjetCalculJour is CalculJourLundiADimanche:
            return list(calendar.day_name)[int(self.numerojour)]




    def Quantieme(self):
        mois = list(calendar.month_name)
        duree = [0, 31, 28, 31, 30, 31,30, 31, 31, 30, 31, 30, 31]
        if calendar.isleap(self.a):
            duree[mois.index('février')] = 29
        q = self.j
        index_mois_debut = mois.index('janvier')
        index_mois = index_mois_debut
        while index_mois < self.m:
            q = q + duree[index_mois]
            index_mois = index_mois + 1
        return q
    
    def numerosemaine(self):
        """ une semaine commence un lundi en semaine iso 8601.
        la semaine 1 est la semaine contenant le 4 janvier.
        (la semaine dont le lundi est compris entre le 29 déc et le 4 janvier ts deux inclus)
        pour trouver un numero de semaine, il faut se ramener au lundi de la semaine du 4 janvier de l'année,
        récupérer son quantième dans l'année: c'est le quantième de la semaine 1
        il faut ensuite récupérer le quantieme du lundi de la semaine recherchée:
        c'est le quantieme de la semaine n.

        le numero de semaine de la semaine n doit valloir
        * en supposant que semaine 1 commence lundi 1er janvier
        * soit qs1 le quantieme du 1er lundi
         - qs1 = 1.   qs2 = 1 + 7 qs3 = 1 + 2x7 ... qsn = 1 + (n -1) x 7
        * en supposant que la semaine 1 commence le 3 janvier:
         - qs1 = 3,   qs2 = qs1 + 7, qs3 = qs1 + 2x7... qsn = qs1 + (n - 1 ) x 7
         ainsi j'obtiens la formule générale :
         n = (qj1sn - qj1s1) / 7 + 1.
         ca ne marche que si le premier lundi de l'année iso se trouve entre le 1er
         et le 4 janvier.
        * reste à déterminer la date du début de la s1 "qj1s1":
        7 cas:
         - qj1s1 = 4 si 1er janvier est un vendredi (1 - jsem1erJan 4) = -3 %7 = +4
         - qj1hs1 = 3 si 1er janvier est un samedi (1 - jsem1erjan? 5) = -4 %7 = +3
         - qj1s1 = 2 si 1er janvier est un dimanche (1 - jsem1erJan? 6) = -5 M%7 = +2
         - qj1s1 = 1 si 1er janvier est un lundi. ben (1 - jsem1erJan)
         - qj1s1 = 0 si 1er janvier est un mardi donc lundi 31 décembre (1 - jsem1erJan )
         - qj1s1 = - 1 si 1er janvier est un mercredi donc lundi 30 déc (1 - jsem1erJan)
         - qj1s1 = -2 si 1er janvier est un jeudi donc lundi 29 déc (1 - jsemjan)
        ca marche?
        qs2 si qs1 = - 2 vaut - 2 + 7 = 5 janvier.
        une semaine appartient toute entière à une année iso.
        une année iso a 52 ou 53 semaine entieres 364 ou 371 jours"""
        
        #         """
        #         7/7/17 : BUG 
        #         FAIL: test_numeroSemaine5janvier2009 (__main__.TestContainer)
        #         ----------------------------------------------------------------------
        #         Traceback (most recent call last):
        #           File "C:\Users\Utilisateur\git\python_planning\pkg_date_heure\test_math_numero_semaine2.py", line 20, in test_repetitif_NumeroSemaine
        #         self.assertEqual(ladate.numerosemaine(), num_attendu,description)
        #         AssertionError: 1.0 != 2 : numeroSemaine5janvier2009"""
        
        
        # bug : 22 juillet 2017
        #         ======================================================================
        # FAIL: test_numeroSemaine1janvier2017 (__main__.TestContainer)
        # ----------------------------------------------------------------------
        # Traceback (most recent call last):
        #   File "C:\Users\Utilisateur\git\python_planning\pkg_date_heure\tests_pkg_date_heure\test_math_numero_semaine2.py", line 20, in test_repetitif_NumeroSemaine
        #     self.assertEqual(ladate.numerosemaine(), num_attendu,description)
        # AssertionError: 0.0 != 52 : numeroSemaine1janvier2017
        # 
        # ----------------------------------------------------------------------
        # Ran 4 tests in 0.013s
        # 
        # FAILED (failures=1)

        self.setObjetCalculJour(objetCalculJour=CalculJourLundiADimanche)
        qj1sn = self.quantieme - self.numerojour
        premier_jan = Date(self.a, 1, 1)
        
        tmp = 1 - premier_jan.numerojour
        if tmp % 7 > 4:
            qj1s1 = tmp
        else: 
            qj1s1 = tmp % 7
            
        n = (qj1sn - qj1s1) / 7   + 1
        if n < 1:
            quantieme = Quantieme(datetime.date(self.a - 1, 12, 31)) + self.quantieme
            qj1sn = quantieme - self.numerojour
            premier_jan = Date(self.a - 1, 1, 1)
            tmp = 1 - premier_jan.numerojour
            if tmp % 7 > 4:
                qj1s1 = tmp
            else: 
                qj1s1 = tmp % 7
            
                n = (qj1sn - qj1s1) / 7   + 1
            return int(n)
        else:
            return int(n)
    
    def calc_qj1s1(self, annee = None):
        if annee is None:
            annee = self.a
        premier_jan = Date(annee, 1, 1)
        
        tmp = 1 - premier_jan.numerojour
        if tmp % 7 > 4:
            qj1s1 = tmp
        else: 
            qj1s1 = tmp % 7
        return int(qj1s1)

    def jourdatepremierjanvier(self):
        annee_premier_jan = self.date.year
        premier_jan = Date(annee_premier_jan,1,1)
        return premier_jan.nomjour
    
    def anneeiso(self):
        """annee sauf dans les cas limites:
        - date > 31 dec et < 1er jour année iso suivante alors  anneeiso = annee - 1
        - date < 31 dec et > 1er jour annee iso suivante alors anneeiso = annee + 1
        prendre annee si mois = tout sauf janvier et décembre
        pour décembre, si date > date_1er_jour_anneeisosuivante alors annee + 1 sinon annee
        pour janvier, si date < date_1er_jour_anneeiso alors annee - 1"""
        if self.a in [1,12]:
            if self.m == 1:
                if self.date < self.datepremierjouranneeiso(self.a):
                    return self.a - 1
                else:
                    return self.a
            else:
                if self.m == 12:
                    if self.date > self.datepremierjouranneeiso(self.a + 1):
                        return self.a + 1
                    else:
                        return self.a
                else: 
                    raise ValueError("le mois vaut forcémetn 1 ou 12 dans cette partie de code")
        else:
            return self.a
        
    def datepremierjouranneeiso(self, annee=None):
        """        * reste à déterminer le quantieme du début de la s1 "qj1s1":
        7 cas:
         - decl 3 qj1s1 = 4 si 1er janvier est un vendredi (1 - jsem1erJan 4) = -3 %7 = +4
         - decl 2 qj1hs1 = 3 si 1er janvier est un samedi (1 - jsem1erjan? 5) = -4 %7 = +3
         - decl 1 qj1s1 = 2 si 1er janvier est un dimanche (1 - jsem1erJan? 6) = -5 M%7 = +2
         - decl 0 qj1s1 = 1 si 1er janvier est un lundi. ben (1 - jsem1erJan)
         - decl -1 qj1s1 = 0 si 1er janvier est un mardi donc lundi 31 décembre (1 - jsem1erJan )
         - decl -2 qj1s1 = - 1 si 1er janvier est un mercredi donc lundi 30 déc (1 - jsem1erJan)
         - decl -3 qj1s1 = -2 si 1er janvier est un jeudi donc lundi 29 déc (1 - jsemjan)
         si date_1er_j_iso = date 1er jan + decl jours 
         """
        pass
        


def isoweek(d):
    return int(Date(ladate=d).numerosemaine())

def isoyear(d):
    return int(Date(ladate=d).anneeiso())


