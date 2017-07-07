import une_passe
import unittest

class TestUnePasse(unittest.TestCase):

    def testSubstLisk(self):
        """subtitution méthode acces aux heures trav
        par un entier pour les tests"""
        self.assertEqual(une_passe.getCumulHeuresTravailleesSemaine(
            a=2016,
            s=15,
            methode=42
            ),
                    42)

    def testHeuresTravSem(self):
        """verification du principe:
             les cumuls d heures trav
             fonctionnent elles tjs pour les
             """
        self.assertEqual(
            une_passe.getCumulHeuresTravailleesSemaine(2015,15),
            30)

    def testHeuresIllegales(self):
        """interdit au delà de 48"""
        self.assertEqual(une_passe.heures_illegales_effectuees(49),
                         1)

    def testHeuresSup50(self):
        """entre 43 et 48"""
        self.assertEqual(une_passe.heures_sup_50_effectuees(43),0)
        self.assertEqual(une_passe.heures_sup_50_effectuees(44),1)
        self.assertEqual(une_passe.heures_sup_50_effectuees(48),5)
        self.assertEqual(une_passe.heures_sup_50_effectuees(49),5)

    def testHeuresSup25(self):
        """entre 39 et 43"""
        self.assertEqual(une_passe.heures_sup_25_effectuees(35),0)
        self.assertEqual(une_passe.heures_sup_25_effectuees(36),1)
        self.assertEqual(une_passe.heures_sup_25_effectuees(43),8)
        self.assertEqual(une_passe.heures_sup_25_effectuees(44),8)

    def test_DB_realdb_test_si_semaine_repos_sautée(self):
        # doit produire 0 heures sup payées si semaine de type repos
        #
        import une_passe
        self.assertEqual(une_passe.sup25_deja_paye(0),4)
        self.assertEqual(une_passe.sup25_deja_paye(39),0)
        self.assertEqual(une_passe.sup25_deja_paye(150),0)
        
        

    



