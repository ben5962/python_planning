'''
Created on 22 juil. 2017

@author: Utilisateur
'''

import os.path
import glob 


def getCheminFichierCourant():
    return os.path.abspath(__file__)

def getAssemblageCheminFicheretSousRep(chemin, sousrep):
    return os.path.join(os.path.dirname(chemin), sousrep)
                 
def getListeFichiersGlobsDansChemin(chemin, starexp):
    return glob.glob(os.path.normpath(chemin) + '/' + starexp)

def getNomFichierDepuisCheminComplet(chemin):
    return os.path.basename(chemin)
    