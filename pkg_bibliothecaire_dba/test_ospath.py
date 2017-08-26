'''
Created on 22 juil. 2017

@author: Utilisateur
'''
import unittest

import glob 
import os.path 
from pkg_utilitaires_repertoires.glob_etc import *

class Test(unittest.TestCase):


    def testTypeRequetePrendBienCaracteresAvantPremier_(self):
        nom_fichier = "meta_chose.sql"
        type_requete = nom_fichier[0:nom_fichier.index('_')]
        self.assertEqual(type_requete,'meta')
        
    def testFuckingPath(self):
        nom_rel_rep_dest = 'requetes_sql_a_importer'
        chemin_repertoire = os.path.join(os.path.dirname(os.path.abspath(__file__)), nom_rel_rep_dest)
        self.assertEqual(os.path.normpath(chemin_repertoire), 'c:/')
        
        
    def testGlob(self):
        nom_rel_rep_dest = 'requetes_sql_a_importer'
        chemin_repertoire = os.path.join(os.path.dirname(os.path.abspath(__file__)), nom_rel_rep_dest)
        print(chemin_repertoire)
        self.assertEqual('plop.sql',glob.glob(os.path.normpath(chemin_repertoire) + '/' + '*.sql'))
        
    def testTypeFuckingGlob(self):
        nom_rel_rep_dest = 'requetes_sql_a_importer'
        chemin_repertoire = os.path.join(os.path.dirname(os.path.abspath(__file__)), nom_rel_rep_dest)
        globs = glob.glob(os.path.normpath(chemin_repertoire) + '/' + '*.sql')
        nom_fichier = os.path.basename(globs[0])
        type_requete = nom_fichier[0:nom_fichier.index('_')]
        self.assertEqual(type_requete, 'meta')
        
    def testLanceDepuisBonEndroit(self):
        self.assertEqual(getCheminFichierCourant(),os.path.abspath(__file__))
        
        
        
    def testPareilAvecPkgUtilReps(self):
        nom_rel_rep_dest = 'requetes_sql_a_importer'
        chemin_courant = getCheminFichierCourant()
        globs = getListeFichiersGlobsDansChemin(getAssemblageCheminFicheretSousRep(os.path.abspath(__file__), 
                                                                                          nom_rel_rep_dest), 
                                                '*.sql')
        nom_fichier = getNomFichierDepuisCheminComplet(globs[0])
        type_requete = nom_fichier[0:nom_fichier.index('_')]
        self.assertEqual(type_requete, 'meta')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()