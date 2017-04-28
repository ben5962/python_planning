# -*- coding: utf-8 -*-

import devpy.develop as log    
        



class Seuil(object):
    """ un seuil a pour resp de:
- connaitre une liste croissante de limites légales (liste st cte de nb heures)
- decouper une duree en heures avant et apres chaque seuil
dans le but de décompter les heures supplémentaires de chaque catégorie.
. utilisé pour les hsup 39 (plusieurs découpages)
. utilisé pour les hsupannu (un seul)
"""

    def __init__(self,*args):
        self.setSeuils(*args)

    def setSeuils(self,*args):
        """1ere resp"""
        """remplir la liste cstte de limites legales"""
        """ la liste doit etre exclusivement composee d entiers"""
        log.info("lancement de Seuils.setSeuils avec pour param {}".format(args))
        print("creation d un seuil depuis", args)
        for i in args:
            if type(i) is not type(1):
                print("type(", str(i), ") vaut: ", type(i))
                print("type(1) vaut:", type(1))
                raise TypeError
        """ la liste doit etre triee"""
        self.seuils = sorted(args)

    def getSeuils(self):
        return self.seuils

    def setIntervalles(self):
        """ [ 14, 28 ] -> [ 14, 14]
sera retranche de nb pour obtenir:
de 48,
[35, 43, 48] -> [35, 8, 5]
->  [35, 
"""
        print("creation d un intervalle depuis", self.getSeuils())
        self.intervalles = []
        for pos, val in enumerate(self.getSeuils()):
            if pos == 0: self.intervalles.append(val)
            else:
                intervalle_calcule = self.getSeuils()[pos] - self.getSeuils()[pos - 1]
                self.intervalles.append(intervalle_calcule)
                print("l intervalle produit estt: ", self.intervalles)

    def getIntervalles(self):
        if not hasattr(self,"intervalles"):
            self.setIntervalles()
        return self.intervalles

            

    def decouper(self, duree):
        """ doit decouper les durees en tranches inférieure et supérieure
a chaque intervalle"""
        self.setIntervalles()
        decoupe = []
        accu = duree
        print("lancement de decouper")
        for pos,intervalle in enumerate(self.getIntervalles()):
            """ algo : accu <- nb
pour chaque intervalle faire
accu  <- accu - intervalle. ainsi si accu est négatif, on a dépassé les seuils.
dans tous les cas renvoyer min(accu, intervalle)
si derniere position renvoyer max(accu, 0)
"""
            
            """cas 1 : decouper(15) avec [18] -> [15,0]"""
            """cas 2 : decouper(15) avec [10] ->  [10,5]"""
            
            """la premiere et deniere position de intervalles
                doivent etre traitees separement"""
            
            """premiere position"""
            """cas 1 : decouper(15) avec [18] -> [18,0]
            renvoyer 18
            accu : duree intervalle: 18 duree: 15
            cas où accu < intervalle
            renvoyer duree donc accu"""
            """cas 2 : decouper(15) avec [10] ->  [10,5]
                renvoyer 10.
                cas où accu > intervalle
                accu: duree intervalle: 10 duree: 15
                renvoyer intervalle"""
            """bilan des deux cas: renvoyer min(accu, intervalle)"""

            """ position entre la permiere et la derniere position"""
            """position générale : ni premier intervalle, ni dernier
            il faut donc ici des cas avec une liste d intervalles
            comportant au moins 3 éléments """
            """cas 3 : decouper(15) avec [18,1,5] -> [15,0]"""
            """ici 15 x 18 a donné 15
                accu : -3  intervalle: 1
                cas où accu n a plus rien à donner.
                renvoyer min(accu, intervalle) donnerait -3 je veux 0."""
            """cas 4 : decouper(15) avec [10,1,3] ->  [10,1,3,1]
                ici 15x10 a donné 10 reste 5.
                accu :  5 intervalle : 1
                renvoyer min(accu, intervalle) fonctionne."""
            """bilan des deux cas: renvoyer max(0,min(accu, intervalle))"""

            """bilan des 4 cas : renvoyer max(0, min(accu,intervalle))
                ne casse pas la mécanique des cas 1 et 2. on peut donc
                les regrouper."""
            print("position : ", str(pos), " intervalle: ", str(intervalle), " intervalles:" ,str(self.getIntervalles()))
            decoupe.append(max(0,min(accu,intervalle)))
            accu = accu - intervalle
            """derniere position de intervalles."""
            """cas 1 : decouper(15) avec [18] -> [18,0]"""
            if pos == len(self.getIntervalles()) - 1:
                """cas 1 : decouper(15) avec [18] -> [18,0]
                renvoyer 0
                accu < intervalle lors éch préc donc accu - interv <0.
                accu : -3 intervalle: NAPLUS duree: 15"""
                """cas 2 : decouper(15) avec [10] ->  [10,5]
                    renvoyer 10.
                    cas où accu > intervalle
                    accu < intervalle lors éch préc donc accu - interv >0.
                    accu: 5 intervalle: 10 duree: 15
                    renvoyer accu"""
                """bilan des deux cas: renvoyer le max de (0, accu)
                    passage à l étape suivante: comme pas d'étape suivante,
                    ne rien retrancher à accu. c est fini."""
                decoupe.append(max(0,accu))
        return decoupe
            
            
     
            

