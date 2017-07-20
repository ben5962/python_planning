'''
Created on 18 juil. 2017

@author: Utilisateur
'''

#import pkg_python_planning.db.bibliothecaire_dba
from pkg_python_planning.db import bibliothecaire_dba
import os.path


def parcourir_dico_contenant_dico(dico_contenant_dico, do_something_with_each_key_value_of_dico_contenu=None):
    for index_dico_contenant_dico, dico_contenu in dico_contenant_dico.items():
        for index_dico_contenu, valeur_dico_contenu in dico_contenu.items():
            do_something_with_each_key_value_of_dico_contenu(index_dico_contenant_dico,index_dico_contenu,valeur_dico_contenu)
                



def exporter_dico_dans_fichier_sql(entete_nom_fichier,partie_principale_nom_fichier, contenu_fichier):
        nom_fichier = ( 
            entete_nom_fichier 
            + "_" 
            + partie_principale_nom_fichier 
            +  ".sql" 
            )
        nom_rel_rep_dest = 'requetes_sql_extraites'
        chemin_repertoire = os.path.join(os.path.dirname(__file__), nom_rel_rep_dest)
        try: 
            chemin_fichier_complet = os.path.join(chemin_repertoire, nom_fichier)
            with open(chemin_fichier_complet, 'w') as f:
            #with p.open(nom_fichier, mode='w', encoding='utf8') as f:
                f.write(contenu_fichier)
        except TypeError:
            ch_err = "erreur de type: write attend ch pas tuple lors appel avec {}".format(nom_fichier)
            print(ch_err)
            
            
    
        


if __name__ == '__main__':
    
    bib = bibliothecaire_dba()
    parcourir_dico_contenant_dico(bib.dicorequetes, do_something_with_each_key_value_of_dico_contenu=exporter_dico_dans_fichier_sql)
    