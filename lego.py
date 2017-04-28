import xpld
import constantes
""" je veux une fonction pour mon larbin
- ouvrant un fichier texte,
- explosant chaque ligne,
- transformant chaque ligne explosee en un poste via:
   * la creation d un horodatage de début
      i. par la combinaison d une date et d une heure:
         - la date etant annee mois et jour de début de poste
         - le début de poste dépendant du type de poste:
             * le type de poste est lu dans le fichier texte à destination du larbin
             * la correspondance entre type de poste et heure de début
                se fait à partir de la lecture de constantes.py
    * la creation d un horodatage de fin
      i . par l ajout à l horodatage de début de poste d une duree
        - la duree dépend du type de poste:
          * le type de poste est lu dans le fichier texte à destination du larbin
          * la correspondance entre type de poste et duree se lit dans constantes.py
    * la creation d un type d entree dans le planning lu dans constantes.py
    * la création d une categorie d entree lu dans constantes.py: travail ou absence"""
      

        

with open("2014.txt") as f:
  for ligne in f:
    for ligne_poste in xpld.xpld().xplode_ite(ligne):
            print(ligne_poste)
##			datetime_debutposte = datetime.datetime.combine(
##				datetime.date(ligne_poste['year'], ligne_poste['month'], ligne_poste['day']),
##				datetime.time(ligne_poste)
##			
