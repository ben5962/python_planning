'''
Created on 22 juil. 2017

@author: Utilisateur
'''
import unittest

from pkg_date_heure.math_date import isoweek
import datetime
class Test(unittest.TestCase):


    def testIsoweekIntegre(self):
        self.assertEqual(isoweek(datetime.date(2016,1,1)),datetime.date(2016,1,1).isocalendar()[1])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()