import os
from pathlib import Path

def setRelativeToAbsoluteCurPath(chemin):
    chemin.cwd()

def getParentDir(chemin):
    to_resolve = chemin.joinpath('..')
    resolved = to_resolve.resolve()
    return resolved

def getResolvedRelativeDir(chemin,  relativedir):
    to_resolve = chemin.joinpath(relativedir)
    resolved = to_resolve.resolve()
    return resolved
    
    
def importer_dossier_dans_path(nom_dossier_a_ajouter_au_path,chemin_relatif_racine_projet,chemin_depart_hardcoded=False):
    # chaine x chaine - void
    #init : dossier = dossier courant de CE fichier
    if chemin_relatif_racine_projet:
        p = Path(r'C:\Users\Utilisateur\Documents\GitHub\import_de_cochon')
    else:
        p = Path('.')
    rep_courant = p.resolve()
    #rep_courant = p.cwd()
    print('importer_dossier_dans_path : init :  dossier : rep_courant vaut {}'.format(
        str(rep_courant)
        )
          )

    #init racine projet relativement a ce repertoire
    racine = Path('.').resolve()
    racine = getResolvedRelativeDir(racine,chemin_relatif_racine_projet)
        #racine = racine / elem

    print('importer_dossier_dans_path : init : racine vaut {}'.format(
        str(racine))
        )

    if not racine.is_dir():
        raise ValueError("racine doit etre un repertoire existant: {}".format(
            str(racine)
            )
                         )

    #lancement boucle principale    
    dossier = rep_courant
    while not dossier.joinpath(nom_dossier_a_ajouter_au_path).is_dir():
        print('importer_dossier_dans_path : pas trouve {} dans {}'.format(
            nom_dossier_a_ajouter_au_path,
            str(dossier.joinpath(nom_dossier_a_ajouter_au_path))
            )
              )
        #cas d arret 'remonte trop haut'
        if racine in [d for d in dossier.resolve().iterdir() if d.is_dir()]:
            raise ValueError('importer_dossier_dans_path : echec import {} : arrive au sommet du projet : {} sans trouver le dossier a importer'.format(
                nom_dossier_a_ajouter_au_path, str(racine)))
                  
            
        #transision a etape suivante: remonter d un repertoire
        dossier = getParentDir(dossier) 
        
        print('importer_dossier_dans_path : je remonte d un dossier : {}'.format(
            str(dossier)
            )
              )
        
        
    # sortie:  ok trouve
    # traitement de  ok trouve
    #avant traitement
    print('importer_dossier_dans_path : trouve repertoire {}: me trouve actuellement dans repertoire {}'.format(
        nom_dossier_a_ajouter_au_path,
        str(dossier)
        )
          )
    import sys
    print('longueur chemin python est de {} avant ajout du dossier {} et contenu :{}'.format(
        len(sys.path),
        nom_dossier_a_ajouter_au_path,
        str(sys.path)
        )
          )

    #traitement
    sys.path.append(str(getResolvedRelativeDir(dossier,nom_dossier_a_ajouter_au_path)))
    #verif effet traitement
    
    print('longueur chemin python est de {} apres ajout du dossier {} et contenu :{}'.format(
        len(sys.path),
        nom_dossier_a_ajouter_au_path,
        str(sys.path)
        )
          )



##
        #cas d arret: le dossier 
##        while not dossier.endswith(nom_dossier_a_ajouter_au_path):
##            dossier = os.path.dirname(dossier)
## 
##        dossier = os.path.dirname(dossier)
## 
##if dossier not in sys.path:
##    sys.path.append(dossier)
