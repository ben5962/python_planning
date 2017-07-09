'''
Created on 6 juil. 2017

@author: Utilisateur
'''
import unittest
from pkg_date_heure import math_date

import calendar


class Test(unittest.TestCase):





    # test numero jour independamment mode de calcul
    def repetitif_numero_jour(self, numerojour, a, m, j, typeObjetCalcul):
        ladate = math_date.Date(a,m,j)
        ladate.setObjetCalculJour(typeObjetCalcul)
        self.assertEqual(numerojour, ladate.numerojour)

    #  test numero jour premier mode de calcul
    def repetitif_numero_jour_dimanchealundi(self, numerojour, a, m, j):
        self.repetitif_numero_jour(numerojour, a, m, j, math_date.CalculJourDimancheALundi)



    def test_numerojour_Lundi3Juillet2017_dimanchealundi(self):
        """on s attend à récuperer la position correspondant à un lundi.
            comme cet algo prend dimanche = °0 lundi = 1 il faut corriger de 1
            la convention de calendar qui prend lundi = 0 mardi = 1... """
        self.repetitif_numero_jour_dimanchealundi((calendar.MONDAY + 1) %7,2017,7,3)
        
    

    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
