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


    # test numero jour deuxieme mode de calcul

    def repetitif_numero_jour_lundiadimanche(self, numerojour, a, m, j):
        self.repetitif_numero_jour(numerojour, a, m, j, math_date.CalculJourLundiADimanche)
        
    def test_numerojour_Lundi3Juillet2017_lundiadimanche(self):
        """là on peut utiliser la meme convention que calendar: calendar.MONdDAY == 0 """
        self.repetitif_numero_jour_lundiadimanche(calendar.MONDAY,2017,7,3)




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
