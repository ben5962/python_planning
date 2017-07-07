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
        ladate.setObjetCalculJour(typeObjetCalcul)
        self.assertEqual(nomjour, ladate.nomjour)

    # premier algo de calcul pour nom jour
    def repetitif_nom_jour_dimanchealundi(self,nomjour,a, m, j):
        self.repetitif_nom_jour(nomjour, a, m, j, math_date.CalculJourDimancheALundi)





    def test_nomjour_Lundi3Juillet2017_dimanchealundi(self):
        self.repetitif_nom_jour_dimanchealundi('lundi',2017,7,3)

    def test_nomjour_dimanche2Juillet2017_dimanchealundi(self):
        self.repetitif_nom_jour_dimanchealundi('dimanche', 2017, 7, 2)






if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
