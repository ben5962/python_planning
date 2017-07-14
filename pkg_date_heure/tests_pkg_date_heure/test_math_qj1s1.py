'''
Created on 7 juil. 2017

@author: Utilisateur
'''
import unittest
from pkg_date_heure import math_date

import calendar 
from _datetime import date
# http://eli.thegreenplace.net/2014/04/02/dynamically-generating-python-test-cases
class TestContainer(unittest.TestCase):
# echantillon de tests: https://fr.wikipedia.org/wiki/Semaine_1
    longMessage = True


def make_test_function(date_attendue, a,m,j,description):
    def test_repetitif_qj1s1(self):
        ladate = math_date.Date(a,m,j)
        #ladate.setObjetCalculJour(math_date.CalculJourLundiADimanche)
        self.assertEqual(ladate.qj1s1(), date_attendue,description)
    return test_repetitif_qj1s1
        

        
        

        
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    testEchantillons = {
        'j1s12009': [date(2008,12,29),2009,1,1],
        'j1s12010' : [date(2010,1,4),2010,1,1],
        'j1s12011' : [date(2011,1,3),2011,1,1]
        }
    for name, params in iter(testEchantillons.items()):
        test_func = make_test_function(params[0], params[1], params[2], params[3],name)
        setattr(TestContainer, 'test_{0}'.format(name), test_func)
    
    
    unittest.main()