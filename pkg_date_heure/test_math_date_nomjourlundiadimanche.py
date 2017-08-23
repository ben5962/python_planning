'''
Created on 6 juil. 2017

@author: Utilisateur
'''
import unittest
from pkg_date_heure import math_date
import calendar


class Test(unittest.TestCase):

    #test independamment du mode de calcul
    def repetitif_nom_jour(self, nomjour,a,m,j,typeObjetCalcul):
        ladate = math_date.Date(a,m,j)
        #ladate.setObjetCalculJour(typeObjetCalcul)
        self.assertEqual(nomjour, ladate.nomjour)



    # deuxieme algo de calcul pour nom jour
    def repetitif_nom_jour_lundiadimanche(self,nomjour,a, m, j):
        self.repetitif_nom_jour(nomjour, a, m, j, math_date.CalculJourLundiADimanche)





    def test_nomjour_Lundi3Juillet2017_lundiadimanche(self):
        self.repetitif_nom_jour_lundiadimanche('lundi',2017,7,3)

    def test_nomjour_dimanche2Juillet2017_lundiadimanche(self):
        self.repetitif_nom_jour_lundiadimanche('dimanche', 2017, 7, 2)
        
    def test_nomjour_jeudi1erJanvier2009_lundiadimanche(self):
        """le 1er janvier 2009 est il bien un jeudi?"""
        self.repetitif_nom_jour_lundiadimanche('jeudi', 2009, 1, 1)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
