'''
Created on 6 juil. 2017

@author: Utilisateur
'''

class CalculJourDimancheALundi(object):
    '''
    classdocs
    '''


    def __init__(self, a, m, j):
        '''
        Constructor
        
    
        '''
        self.a = a 
        self.m = m 
        self.j = j 
        
    def calcul(self):
        """Algorithme de Mike Keith wikipedia. 
        0 = dimanche
        1 = lundi.... 
        """
        d = PAS_CALCULE = 1000
        quotient_mois, __osef__ = divmod(((23  * self.m) / 9),1)  
        quotient_annee_bis1, __osef__ = divmod((self.a / 4),1)
        quotient_annee_bis2, __osef__ = divmod((self.a / 100 ),1)
        quotient_annee_bis3, __osef__ = divmod((self.a / 400),1)
         
        
        if self.m >= 3:
            z = self.a
            temp = quotient_mois + self.j + 4 + z + quotient_annee_bis1 - quotient_annee_bis2 + quotient_annee_bis3
            __osef__, d = divmod ((temp - 2 ), 7)

        else:
            z = self.a - 1
            temp = quotient_mois + self.j + 4 + z + quotient_annee_bis1 - quotient_annee_bis2 + quotient_annee_bis3
            __osef__, d = divmod(temp,7)
        
        return int(d)