'''
Created on 6 juil. 2017

@author: Utilisateur
'''
import unittest
from pkg_date_heure import math_date
import calendar


# http://eli.thegreenplace.net/2014/04/02/dynamically-generating-python-test-cases
class TestContainer(unittest.TestCase):
# echantillon de tests: https://fr.wikipedia.org/wiki/Semaine_1
    longMessage = True


def make_test_function(numero_jour_attendu, a,m,j,description):
        # test numero jour independamment mode de calcul
#     def repetitif_numero_jour(self, numero_jour_attendu, a, m, j, typeObjetCalcul):
#         ladate = math_date.Date(a,m,j)
#         ladate.setObjetCalculJour(typeObjetCalcul)
#         self.assertEqual(numero_jour_attendu, ladate.numerojour, description)


    # test numero jour deuxieme mode de calcul

    def test_repetitif_numero_jour_lundiadimanche(self):
        ladate = math_date.Date(a,m,j)
        ladate.setObjetCalculJour(math_date.CalculJourLundiADimanche)
        self.assertEqual(numero_jour_attendu, ladate.numerojour, description)
        
        
    return test_repetitif_numero_jour_lundiadimanche

        

        
    
        
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    testEchantillons = {
        'numeroJour1erJanvier2009': [3,2009,1,1],
        'numeroJour4janvier2009' : [6,2009,1,4],
        'numeroJour5janvier2009' : [0,2009,1,5],
        'numeroJourlundi3juillet2017': [calendar.MONDAY, 2017,7,3],
        'numeroJourmardi1erjanvier2008': [calendar.TUESDAY, 2008,1,1],
        'numeroJourJeudi1erJanvier2009': [calendar.THURSDAY, 2009, 1, 1],
        'numeroJourvendredi1janvier2010': [calendar.FRIDAY, 2010, 1,1],
        'numeroJoursamedi1janvier2011' : [calendar.SATURDAY,2011,1,1],
        'numeroJourdimanche1Janvier2012': [calendar.SUNDAY, 2012,1,1],
        'numeroJourmercredi1erJanvier2014': [calendar.WEDNESDAY, 2014,1,1]
        }
    for name, params in iter(testEchantillons.items()):
        test_func = make_test_function(params[0], params[1], params[2], params[3],name)
        setattr(TestContainer, 'test_{0}'.format(name), test_func)
    
    
    unittest.main()


