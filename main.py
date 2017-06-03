#-*-coding:utf8;-*-
#qpy:3
#qpy:console

#import auditeur
#import boss
from db import realdb
import db
import une_passe


def run():
    ETAT = 'DEPART'
    ETATS_FIN = ['FIN']
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
            ETAT = 'SCHEMAS_EXISTE'
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
            ETAT = 'SCHEMAS_EXISTE'
            continue
        if ETAT == 'PRET_POUR_RAPPORT':
            print(ETAT)
    
            une_passe.prejudice()
            ETAT = 'FIN'
            continue
            
    
if __name__ == '__main__':
    run()
        
        
            

    
    def commentaire():
        boss = Boss()
        boss.setAnnees(2014,2015,2016)
        boss.doit()
    
# modif de val pour test autologin ssh key    
