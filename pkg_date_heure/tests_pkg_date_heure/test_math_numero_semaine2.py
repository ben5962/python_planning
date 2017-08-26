'''
Created on 7 juil. 2017

@author: Utilisateur
'''
import unittest
from pkg_date_heure import math_date

import calendar 
# http://eli.thegreenplace.net/2014/04/02/dynamically-generating-python-test-cases
class TestContainer(unittest.TestCase):
# echantillon de tests: https://fr.wikipedia.org/wiki/Semaine_1
    longMessage = True


def make_test_function(num_attendu, a,m,j,description):
    def test_repetitif_NumeroSemaine(self):
        ladate = math_date.Date(a,m,j)
        ladate.setObjetCalculJour(math_date.CalculJourLundiADimanche)
        self.assertEqual(ladate.numerosemaine(), num_attendu,description)
    return test_repetitif_NumeroSemaine
        

        
        

        
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    testEchantillons = {
        'numeroSemaine1erJanvier2009': [1,2009,1,1],
        'numeroSemaine4janvier2009' : [1,2009,1,4],
        'numeroSemaine5janvier2009' : [2,2009,1,5],
        'numeroSemaine1janvier2017' : [52, 2017,1,1],
        'numeroSemaine1janvier2016' : [53, 2016, 1,1]
        }
    for name, params in iter(testEchantillons.items()):
        test_func = make_test_function(params[0], params[1], params[2], params[3],name)
        setattr(TestContainer, 'test_{0}'.format(name), test_func)
    
    
    unittest.main()