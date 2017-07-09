'''
Created on 7 juil. 2017

@author: Utilisateur
'''
import unittest
from pkg_date_heure import math_date

import calendar 
# http://eli.thegreenplace.net/2014/04/02/dynamically-generating-python-test-cases
class Test(unittest.TestCase):
# echantillon de tests: https://fr.wikipedia.org/wiki/Semaine_1

    def repetitif_NumeroSemaine(self,num_attendu,a,m,j):
        ladate = math_date.Date(a,m,j)
        
        ladate.setObjetCalculJour(math_date.CalculJourLundiADimanche)
        
        self.assertEqual(ladate.numerosemaine(), num_attendu)
        

        
        
    def testNumeroSemaine1erJanvier2009(self):
        """ le 1er janvier 2009 est un jeudi"""
        self.repetitif_NumeroSemaine(1,2009,1,1)
        
    def testNumeroSemaine4Janvier2009(self):
        """ en conséquence le 4 janvier 2009 est un dimanche"""
        self.repetitif_NumeroSemaine(1,2009,1,4)
        
    def testNumeroSemaine5Janvier2009(self):
        """en conséquence le 5 janvier 2009 commence s2"""
        self.repetitif_NumeroSemaine(2,2009,1,5)
        
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    
    unittest.main()