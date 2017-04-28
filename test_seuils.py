# -*- coding: utf-8 -*-
import unittest
import seuils
from seuils import Seuil
import types
import devpy.develop as log

class TestSeuils(unittest.TestCase):
    from seuils import Seuil



    def planter_si_liste_vide(self,liste,nomliste):
        log.info("lancement de planter si liste vide avec {} et {}".format(liste, nomliste))
        if liste is None:
            log.critical(nomliste + " is  None. should be non empty list")
            raise TypeError
            
    def listes_meme_longueur(self,liste1=None,liste2=None):
        """teste si deux listes ont la mm longueur"""
        log.info("lancement de liste_meme_longueur avec {} et {}. teste si les deux param st des listes et ont la mm lg".format(liste1, liste2))
        self.planter_si_liste_vide(liste1,"liste1")
        self.planter_si_liste_vide(liste2,"liste2")

        
        verite = False
        if type(liste1) == type([]):
            if type(liste2) == type([]):
                verite = (len(liste1) == len(liste2))
                return verite
            else:
                print("type( ", str(liste1), "):", type(liste1))
                print("type([]): ", type([]))
                raise TypeError
        else:
            print("type( ", str(liste2), "):", type(liste2))
            print("type([]): ", type([]))
            raise TypeError

    def listes_meme_contenus(self,liste1,liste2):
        """si les deux elements sont des listes de mm lg, cherche si elles ont
        le meme contenu"""
        
        log.info("lancement de listes_meme_contenus. si les deux elements sont des listes de mm lg, cherche si elles ontle meme contenu")
        verite = True
        """ parametre: deux listes non vides"""
        """non vides"""
        if liste1 is None:
            log.critical("liste1 is none! should be list")
            raise TypeError
        if liste2 is None:
            log.critical("liste2 is none! should be list")
            raise TypeError
        
        for pos, elem in enumerate(liste1):
            if liste1[pos] != liste2[pos]:
                verite = False
                break
        return verite
            
            
            
    def meme_liste(self,liste1,liste2):
        """teste si deux listes sont identiques"""
        log.info("lancement de meme liste.teste si deux listes sont identiques")
        verite = False
        if self.listes_meme_longueur(liste1,liste2):
            return self.listes_meme_contenus(liste1,liste2)
            
        else:
            return verite

 


    def t_seuils(self,liste1,liste2):
        log.info("lancement de t_seuils avec: {} {}".format(liste1,liste2))
        self.assertEqual(True, self.meme_liste(liste1,liste2), '{} differe de {}'.format(liste1, liste2))

    
    def test_production_intervalles_multiples_2(self):
        log.info("lancement de test_production_intervalles_multiples_2")
        self.t_seuils([15,3],Seuil(15,18).getIntervalles())

    
    def test_production_intervalles_multiples_3(self):
        log.info("lancement de test_production_intervalles_multiples_3")
        self.t_seuils([15,3,1],Seuil(15,18,19).getIntervalles())

    
    def test_cas_heures_inf_au_premier_seuil_seuil_unique(self):
        log.info("lancement de test_cas_heures_inf_au_premier_seuil_seuil_unique")
        self.t_seuils([15,0],Seuil(18).decouper(15))

    
    def test_cas_heures_sup_au_premier_seuil_seuil_unique(self):
        log.info("lancement de test_cas_heures_sup_au_premier_seuil_seuil_unique")
        self.t_seuils([15,3],Seuil(15).decouper(18))

        
    
    def test_cas_heures_inf_au_deuxieme_seuil(self):
        self.t_seuils([15,3,0],Seuil(15,18).decouper(18))
        # enfin réglé: pb de décalage de return : indenté par rapport à
        # boucle for provoquait sortie du for lors premiere boucle.
        # résolu en le mettant au meme niveau que le for.

    def test_plantage_listes_memes_lg_si_param1_liste_vide(self):
        log.info("lancement de test_plantage_listes_memes_lg_si_param1_liste_vide")
        self.assertRaises(TypeError,self.listes_meme_longueur,None,[1])
                      
        
if __name__ == '__main__':
    unittest.main()
