'''
Created on 6 juil. 2017

@author: Utilisateur
'''
class CalculJourLundiADimanche(object):
    def __init__(self, a, m, j):
        '''
        Constructor
        
    
        '''
        self.a = a 
        self.m = m 
        self.j = j 
        
    def calcul(self):
        """Algorithme de Mike Keith wikipedia. 
        https://fr.wikibooks.org/wiki/Curiosit%C3%A9s_math%C3%A9matiques/Trouver_le_jour_de_la_semaine_avec_une_date_donn%C3%A9e
        0 = dimanche
        1 = lundi.... 
        modifié pour produire:
        0: lundi
        ..
        6 : dimanche
        d = (d + modificateur) modulo 7
        modificateur = -1       """
        modificateur = -1
        
        d = PAS_CALCULE = 1000
        def quotient_mois(m):
            qm, __osef__ = divmod(((23  * m) / 9),1)
            return qm
        def test_annee_bissextile_div_par_4(z):
            qa, __osef__ = divmod((z / 4),1)
            return qa
        def test_annee_bissextile_div_par_100(z):
            quotient_annee_bis2, __osef__ = divmod((z / 100 ),1)
            return quotient_annee_bis2
        def test_annee_bissextile_div_par_400(z):
            quotient_annee_bis3, __osef__ = divmod((z / 400),1)
            return quotient_annee_bis3
        
        def calc_intermediaire(mois, jour, annee, z):
            return ( 
                    quotient_mois(self.m)
                     + self.j 
                     + 4 
                     + self.a 
                     + test_annee_bissextile_div_par_4(z)
                    -  test_annee_bissextile_div_par_100(z)
                    +  test_annee_bissextile_div_par_400(z)
                    )
         
        
        if self.m >= 3:
            z = self.a
            temp = calc_intermediaire(self.m, self.j,self.a, z)
            __osef__, d = divmod ((temp - 2 + modificateur), 7)

        else:
            z = self.a - 1
            # meme temp.
            temp = calc_intermediaire(self.m, self.j, self.a, z)
            __osef__, d = divmod(temp + modificateur,7)
        
        return int(d)