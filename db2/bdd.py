#-*-coding:utf8;-*-
#qpy:2
#qpy:consol
from metier import Entree
from metier import timedelta_to_hour
from metier import diff_entre_deux_datestimes


from dateutil.parser import parse
import devpy.develop as log

class bdd (object):
    """
    les données, indépendemment de leur mode d obtention
    (db, fichier, osef.... typiquement la tete de ligne du modele)
    """
    """
    bdd est un proxy vers realdb et 
    1) connaissance des données db:
       tâche par tâche:
       A)tâche vérification des heures supplémentaires, 39 heures :
       les heures supplémentaires se calculent à la semaine et sont cumulées au mois
       if faut donc
       - pouvoir itérer sur les mois par numéro
       A.1 -> déporté dans métier AnneeCalendaire:
            fournit un objet itermois
            mode emploi:
            a = Annee(2016)                 -- TODO metier.A.1
            for m in a.iterMois():          -- TODO metier.A.2
                print(m)
            > 1
            > 2
            > ...
            > 12
            => il faut aussi un accesseur getAnnee() à Annee pour A.3 TODO metier.A.3
            mode emploi: a = annee(2016)
                        a.getAnnee()
                        >> 2016 
       pour chaque mois 
       - connaitre par leur numéro la liste des semaines à rattacher à un mois
       A.2 donne les numéros de semaines .
          -> déporté dans métier: objet MoisComptableCalendaire fournit iter sur liste
             des numéros de semaine Terminées dans le mois saisi.
             mode emploi :  m = MoisComptableCalendaire(2015, 1)      -- METIER.B.1 TODO
             for num_sem in m.iterNumerosSemainesTermineesAuCoursDuMois() -- METIER.B.2 TODO
                 print(num_sem)
            >> (2015,53)
            >> (2016,1)
            >>  (2016,2)
            >>  (2016,3)
             DONE
             bdd() possède un accès à mois maybe? 
       - connaitre les bornes en horodatage des semaines afin de pouvoir interroger
       la db sur la somme des heures faites sur la semaine situee entre date début
       et date fin.
       A.3 donne les bornes en horodatage d une semaine, annee saisie
            -> déporté dans métier : objet SemaineCalendaire fournit methode
            getHoroDebutEtHoroDebutSplus1BornantSemaine() mode emploi:
            s = SemaineCalendaire(a=2016,num_sem=43)
            s.getHoroDebutEtHoroDebutSplus1BornantSemaine()
            > (datetime;datetime('2017-11-05 00:00:00'),datetime.datetime('2017-11-12 00:00:00'))
            TODO 
       pour cela il faut interroger la base qui doit avoir acces, non pas aux saisies
       plannings mais aux saisies sous formes de jours travaillés (de 0 à 24h)
       -- la creation des jours travailles est l objet de:
       --  la creation de trigger dans la base dans les requetes de creation
       --    c'est la tâche C.1 "creation d un trigger de crea des periodes_trav"
       --    dans bibliothécaire FAIT
       --    et de B.2 "lancement des trigger de bibliothécaire  C.1" FAIT
       --    avec le "lancement de la créat de structure de la db de plannings"
       --    B.1 FAIT
       pour faire le cumul des heures  faites dans une semaine calendaire
       A.4 donne le nombre d heures travailles sur une semaine annee
       donnee sur la base des chiffres trouvés par requete dans la db
           -> bdd() fournit méthode getCumulHeuresTravailleesSemaine(num_sem,aaaa)
           mode emploi:
           a = annee(2016)
               for mois in a.iterMois():
                   m = MoisComptableCalendaire()
                   for num_sem in m.iterNumerosSemainesTermineesAuCoursDuMois()
                      presentation.tranche(
                      ''.join("W", num_sem[1]),
                      bdd().getCumulHeuresTravailleesSemaine(52,2016),
                      HeuresDansLesSeuils(
                          bdd().getCumulHeuresTravailleesSemaine(52,2016),
                          39,
                          43),
                      HeuresDansLesSeuils(
                          bdd().getCumulHeuresTravailleesSemaine(52,2016),
                          43,
                          48),
                       HeuresDansLesSeuils(
                          bdd().getCumulHeuresTravailleesSemaine(52,2016),
                          48,
                          2000).to_list()
                      )
           >>["W52", "48","4","5"]  --presentation.tranche sera en fait:
               secretaire.ajouter_au_rapport( comptable (ou larbin.getLigneTableau3
       - connaitre le seuil pour les 39 heures et savoir qu il s agit d un seuil
       hebdo A.5
       - savoir ce que l on fait en cas de dépassement de ce seuil.
       (décompte heures sup) A.6
       - stocker toutes ces informations qq part pour pas les produire 20 fois:
         il me faut une table contenant l asso entre l annee la semaine et les heures faites
         MAUVAISE IDEE LES CALCULS SERONT FAITS A CHAQUE FOIS:
         EN CAS DE MODIF DES DONNEES IL FAUDRAIT REPERCUTER CELA SUR LES
         INFORS STOCKEES. COMPLIQUE PAS ENVIE DE SE FAIRE CH...
       
       - aller checher ces informations et les mettre en forme.
       je choisis de ne pas séparer le calcul de ces infos et leur mise en forme.
       LES DEUX SE FONT DANS LA MEME ETAPE
       afin de fournir la liste des semaines calendaires devant être rattachées
       à un mois calendaire, fournit des utilitaires de calendrier:
       
       - donne les bornes en horodatage de l instant de début d une semaine et
         de l instant de fin de la semaine suivante.
          
       -  planning : connait et peut fournir la liste des entrees dans le plng
          ainsi que leur nombre
          but: décompte des postes pour les  vérifs de primes de panier
       -  journées travaillées: connait et peut fournir la liste des tranca
       -  pour le boss : fournit la liste des années dans lesquelles il y a au
          moins une entrée. 
    2) connait tous les noms de classes de taches de verif
     3) 
     4) connait tous les fichiers de postes manuels disponibles
     5) connait tous les fichiers de fiches de paye manuels disponibles
     
   
     """
    import calendar
    import calendrierComptable
    

    def __init__(self):
        #self.setListeNomsEtapesVerificationMensuelle()
        self.setRealDb()

    def setRealDb(self):
        self.realdb = realdb()

    def getRealDb(self):
        #une  UNIQUE instance de RealDb()! 
        if hasattr(self,'realdb'):
            return self.realdb
        else:
            self.setRealDb()
            return self.realdb

    def valider(self):
        self.getRealDb().valider()


    def getCumulHeuresTravailleesSemaine(self,annee,num_semaine):
        """ doit renvoyer un nombre:
            -> le nombre d heures effectuees dans un intervalle de dates
            peut renvoyer plusieurs valeurs:
            0 si la semaine n'est ni travaillée ni une semaine d absence
             (hautement improbable)
            un_nombre sinon.
            nb: il faut traiter le cas des cp:
            un cp entraine 0 heures à décompter dans le cadre des heures sup
            et 0 h à payer. il faudra la sortir du lot lors du cumul
            il faudra penser aussi aux semaines avec 1 jour de congés....
            je propose :
            - de mettre la somme à zéro
            - de renvoyer la somme des heures travaillées
            - de traiter séparément la cause du zéro s'il y a lieu
            """
        nb_heures = 0
        ajout = self.getRealDb().getCumulHeuresTravailleesSemaine(annee,num_semaine)
        nb_heures = nb_heures + ajout
        return nb_heures
        

        
    def verifier_travail_saisie_planning(self):
        """verifie que le nombre de saisies dans la base n est pas nul"""
        nombre_postes_saisis = self.getRealDb().getNombrePostesSaisis()
        print("le nombre d elements de planning saisis est de : {}"
              .format(nombre_postes_saisis)
              )
        if nombre_postes_saisis:  #vrai si non nul
            return True
        else:
            return False

    def verifier_travail_saisie_periodes_travaillees(self):
        """verifie que le nombre de saisies dans la base n est pas nul"""
        nombre_postes_saisis = self.getRealDb().getNombrePeriodesTravailleesSaisies()
        print("le nombre d elements de périodes travaillées saisies est de : {}"
              .format(nombre_postes_saisis)
              )
        if nombre_postes_saisis:  #vrai si non nul
            return True
        else:
            return False

    

        

    def iterMonthNumber(self):
        return range(1,13)

    def iterFichiersPostes(self):
        import re
        import os
        genfichiers = (f for f in os.listdir('.') if re.match(r'postes[0-9]{4}\.txt', f) )
        return genfichiers

    def iterLignesFichiersPostes(self):
        for f in self.iterFichiersPostes():
            with open(f, 'r') as fichierCourant:
                for ligne in fichierCourant:
                    yield ligne


    def saisirToutesEntrees(self, iterateurEntrees):
        self.getRealDb().saisirToutesEntrees(iterateurEntrees)

    def saisir_entree(self, tuple_entree):
        self.getRealDb().saisir_entree(tuple_entree)
        
        
                



        

    def getSemainesJoursTravaillesFromMonthYear(self, month, year):
        """ pour les 39 heures permet de récupérer
- une liste de semaines
 -  une semaine étant une liste de 7 dates commencant un lundi"""
        ToutesLesSemainesCommenceesOuTermineesDansLeMois  = self.cal.monthdatescalendar(year, month)
        LesSemainesAgarderDansLeMois = methodeTronquage(ToutesLesSemainesCommenceesOuTermineesDansLeMois)
        calendar.weekday(2016, 1, 31)


    def getJoursTravaillesFromYear(self,month,year):
        """ pour l annu renvoie la liste de postes travailles
pour les sommer ensuite


"""
    pass

    def getEtapesVerificationMensuelle(self):
        """renvoie les etapes de la vérif"""
        return EtapeVerificationHeureSupplementaireMensuelle.__subclasses__()
        

        

    def setListeNomsEtapesVerificationMensuelle(self):
        """remplit la liste des noms de taches de verif dispo
chaque verif listee ici doit etre implémentee ou claquer une
Exception("not implemented")
"""
        
            #http://stackoverflow.com/questions/3451779/how-to-dynamically-create-an-instance-of-a-class-in-python
        import tachesVerif
        self.listeNomsEtapesVerificationMensuelle =  tachesVerif.getNomTaches()
        
    def getListeNomsEtapesVerificationMensuelle(self):
        """ doit renvoyer les noms d etapes.  sert en interne a instancier
les classes par nom"""
        return self.listeNomsEtapesVerificationMensuelle



    def setListeEtapesVerificationMensuelle(self):
        """ doit construire les instances d etapes de  verif
et les mettre dans une liste
chaque verif listee ici doit etre implémentee ou claquer une
Exception("not implemented") """

        #http://stackoverflow.com/questions/3451779/how-to-dynamically-create-an-instance-of-a-class-in-python
