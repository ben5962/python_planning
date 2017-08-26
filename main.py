#-*-coding:utf8;-*-
#qpy:3
#qpy:console

#import auditeur
#import boss
from db import realdb
from db import bdd
from secretaire import Secretaire
import db
import une_passe


def run():
    ETAT = 'DEPART'
    ETATS_FIN = ['FIN', 'FIN_ERREUR_DONNEES_MAL_PRODUITES_EXISTENT_PAS','FIN_ERREUR_SCHEMAS_MAL_PRODUIT']
    while ETAT not in ETATS_FIN:
        if ETAT == 'DEPART':
            print(ETAT)
            r = realdb()
            r.setFichierDb('planning.db')
            if r.TestFichierDbExiste():
                ETAT = 'DB_EXISTE'
                
            else:
                ETAT = 'DB_EXISTE_PAS'
            continue
        if ETAT == 'DB_EXISTE_PAS':
            print(ETAT)
            r.createDbFile()
            ETAT = 'DB_EXISTE'
            continue
        if ETAT == 'DB_EXISTE':
            print(ETAT)
            r.setBibliothecaireDba()
            if r.TestSchemasDbExiste():
                ETAT = 'SCHEMAS_EXISTE'
            else:
                ETAT = 'SCHEMAS_EXISTE_PAS'
            continue
        if ETAT == 'SCHEMAS_EXISTE_PAS':
            print(ETAT)
            r.setSchemaDb()
            if r.TestSchemasDbExiste():
                ETAT = 'SCHEMAS_EXISTE'
            else:
                ETAT = 'FIN_ERREUR_SCHEMAS_MAL_PRODUIT'
            continue
        if ETAT == 'SCHEMAS_EXISTE':
            print(ETAT)
            if r.TestDonneesDbExistent():
                ETAT = 'DONNEES_EXISTENT'
            else:
                ETAT = 'DONNEES_EXISTENT_PAS'
            continue
        if ETAT == 'DONNEES_EXISTENT':
            print(ETAT)
            
            ETAT = 'PRET_POUR_RAPPORT'
            continue
        if ETAT == 'DONNEES_EXISTENT_PAS':
            print(ETAT)
            r.setContentDb()
            if r.TestDonneesDbExistent():
                ETAT = 'DONNEES_EXISTENT'
            else:
                ETAT = 'FIN_ERREUR_DONNEES_MAL_PRODUITES_EXISTENT_PAS'
            continue
            continue
        if ETAT == 'PRET_POUR_RAPPORT':
            print(ETAT)
            SOUS_ETAT = 'DEBUT'
            SOUS_ETATS_FIN = ['FIN','FIN_SOUS_ETAT_ERREUR_ECHEC_PRODUC_DONNEES_EXCEL_EXPERT']
            b = bdd(realdb=r)
            s = Secretaire(bdd=b)
            while SOUS_ETAT not in SOUS_ETATS_FIN:
                print(SOUS_ETAT)
                if SOUS_ETAT == 'DEBUT':
                    if b.TestRapportJeuDonneesExpertComptableExistent():
                        SOUS_ETAT = 'DONNEES_EXCEL_EXPERT_EXISTENT'
                    else:
                        SOUS_ETAT = 'DONNEES_EXCEL_EXPERT_EXISTENT_PAS'
                continue
                if SOUS_ETAT == 'DONNEES_EXCEL_EXPERT_EXISTENT_PAS':
                    s.CreerExcelDonneesExpert()
                    if b.TestRapportJeuDonneesExpertComptableExistent():
                        SOUS_ETAT = 'DONNEES_EXCEL_EXPERT_EXISTENT'
                    else:
                        SOUS_ETAT = 'FIN_SOUS_ETAT_ERREUR_ECHEC_PRODUC_DONNEES_EXCEL_EXPERT'
                continue
                    
                   
            #une_passe.prejudice()
            ETAT = 'FIN'
            continue
    
    print(ETAT)
            
    
if __name__ == '__main__':
    run()
        
        
            

    
    def commentaire():
        boss = Boss()
        boss.setAnnees(2014,2015,2016)
        boss.doit()
    
# modif de val pour test autologin ssh key fonctionne
# modif de val pour test envoi tache plannifiee 5 min  plop
# plop plop plop ca doit se lancer
