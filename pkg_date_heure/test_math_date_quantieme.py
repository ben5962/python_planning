'''
Created on 6 juil. 2017

@author: Utilisateur
'''
import unittest
from pkg_date_heure import math_date

import calendar


class Test(unittest.TestCase):




    def repetitif_quantieme(self, quantieme, a, m, j):
        ladate = math_date.Date(a,m,j)
        ladate.setObjetCalculJour(math_date.CalculJourLundiADimanche)
        self.assertEqual(quantieme, ladate.quantieme)

    def test_1erJanvier2017(self):
        self.repetitif_quantieme(1, 2017, 1, 1)

    def test_1erfervrier2017(self):
        self.repetitif_quantieme(32, 2017, 2, 1)

    def test_31dec2017(self):
        self.repetitif_quantieme(365, 2017, 12, 31)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