##        module = "db"
##        for nom_etape in nomEtapesVerificationMensuelle:
##            self.getListeEtapesVerificationMensuelle().append(
##                self.construireEtapeVerificationMensuelleFromNomEtape(module,nom_etape)
##                )

    def getListeEtapesVerificationMensuelle(self):
        """ doit renvoyer les etapes instanciees avec des valeurs par defaut"""
        return self.listeEtapesVerificationMensuelle

    
        

        
    def getPostes (self,name):
        
        if name == "all":
            return self.getRealDb().getAllPostes()

    def iterAllPostes(self):
        return self.getRealDb().iterAllPostes()

    def iterAnneesDispo(self):
        """realisation de 3)
doit renvoyer les annees uniques disponibles dans la base
préconditions:
- besoin d'une connexion à la base ou déléguer à bdd donc récupérer un trigger
de requete à la db donc le récup d'un tuple donc le transfo en champ"""
        return self.getRealDb().iterAnneesDispo()

    def remplirBase(self):
        """hmmm tentative de remplissage de db.
            appels infinis?"""
        self.getRealDb().setContentDb()
            
      


class ErrAnnu(object):
    """doit signifier les erreurs dans le decompte de l annualisation.
pour l instant je pars d une annualisation de janvier à janvier
l annualisation compare les fiches de paye réelles aux fiche de paye theorique.
les fiches de paye reelles n ont aucune heure sup sauf la derniere qui cumule
les heures sup de l annee par rapport au seuil legal de 17
https://www.juristique.org/social/duree-du-travail"""
    import datetime
    def __init__(self,annee=2016, debut={'heure':0, 'minute': 0, 'jour':1, 'mois':1, 'annee':0}, duree={'heure':0, 'minute': 0, 'jour':0, 'mois':0, 'annee':1}):
        self.annee = annee
        self.datedebut = datetime.datetime(self.annee,
                                         delta_debut.mois,
                                         delta_debut.jour,
                                         deltat_debut.heure,
                                         delta_debut.minute)
        self.datefin = self.datedebut
        + datetime.timedelta(years=duree.annee)
        
    def getDateDebut(self):
        return self.datedebut

    def getDateFin(self):
        return self.datefin

    def getAnnee(self):
        return self.annee
