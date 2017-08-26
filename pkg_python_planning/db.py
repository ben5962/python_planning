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
    

    def __init__(self,realdb=None):
        #self.setListeNomsEtapesVerificationMensuelle()
        self.setRealDb(realdb)

    def setRealDb(self, realdb=None):
        import db
        if realdb is None:
            self.realdb = db.realdb()
        else:
            self.realdb = realdb

    def getRealDb(self):
        #une  UNIQUE instance de RealDb()! 
        if hasattr(self,'realdb'):
            return self.realdb
        else:
            self.setRealDb()
            return self.realdb

    def valider(self):
        self.getRealDb().valider()

    def getCumulHeuresCpSemaine(self,annee,num_semaine):
        return self.getRealDb().getCumulHeuresCpSemaine(annee,num_semaine)



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
        log.debug("")
        log.debug("le nombre d elements de planning saisis est de : {}"
              .format(nombre_postes_saisis)
              )
        if nombre_postes_saisis:  #vrai si non nul
            return True
        else:
            return False

    def verifier_travail_saisie_periodes_travaillees(self):
        """verifie que le nombre de saisies dans la base n est pas nul"""
        nombre_postes_saisis = self.getRealDb().getNombrePeriodesTravailleesSaisies()
        log.debug("le nombre d elements de périodes travaillées saisies est de : {}"
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
    
    def __init__(self,annee=2016, debut={'heure':0, 'minute': 0, 'jour':1, 'mois':1, 'annee':0}, duree={'heure':0, 'minute': 0, 'jour':0, 'mois':0, 'annee':1}):
        self.annee = annee
        import datetime
        self.datedebut = datetime.datetime(self.annee,
                                         delta_debut.mois,
                                         delta_debut.jour,
                                         delta_debut.heure,
                                         delta_debut.minute)
        self.datefin = self.datedebut
        + datetime.timedelta(years=duree.annee)
        
    def getDateDebut(self):
        return self.datedebut

    def getDateFin(self):
        return self.datefin

    def getAnnee(self):
        return self.annee
        
        


class realdb (object):
    """fait toutes les requetes
    vers la db que ce soit
    - la crea de la strucure de la table
    - dispo pour son remplissage
    - dispo pour les req en lecture si présence de champs"""
    def __init__(self, fichdb='planning.db'):
        """ besoins: nomfichdb"""
        self.setBibliothecaireDba()
        self.setFichierDb (fichdb)
        # apres cette etape le fichier existe forcement
        # la db a le bon schemas
        # structure
        #self.cnx = "" # initialise par setCnx
        #self.setCnx()
        

    def setContentDb(self):
        """remplit la base via larbin si pas remplie"""
        if not self.__nb_lignes_db(): # faux <=> renvoie 0
            log.debug("remplissons la base: elle ne contient aucune entrée actuellement")
            import db
            b = db.bdd(realdb = self)
            import larbin
            l = larbin.larbin(bdd = b)
            l.saisir()
            
            
        else:
            log.debug("base déjà remplie, rien à faire")
            log.debug("ont déjà été saisis {} postes et {} périodes travaillées".format(self.getNombrePostesSaisis(),
                                                                                    self.getNombrePeriodesTravailleesSaisies()
                                                                                    )
                  )

    def __nb_lignes_db(self):
        return self.getNombrePostesSaisis()

    def iterSemainesMoinsDe35Heures(self,borne_etudiee):
        """trouver les semaines de l annees où
            j ai travaille mois de <borne_etudiee> heures.
            utilisation : r = realdb()
            r.iterSemainesMoinsDe35heures(39) pour
            compter le nombre de semaines qui comporteront
            des heures négatives - 39 heures payées moins de 39 faites -
            certaines semaines comprennent des congés payés.
            il faut combler les trous des semaines en trop
            après cela il faudra borner cela à l'années:
            à la fin d une année on arrête de compter"""
        listeSemainesMoinsDe35Heures = []
        from db import bdd
        import utilitaireDates
        for annee in self.iterAnneesDispo():
            for mois in bdd().iterMonthNumber():
                for semaine in utilitaireDates.iterSemaine(annee,mois):
                    duree = self.getCumulHeuresTravailleesSemaine(annee,semaine) + self.getEqvCongesSemaine(annee,semaine)
                    """à cette fin, il faut remplir une table des repos sur le meme modele que horaires trav """

                    if duree < borne_etudiee:
                        le_tuple = (annee, semaine, duree, 39 - duree)
                        print(le_tuple)
                        listeSemainesMoinsDe35Heures.append(le_tuple)
        return listeSemainesMoinsDe35Heures
                    
            
    def getCumulHeuresCpSemaine(self,annee=None,num_semaine=None, scal=None):
        """ doit fournir le nombre d heures travaillees sur une semaine"""
        from metier import semaineCalendaire
        """éléments potentiellement foireux:
            - la différence entre deux dates en sqlite
            - l'agrégat de la différence entre deux dates en sqlite
            je préfère
            1) récupérer dans une liste tous les couples
            (période_travaillée.debut_période, période_travaillée.fin_période)
            FAIRE LA SOMME, SUR CHAQUE tuple de la liste de résultats de :
            2) créer un objet horodatage PYTHON pour chaque chaine horodatage de ce couple
            3) faire la différence fin_période - début_période (qui donne un timedelta en heures)
            4) convertir ce timedelta en entier (ne pas faire la somme sur des timedeltas,
            ca convertirait automatiquement en jours etc... je veux des heures

            """
        #1) récupérer la liste de tous les couples ....
        if annee is not None and num_semaine is not None:
            s = semaineCalendaire(annee,num_semaine)
        else:
            if  scal is not None:
                s = scal
            else:
                raise("erreur sur paramètres")
        tuple_premier_et_dernier_jour_semaine = s.getPremierEtDernierJourSemaine()
        premier_jour = tuple_premier_et_dernier_jour_semaine[0]
        dernier_jour = tuple_premier_et_dernier_jour_semaine[1]
        """ il faut transformer getBornes pour que la requete sql soit acceptée par sqlite
            comme requête entre deux bornes:
            - de (datetime.datetime(...), datetime.datetime(...))
                à ... no se"""
        liste_resultats = self.getListePeriodesCpEntreDeuxDates(
            premier_jour,
            dernier_jour
            )
        # la somme des elements d une liste vide est une liste vide
        # donc osef si getListePeriodesTravaileesEntreDeuxDates renvoie rien
        result = sum(
            [ timedelta_to_hour(
                diff_entre_deux_datestimes(
                    parse(t[0]),
                    parse(t[1])
                    )
                )
            for t in liste_resultats
              ]
            )
        return result            


    def getCumulHeuresTravailleesSemaine(self,annee=None,num_semaine=None, scal=None):
        """ doit fournir le nombre d heures travaillees sur une semaine"""
        from metier import semaineCalendaire
        """éléments potentiellement foireux:
            - la différence entre deux dates en sqlite
            - l'agrégat de la différence entre deux dates en sqlite
            je préfère
            1) récupérer dans une liste tous les couples
            (période_travaillée.debut_période, période_travaillée.fin_période)
            FAIRE LA SOMME, SUR CHAQUE tuple de la liste de résultats de :
            2) créer un objet horodatage PYTHON pour chaque chaine horodatage de ce couple
            3) faire la différence fin_période - début_période (qui donne un timedelta en heures)
            4) convertir ce timedelta en entier (ne pas faire la somme sur des timedeltas,
            ca convertirait automatiquement en jours etc... je veux des heures

            """
        #1) récupérer la liste de tous les couples ....
        if annee is not None and num_semaine is not None:
            s = semaineCalendaire(annee,num_semaine)
        else:
            if  scal is not None:
                s = scal
            else:
                raise("erreur sur paramètres")
        tuple_premier_et_dernier_jour_semaine = s.getPremierEtDernierJourSemaine()
        premier_jour = tuple_premier_et_dernier_jour_semaine[0]
        dernier_jour = tuple_premier_et_dernier_jour_semaine[1]
        """ il faut transformer getBornes pour que la requete sql soit acceptée par sqlite
            comme requête entre deux bornes:
            - de (datetime.datetime(...), datetime.datetime(...))
                à ... no se"""
        tuple_resultat = self.getListePeriodesTravailleesEntreDeuxDates(
            premier_jour,dernier_jour)
        # la somme des elements d une liste vide est une liste vide
        # donc osef si getListePeriodesTravaileesEntreDeuxDates renvoie rien
        result = sum(
            [ timedelta_to_hour(
                diff_entre_deux_datestimes(
                    parse(t[0]),
                    parse(t[1])
                    )
                )
            for t in self.getListePeriodesTravailleesEntreDeuxDates(
                premier_jour,
                dernier_jour
                )
              ] if self.getListePeriodesTravailleesEntreDeuxDates(premier_jour,dernier_jour) else [0]  #pour les autres langages
            )
        return result


    def getListePeriodesTravailleesEntreDeuxDates(self,d1,d2):
        """ datetime.date x datetime.date -> [(dtime_deb, dtime_fin),..(,)]"""
        return self.getCnx().execute(self.getBibliothecaireDba()
                                               .getRequeteLectureByName('periodes_travaillees_entre_deux_dates'),
                                               (d1, d2)
                                     ).fetchall()

    def getListePeriodesCpEntreDeuxDates(self, d1,d2):
        """ datetime.date x datetime.date -> [(dtime_deb, dtime_fin),..(,)]"""
        return self.getCnx().execute(self.getBibliothecaireDba()
                                     .getRequeteLectureByName('periodes_cp_entre_deux_dates'),
                                     (d1, d2)
                                     ).fetchall()
        
    
        
    

    def getNombrePostesSaisis(self):
        tuple_resultat = self.getCnx().execute(self.getBibliothecaireDba()
                                    .getRequeteMetaByName('nombre_postes_saisis')
                                    ).fetchone()
        
        nb = tuple_resultat[0] #le nombre doit etre extrait du tuple
        return nb

    def getNombrePeriodesTravailleesSaisies(self):
        tuple_resultat = self.getCnx().execute(self.getBibliothecaireDba()
                                    .getRequeteMetaByName('nombre_periodes_travaillees_saisies')
                                    ).fetchone()
        
        nb = tuple_resultat[0] #le nombre doit etre extrait du tuple
        return nb

    

    


    def saisirToutesEntrees(self, iterateurEntrees):
        """saisit toutes les entrees dans la base"""
        texterequete = self.getBibliothecaireDba().getRequeteEcritureByName('saisir_entree')
        for entree in iterateurEntrees:
            log.debug("ecriture de {}".format(str(entree))),
            self.getCnx().execute(texterequete, entree)
        self.getCnx().commit()

    def saisir_entree(self, tuple_entree):
        """ saisit 1 entree dans la base """
        texterequete = self.getBibliothecaireDba().getRequeteEcritureByName('saisir_entree')
        log.debug("ecriture de {}".format(str(tuple_entree))),
        self.getCnx().execute(texterequete, tuple_entree)

    def valider(self):
        self.getCnx().commit()
        

    def setBibliothecaireDba(self):
        """initialise un bibliothecaire. le lie a l objet realdb"""
        self.bibliothecaire_dba = bibliothecaire_dba()

    def getBibliothecaireDba(self):
        """si pas de bibli, le cree. sinon utilise l existant"""
        if self.bibliothecaire_dba is None:
            self.setBibliothecaireDba()
        return self.bibliothecaire_dba

    
            	
    import sqlite3
    def getFichierDb (self):
        return self.fichierdb


        
    
    def setFichierDb(self,filename):
        """ doit affecter la valeur filename a self.fichierdb
et s assurer que le fichier existe qu il est une base sqlite3
et que la base a le bon schemas"""
        self.fichierdb = filename
        
        def crea_fich_si_necessaire():
            db = self.getFichierDb()
            if not self.TestFichierDbExiste():
                """le fichier est cree en cnnct a fichier
        q existe pas et fermant cnx"""
                log.debug(self.getFichierDb() + "existe pas . le cree.""")
                self.createDbFile()
        crea_fich_si_necessaire()
        def commentaire3():
            log.debug("teste si le schemas existe")
            if not self.TestSchemasDbExiste():
                log.debug("schemas existe pas ou pas conforme. le cree""")
                self.setSchemaDb() # effet de bord: ecrit dans un fichier sql

    def acces_premier_element_tuple(self,t):
        return t[0]

    def TestDonneesDbExistent(self):
        """teste si chaque table comporte au moins mettons 50 enregistrements"""
        verite = True
        listerToutesTablesSQLImportantes = ( t for t in self.listerToutesTablesSQL() if self.acces_premier_element_tuple(t) != "pff")
        for t in listerToutesTablesSQLImportantes:
            nom_table = self.acces_premier_element_tuple(t)
            e = self.compterEnregistrements(nom_table)
            print ("pour la table {} j ai compte {} enregistrements"
                   .format(t, e))
            if e < 50:
                print ("c est moins de 50")
                verite = False
        return verite
    
    def listerToutesTablesSQL(self):
        """renvoie la liste des tables sql dans une liste de tuples [ (aa,), (bb,)] 
        parce que pas le choix, c est le format de """
        return self.getCnx().execute(
            self.getBibliothecaireDba()
            .getRequeteMetaByName('lister_tables_sql')
            )

    def compterEnregistrements(self,nom_table):
        """ renvoie le nombre d enr d une table"""
        req = self.getBibliothecaireDba().getRequeteMetaByName('nombre_enr_table_param')
        req = req.replace('<TABLE>', nom_table)
        return self.acces_premier_element_tuple(
            self.getCnx().execute(req).fetchone()
            )


    def TestSchemasDbExiste(self):
        """teste si la db obeit bien au schemas.
pour l instant test sommaire: ok si possede au moins une table grace a la
valeur de verite python vraie si liste non nulle.
TODO verifier si les champs de chaque table correspondent
en comparant la table speciale sqlite a une table custom de meme forme
stockant les noms de tables, leurs noms et types de champs et
leurs contraintes"""
        log.debug("verif si schemas db existe et conforme")
        ListeTables = self.getCnx().execute(
            self.getBibliothecaireDba().getRequeteMetaByName('non_vide_si_table_planning_existe').fetchall()
            )
        return ListeTables
    
    def isSqlite3(self,filename):
        """ fich sqlite3?"""
        TAILLE_HEADER_SQLITE3 = 100
        from os.path import isfile, getsize
        if not isfile(filename):
            log.error(filename + " est pas un fich")
            return False
        if getsize (filename) < TAILLE_HEADER_SQLITE3:
            log.error("trop petit pr e fic sqlitr3")
            
            return False
        with open (filename, 'rb') as fd :
            header = fd.read (TAILLE_HEADER_SQLITE3)
            verite = (header [:16] == b'SQLite format 3\x00')
            if not verite:
                log.error("{}: mauvais header sqlite3".format(filename)) 
            else:
                log.info("fichier {} est bien de type sqlite3".format(filename))
            return verite
            
    def TestFichierDbExiste(self):
        """teste l existance d un FICHIER sqlite3"""
        return self.isSqlite3(self.getFichierDb())

    def _connexion_effective(self):
        """effectue la connexion effective. sans condition"""
        import sqlite3
        db = self.getFichierDb()
        param1 = sqlite3.PARSE_DECLTYPES
        param2 = sqlite3.PARSE_COLNAMES
        # autocommit.... pas touche pour l instant
        #isolation_level = None
        masque_options = param1 | param2
        #self.cnx = sqlite3.connect(db,isolation_level, masque_options)
        self.cnx = sqlite3.connect(db)

    def TestAttributCnxExisteEtCnxOuverte(self):
        """doit provoquer un attributError si self.cnx existe pas et un sqlite.programmingError si la cnx est fermée. ne sert à rien d autre"""

        self.cnx.execute("SELECT 1 FROM "
                 + self.getNomTablePostes()
                 + " LIMIT 1") #FAIL IF self.cnx does not exist

        
    
    def setCnx (self):
        """ fournit cnx a db existante """
        import sqlite3
        from sqlite3 import ProgrammingError #le cas de la cnx fermee
        from sqlite3 import OperationalError #cas de départ : le cas de la table planning existant pas encore dans
        try:
            self.TestAttributCnxExisteEtCnxOuverte()
        except (AttributeError,ProgrammingError,OperationalError) as e :
            log.debug("soit attribut cnx de realdb existe pas, soit objet_cnx pointe sur cnx fermée. dans les deux cas je dois creer un attribut cnx pour real_db et lui affecter une connexion ouverte donc en creer une nouvelle")
            log.debug(e)
            self._connexion_effective()
        finally:
            log.debug("que la connexion et l attribut cnx existaient ou pas avant cet appel, maintenant tout est en ordre")


    def fermerCnx(self):
        """ferme une cnx et le dit pr debug"""
        log.debug("je ferme la cnx")
        self.getCnx().close()

    def createDbFile(self):
        """cree un fichier db"""
        con = self.getCnx()
        con.execute('CREATE TABLE pff( mouais TEXT);')
        con.commit()
        con.execute('INSERT INTO pff(mouais) VALUES ("gibberish");')
        con.commit()
        self.fermerCnx()
        
            
            
            
    def getNomTablePostes(self):
        """renvoie le nom de la table des postes, premiere table so far"""
        return "planning"
    
    def getCnx (self):
        """renvoie le jeton de cnx.
        en cree un nv jmsi neceds
        EAFP way"""
        self.setCnx()
        return self.cnx

    def getCursor(self):
        """renvoie un objet iterable sur les resultats
    d une requete"""
        return self.getCnx().cursor()

    def setSchemaDb(self):
        """cree la structure de la base si elle n existe pas"""
        """ TODO: déplacer chacune de ces fonctions dans pkg_crea_base """
        log.debug("creation du schemas")
        self.getCnx().execute(
            self.getBibliothecaireDba()
            .getRequeteCreaByName('creer_tables_datetimeexperimentalsqlite3')
            
            )
##        self.getCnx().execute(
##            self.getBibliothecaireDba()
##            .getRequeteCreaByName('creer_table_joursTravailles')
##            )
        self.getCnx().execute(
            self.getBibliothecaireDba()
            .getRequeteCreaByName('creer_table_periodesTravaillees_datetimeexperimentalsqlite3')
            )
        
        self.getCnx().execute(
            self.getBibliothecaireDba()
            .getRequeteCreaByName('creer_trig_aj_periode_trav_from_scission_poste')
            )
        
        self.getCnx().execute(
            self.getBibliothecaireDba()
            .getRequeteCreaByName('creer_trig_aj_periode_trav_from_copy_poste')
            )
        self.getCnx().execute(
            self.getBibliothecaireDba()
            .getRequeteCreaByName('vue_35_semaine')
            )
        self.getCnx().execute(
            self.getBibliothecaireDba()
            .getRequeteCreaByName('vue_CP_semaine')
            )
        self.getCnx().execute(
            self.getBibliothecaireDba()
            .getRequeteCreaByName('vue_35_semaine_hsup_sans_bonif')
            )
        self.getCnx().execute(
            self.getBibliothecaireDba()
            .getRequeteCreaByName('plus_de_48_heures')
            )
        
        self.getCnx().execute(
            self.getBibliothecaireDba()
            .getRequeteCreaByName('hs_dues_hebdo')
            )
        self.getCnx().execute(
            self.getBibliothecaireDba()
            .getRequeteCreaByName('vue_heures_annu_janjan')
            )
        self.getCnx().execute(
            self.getBibliothecaireDba()
            .getRequeteCreaByName('vue_cumul_annu_juin_a_mai')
            )
        
        
        log.debug("schemas doit maintenant etre cree")
                              
    
              
    def getAllPostes (self):
        """ resp faciliter debug en
renvoyant tous les postes 
sans retraitement"""
        return self.getCnx().execute(
        	self.getBibliothecaireDba()
                .getRequeteLectureByName('tous_postes')
                ).fetchall()

    def renvoyerCurseurRequeteLecture(self,requete):
        """renvoyer le curseur pour une requete
select fournit un o iterable sur une requete
sans faire un fetchone qui renvoie un resultat """
        return self.getCursor().execute(requete)

    def iterAllPostes(self):
        """renvoie un iterateur sur la requete tous postes
        moins lourd à l exe que getAllPostes normalement"""
        texterequete = self.getBibliothecaireDba().getRequeteLectureByName('tous_postes')
        return self.renvoyerCurseurRequeteLecture(texterequete)

    def acces_premier_element_tuple(self,tup):
        return tup[0]

    def iterAnneesDispo(self):
        """renvoie un iterateur aux annees disponibles"""
        texterequete = self.getBibliothecaireDba().getRequeteLectureByName('annees_dispo')
        for a in self.renvoyerCurseurRequeteLecture(texterequete):
            annee = a[0]
            yield int(annee)

    def getNomsTables(self):
        """renvoie le nom des tables dispo hors sqlite_master """
        texterequete = self.getBibliothecaireDba(
            ).getRequeteMetaByName('nom_des_tables')
        return [
            member[1] for member in self.getCnx(
                ).execute(texterequete).fetchall()]


    def getNomsColonnes(self, nom_table):
        """ renvoie le nom des colonnes d une table existante"""
        texterequete = self.getBibliothecaireDba(
            ).getRequeteLectureByName('astuce_noms_colonnes')
        texterequete = texterequete.replace('<NOM_TABLE>', nom_table)
        return next(
            zip(*self.renvoyerCurseurRequeteLecture(texterequete).description)
            )
        
        

        

    
    

class bibliothecaire_dba (object):
        """ resp conn texte ttes les
        requetes creation
        lecture 
        ecriture
        """
        def __init__(self):
            self.setDicoRequetes()

        def getNomTablePlanning(self):
            return "planning"
            
        def setDicoRequetes (self):
            nom_table_liste_postes = self.getNomTablePlanning()
            def initialiser_structure_dico_requetes():
                self.dicorequetes = {}
                self.dicorequetes.setdefault('agregation', {})
                self.dicorequetes.setdefault('lecture', {})
                self.dicorequetes.setdefault('ecriture', {})
                self.dicorequetes.setdefault('meta', {})
                self.dicorequetes.setdefault('crea', {})
                
            initialiser_structure_dico_requetes()
            # les clefs existant pas provoquent des KeyErrors


            self.dicorequetes['meta'].setdefault('nom_des_tables',
                                                 '''
                                                SELECT
                                                *
                                                FROM
                                                sqlite_master
                                                WHERE type="table"
                                                ;
                                                ''')
            self.dicorequetes['meta'].setdefault('non_vide_si_table_planning_existe',
                                                 """SELECT name from sqlite_master where type='table' and name = 'planning';"""
                                                
                                                  
                                                 )
            self.dicorequetes['meta'].setdefault('nombre_postes_saisis',
                                                       "SELECT COUNT(*) FROM "
                                                        + nom_table_liste_postes
                                                       )

            self.dicorequetes['meta'].setdefault('nombre_periodes_travaillees_saisies',
                                                 '''SELECT COUNT(*)
                                                    FROM
                                                    periodes_travaillees
                                                    ;''')
            self.dicorequetes['meta'].setdefault('lister_tables_sql',
                                                 '''SELECT 
                                                         name 
                                                    FROM
                                                        sqlite_master
                                                    WHERE 
                                                        type="table"
                                                        ;
                                                        ''')
            self.dicorequetes['meta'].setdefault('nombre_postes_saisis',
                                                       "SELECT COUNT(*) FROM "
                                                        + nom_table_liste_postes
                                                       )
            self.dicorequetes['meta'].setdefault('nombre_enr_table_param',
                                                 '''SELECT 
                                                     COUNT(*)
                                                    FROM
                                                        <TABLE>
                                                    ;
                                                 ''')
            
            # convertisseur de texte vers timestamp existe par defaut. rend non nécessaire l ecriture d un convertisseur sqllite3->py
            # pour le text iso8601 string (sqlite3) -> timestamp (python)
            # car déjà fourni
            # sinon ben def converter_timestamp, sqlite3.register_converter("timestamp", converter_timestamp)
            self.dicorequetes['lecture'].setdefault('periodes_cp_entre_deux_dates',
                                                    '''SELECT
                                                            debut_poste as "debut_poste [timestamp]",
                                                            fin_poste as "fin_poste [timestamp]"
                                                        FROM
                                                            planning
                                                        WHERE
                                                                planning.categorie_poste = 'absence'
                                                            AND
                                                                nom_poste = 'CP'
                                                            AND
                                                                date( planning.debut_poste )
                                                                    BETWEEN
                                                                        date ( ? )
                                                                    AND
                                                                        date ( ? )
                                                        ; -- NON CLASSE
                                                    
                                                    ''')

            self.dicorequetes['lecture'].setdefault('periodes_travaillees_entre_deux_dates',
                                                    '''SELECT
                                                            debut_periode as "debut_periode [timestamp]",
                                                            fin_periode as "fin_periode [timestamp]"
                                                        FROM
                                                            periodes_travaillees
                                                        WHERE
                                                            date( periodes_travaillees.jour_travaille )
                                                            BETWEEN
                                                                    date ( ? )
                                                                AND
                                                                    date( ? ) 
                                                            ; -- C33''')

            self.dicorequetes['lecture'].setdefault('annees_dispo','''SELECT DISTINCT strftime("%Y",debut_poste) from planning''')
            
            self.dicorequetes['lecture'].setdefault('tous_postes',
                                                    """SELECT debut_poste as 'd [timestamp]', fin_poste as 'f [timestamp]', nom_poste, categorie_poste from """
                                                     + nom_table_liste_postes
                                                    )
            self.dicorequetes['lecture'].setdefault('postes_debutes_ou_termines_ou_les_deux_dans_annee',
                                                    """SELECT debut_poste as 'd [timestamp]', fin_poste as 'f [timestamp]' 
                                                    from planning 
                                                    WHERE  d > ?  AND f <= ?"""
                                                    )
            self.dicorequetes['lecture'].setdefault('astuce_noms_colonnes',
                                                    '''
                                                    SELECT
                                                    *
                                                    FROM
                                                    <NOM_TABLE>
                                                    limit 1
                                                    ;
                                                    ''')
            self.dicorequetes['crea'].setdefault('vue_35_semaine',
                                                   """
                                                    CREATE VIEW vue_35_semaine
                                                    AS
                                                    SELECT
                                                        strftime('%Y', datetime(jour_travaille, 'start of day', 'weekday 0')) as annee,
                                                        strftime('%m', datetime(jour_travaille, 'start of day', 'weekday 0')) as mois,
                                                        ( strftime('%j', datetime(jour_travaille, 'start of day', '-3 days', 'weekday 4')) - 1 ) / 7 + 1 as semaine,
                                                        round( SUM( (JulianDay(fin_periode) - JulianDay(debut_periode)) * 24  ) )as heure_semaine_travaillees
                                                    FROM periodes_travaillees
                                                    GROUP BY annee, mois, semaine
                                                    ;
                                                    """)

            self.dicorequetes['crea'].setdefault('vue_CP_semaine',
                                                 """
                                                CREATE VIEW 'vue_CP_semaine'
                                                AS
                                                SELECT
                                                    strftime('%Y', 
                                                        datetime(planning.debut_poste, 'start of day', 'weekday 0')) as annee,
                                                 strftime('%m', datetime(planning.debut_poste, 'start of day', 'weekday 0')) as mois, 
                                                 ( strftime('%j', datetime(planning.debut_poste, 'start of day', '-3 days', 'weekday 4')) - 1 ) / 7 + 1 as semaine, 
                                                 round( SUM( (JulianDay(fin_poste) - JulianDay(debut_poste)) * 24 ), 2 )as heure_semaine_CP
                                                 FROM 
                                                    planning 
                                                WHERE 
                                                    planning.nom_poste = 'CP'
                                                GROUP BY annee, mois, semaine
                                                ;""")

            self.dicorequetes['crea'].setdefault('vue_35_semaine_hsup_sans_bonif',
                                                """
                                                CREATE VIEW 'vue_35_semaine_hsup_sans_bonif'
                                                AS
                                                SELECT strftime('%Y', datetime(jour_travaille, 'start of day', 'weekday 0')) as annee,
                                                strftime('%m', datetime(jour_travaille, 'start of day', 'weekday 0')) as mois,
                                                ( strftime('%j', datetime(jour_travaille, 'start of day', '-3 days', 'weekday 4')) - 1 ) / 7 + 1 as semaine, 
                                                round( SUM( (JulianDay(fin_periode) - JulianDay(debut_periode)) * 24 ) )as heure_semaine_travaillees,
                                                4 as heure_sup_payee_25,
                                                 max(0, 
                                                     min(round( SUM( 
                                                                     (JulianDay(fin_periode)
                                                                     -
                                                                     JulianDay(debut_periode)) 
                                                * 24 ) ) - 35, 43 - 35)
                                                )	as heures_sup_25_effectuees_semaine ,
                                                
                                                 max(0, 
                                                     min(round( SUM( 
                                                     (JulianDay(fin_periode) - JulianDay(debut_periode)) 
                                            		* 24 ) ) - 43, 48 - 43)
                                                )	as heures_sup_50_effectuees_semaine ,
                                                
                                                max(0, 
                                                     min(round( SUM( 
                                                     (JulianDay(fin_periode) - JulianDay(debut_periode)) 
                                                        * 24 ) ) - 48, 1000 - 48)
                                                    )	as heures_sup_50_ille_semaine 	
                                                FROM periodes_travaillees
                                                GROUP BY annee, mois, semaine
                                                ;
                                                """
                                                 )
            self.dicorequetes['crea'].setdefault('plus_de_48_heures',
                                                 """
                                                create view 'plus_de_48'
                                                    as
                                                select
                                                    *
                                                from
                                                    vue_35_semaine 
                                                where
                                                    vue_35_semaine.heure_semaine_travaillees
                                                    > 48
                                                ;
                                                """)

            self.dicorequetes['crea'].setdefault('hs_dues_hebdo',
                                                 """
                                                CREATE VIEW
                                                    'hs_dues_hebdo'
                                                AS
                                                SELECT
                                                    table_hs_hebdo.a as a,
                                                    table_hs_hebdo.m as m,
                                                    table_hs_hebdo.s as s,
                                                    table_hs_hebdo.t as t,
                                                    table_hs_hebdo.hs_25_hebdo - table_hs_hebdo.cte as hs_25_dues,
                                                    table_hs_hebdo.hs_50_hebdo as h50_l,
                                                    table_hs_hebdo.hs_ille_hebdo as h50_i,
                                                    table_hs_hebdo.hs_50_hebdo + table_hs_hebdo.hs_ille_hebdo as hs_50_dues,
                                                    (table_hs_hebdo.hs_25_hebdo - table_hs_hebdo.cte) * 1.25 as eqv_t_hs_25_dues,
                                                    table_hs_hebdo.hs_50_hebdo * 1.5 as eqv_t_hs_50_l_dues,
                                                    table_hs_hebdo.hs_ille_hebdo * 1.5 as eqv_t_hs_50_i_dues,
                                                    (table_hs_hebdo.hs_50_hebdo * 1.5) + (table_hs_hebdo.hs_ille_hebdo * 1.5) + (table_hs_hebdo.hs_25_hebdo - table_hs_hebdo.cte) * 1.25 as eqv_t_tot_h_dues
                                                FROM
                                                    (
                                                    SELECT 
                                                        table_h_hebdo.annee as a, 
                                                        table_h_hebdo.mois as m,
                                                        table_h_hebdo.semaine as s,
                                                        table_h_hebdo.trav as t,
                                                        4 as cte,
                                                        max(0, min(table_h_hebdo.trav - 35, 43 - 35) )  as hs_25_hebdo,
                                                        max(0, min(table_h_hebdo.trav - 43, 48 - 43) ) as hs_50_hebdo,
                                                        max(0, min(table_h_hebdo.trav - 48, 1000 - 48) )  as hs_ille_hebdo
                                                    FROM 
                                                        ( SELECT
                                                        --  LA SUBQUERY DE BASE : a m s hs_trav_hebdo
                                                        -- les périodes
                                                        -- p1 : année
                                                        strftime('%Y', 
                                                                datetime(jour_travaille, 
                                                                        'start of day', 
                                                                        'weekday 0')) 
                                                                as annee, 
                                                        -- p2: mois
                                                        strftime('%m', 
                                                                datetime(jour_travaille, 
                                                                'start of day', 
                                                                'weekday 0')) 
                                                            as mois, 
                                                        -- p3: semaine
                                                        ( strftime('%j', 
                                                                datetime(jour_travaille, 
                                                                'start of day', 
                                                                '-3 days', 
                                                                'weekday 4')) - 1 ) / 7 + 1 
                                                        as semaine, 
                                                        -- fin des périodes

                                                        -- début des calculs

                                                        -- c1 heures effectuées dans la semaine
                                                        -- somme les differences d heures chaque jour.
                                                        --  technique : la différence est en jour. 
                                                        --         conversion en heures? * 24. 
                                                        --          round pour faire bonne mesure. 
                                                        -- dans le group by, on indique que cette somme se limite
                                                        --- à la semaine:
                                                        round( 
                                                                SUM( 
                                                                        (
                                                                            JulianDay(fin_periode) 
                                                                            - 
                                                                            JulianDay(debut_periode)
                                                                        ) 
                                                                    * 24 )
				)
                                                                as trav



                                                        FROM periodes_travaillees GROUP BY annee, mois, semaine
                                                        ) table_h_hebdo
                                                    ) table_hs_hebdo
                                                            ;


                                                
                                                """
                                                 
                                                 )
            self.dicorequetes['crea'].setdefault('vue_heures_annu_janjan',
                                                 """
                                                CREATE view 'VUE_heures_annu_janjan'
                                                AS
                                                SELECT 
                                                strftime('%Y', datetime(jour_travaille))
                                                as annee, 
                                                strftime('%m', datetime(jour_travaille)) as mois, 
                                                ( strftime('%j', datetime(jour_travaille, 'start of day', '-3 days', 'weekday 4')) - 1 ) / 7 + 1 as semaine,
                                                 round( SUM( (JulianDay(fin_periode) - JulianDay(debut_periode)) * 24 ) )
                                                 as heure_semaine_travaillees 
                                                FROM periodes_travaillees 
                                                GROUP BY annee

                                                ;

                                                    """)
            self.dicorequetes['crea'].setdefault('vue_cumul_annu_juin_a_mai',
                                                    """create view
                                                        'vue_cumul_annu_juin_a_mai'
                                                            as
                                                            select 
                                                            sem_annu_juin_a_mai.annee_annu as annee_annu, 
                                                            sem_annu_juin_a_mai.mois as mois ,
                                                            sum(sem_annu_juin_a_mai.heure_semaine_travaillees) as vol_annu
                                                            from 

                                                            -- fonctionne. il faut grouper par annee_annu maintenant
                                                            (SELECT 
                                                            CAST(strftime('%Y', datetime(jour_travaille))  AS INTEGER) as repere,
                                                            CAST(strftime('%m', datetime(jour_travaille))  AS INTEGER) > 5 as bool,
                                                            strftime('%Y', datetime(jour_travaille)) as resultat_si_vrai,
                                                            strftime('%Y', datetime(jour_travaille)) - 1 as resultat_si_faux,

                                                            CASE 
                                                                    WHEN cast(strftime('%m', datetime(jour_travaille)) as INTEGER) > 5 THEN strftime('%Y', datetime(jour_travaille))
                                                                    ELSE strftime('%Y', datetime(jour_travaille, '-1 year'))
                                                            END annee_annu, 

                                                            strftime('%Y', datetime(jour_travaille))
                                                                    as annee, 
                                                            strftime('%m', datetime(jour_travaille)) as mois, 
                                                            ( strftime('%j', datetime(jour_travaille, 'start of day', '-3 days', 'weekday 4')) - 1 ) / 7 + 1 
                                                            as semaine,
                                                            datetime(jour_travaille, 'start of day', '-3 days', 'weekday 4') as debut_semaine,
                                                             round( SUM( (JulianDay(fin_periode) - JulianDay(debut_periode)) * 24 ) )
                                                             as heure_semaine_travaillees 
                                                            FROM periodes_travaillees 
                                                            GROUP BY annee_annu, mois, semaine
                                                            ORDER BY annee_annu, mois, semaine ) sem_annu_juin_a_mai
                                                            GROUP BY annee_annu
                                                            ;
                                                            """)

            """
TODO: crea vue prenant en compte les jours feries
afin de
crea vue fusionner prenant en compte les heures sup
- les jours ou jours fériers
SELECT 

strftime('%Y', 
 
		datetime(planning.debut_poste, 'start of day', 'weekday 0')
		) as annee,
date(planning.debut_poste) as jour,
round((JulianDay(planning.fin_poste) - 
JulianDay(planning.debut_poste)) * 24, 2) as duree,
planning.nom_poste
		
FROM
	planning
WHERE
   planning.categorie_poste = 'absence'
 AND
	planning.nom_poste = 'CP'



'vue_35_semaine'






-- je veux choisir
-- chaque annee_cp, mois_cp, semaine
--    (le rattachement des semaines au mois est 
--    sur le mode des heures sup)
-- afin de renvoyer le nombre de jours de cp chaque semaine


-- premiere partie du select:
-- je veux l'annee à laquelle est rattachée le jour cp
-- les jours cp sont sur une seule journee
-- je peux donc prendre la date de debut_poste
--   ou 
--   la date de fin_poste
--  mais la conversion en date est inutile:
-- stfrtime prend indifférement une ch date ou datetime

     -- l'annee de 
	  -- la semaine à laquelle appartient
	  -- le dernier jour 
	  -- de la semaine de cp



SELECT 

strftime('%Y', 
 
		datetime(planning.debut_poste, 'start of day', 'weekday 0')
		) as annee,
planning.debut_poste,
planning.fin_poste,
planning.nom_poste
		
FROM
	planning
WHERE
   planning.categorie_poste = 'absence'
 AND
	planning.nom_poste = 'CP'
	
	; """
            self.dicorequetes['crea'].setdefault('creer_tables',
                                                 '''CREATE TABLE {} (
                                                     idx_planning INTEGER NOT NULL PRIMARY KEY,
                                                    debut_poste TEXT,
                                                    fin_poste TEXT,
                                                    nom_poste TEXT,
                                                    categorie_poste TEXT,
                                                    CONSTRAINT debut_unique UNIQUE (debut_poste),
                                                    CONSTRAINT fin_unique UNIQUE (fin_poste))'''
                                                 .format(nom_table_liste_postes)
                                                 )

            self.dicorequetes['crea'].setdefault('creer_tables_datetimeexperimentalsqlite3',
                                                 '''CREATE TABLE {}(
                                                        idx_planning INTEGER NOT NULL PRIMARY KEY,
                                                        debut_poste timestamp,
                                                        fin_poste timestamp,
                                                        nom_poste TEXT,
                                                        categorie_poste TEXT,
                                                        CONSTRAINT debut_unique UNIQUE (debut_poste),
                                                        CONSTRAINT fin_unique UNIQUE (fin_poste))
                                                        ;'''
                                                 .format(nom_table_liste_postes)
                                                 )

            # cette requete cree la table de JoursTravailles et la table de periodes_travaillees et ajoute le triger de creation de ces champs
            self.dicorequetes['crea'].setdefault('creer_table_joursTravailles',
                                                 '''CREATE TABLE jours_travailles (
                                                    jour TEXT,
                                                    CONSTRAINT jour_unique UNIQUE(jour) ON CONFLICT IGNORE
                                                    )
                                                    ;''')
            self.dicorequetes['crea'].setdefault('creer_table_periodesTravaillees',
                                                 '''CREATE TABLE periodes_travaillees (
                                                    debut_periode TEXT,
                                                    fin_periode TEXT CHECK(fin_periode > debut_periode),
                                                    jour_travaille TEXT,
                                                    CONSTRAINT periode_unique UNIQUE(debut_periode, fin_periode, jour_travaille) 
                                                    )
                                                    ;''')

            self.dicorequetes['crea'].setdefault('creer_table_periodesTravaillees_datetimeexperimentalsqlite3',
                                                 '''CREATE TABLE periodes_travaillees (
                                                    debut_periode timestamp,
                                                    fin_periode timestamp CHECK(fin_periode > debut_periode),
                                                    jour_travaille DATE,
                                                    CONSTRAINT periode_unique UNIQUE(debut_periode, fin_periode, jour_travaille) 
                                                    )
                                                    ;''')

            self.dicorequetes['crea'].setdefault('creer_trig_aj_periode_trav_from_scission_poste',
                                                 '''CREATE TRIGGER t1 AFTER INSERT ON planning
                                                    WHEN (( NEW.categorie_poste = 'travaillé') AND( date( NEW.debut_poste )  < date ( NEW.fin_poste )) )
                                                    -- entrée à cheval sur deux jours,
                                                    -- il faut la splitter avant insertion
                                                    -- vers periode_travaillée
                                                    BEGIN
                                                    -- CONTRAT D INSERTION
                                                    -- 1er insert : de debut_poste
                                                    -- à fin(jour_calendaire(debut_poste))
                                                    -- C26
                                                    INSERT INTO
                                                        periodes_travaillees (debut_periode, fin_periode, jour_travaille)
                                                    VALUES (
                                                            datetime(NEW.debut_poste),
                                                            datetime(NEW.debut_poste, '+1 day','start of day'),
                                                            date(NEW.debut_poste)
                                                            )
                                                    ;
                                                     -- FIN DU 1ER INSERT C26
                                                     -- CONTRAT D INSERTION
                                                     -- 2eme insert: de fin(jour_calendaire(debut_poste)
                                                     -- à fin_poste
                                                     -- C27
                                                     INSERT INTO
                                                     periodes_travaillees
                                                     (debut_periode, fin_periode, jour_travaille)
                                                     VALUES (datetime(NEW.debut_poste, '+1 day', 'start of day'),
                                                             datetime(NEW.fin_poste),
                                                             date(NEW.fin_poste)
                                                             )
                                                    ; -- FIN DE 2EME INSERT C27
                                                    END; --fin du trigger ''')
            self.dicorequetes['crea'].setdefault('creer_trig_aj_periode_trav_from_copy_poste','''
                                                    CREATE TRIGGER t2 AFTER INSERT ON planning
                                                    WHEN (( NEW.categorie_poste = 'travaillé' ) AND ( date (NEW.debut_poste ) = date (NEW.fin_poste ) ) )
                                                    -- entree sur un seul jour
                                                    -- insertion telle quelle de debut_poste et fin_poste vers période_travaillée
                                                    BEGIN
                                                    -- CONTRAT D INSERTION
                                                    -- 1 UNIQUE INSERT: de debut_poste à fin_poste
                                                    -- C28
                                                    INSERT INTO
                                                    periodes_travaillees
                                                    (debut_periode, fin_periode, jour_travaille)
                                                    VALUES (
                                                            datetime(NEW.debut_poste),
                                                            datetime(NEW.fin_poste),
                                                            date(NEW.debut_poste)
                                                            )
                                                    ; -- FIN DE L INSERT UNIQUE C28
                                                    END; -- FIN DU TRIGGER C29''')

            self.dicorequetes['crea'].setdefault('creer_trigger_ajout_jourstravailles_et_periodestravaillees',
                                                 """CREATE TRIGGER
                                                    ajoutperiodestravtrig
                                                    AFTER
                                                        INSERT ON
                                                        planning
                                                    WHEN NEW.categorie_poste = 'travaillé'
                                                    BEGIN
                                                        INSERT OR IGNORE INTO
                                                            jours_travailles (jour)
                                                        SELECT date(NEW.debut_poste) UNION SELECT date(NEW.fin_poste)
                                                        
                                                        ;

                                                        INSERT INTO
                                                            periodes_travaillees (debut_periode, fin_periode, jourtravaille)
                                                        SELECT
                                                            NEW.debut_poste,

                                                            CASE
                                                                WHEN
                                                                    date(NEW.fin_poste)
                                                                    >
                                                                    date(NEW.debut_poste)
                                                                THEN datetime(date(NEW.debut_poste,'+1day'))
                                                                ELSE NEW.fin_poste
                                                            END fin_periode,
                                                            date(NEW.debut_poste)
                                                            FROM planning
                                                           ;
                                                           
                                                        INSERT INTO
                                                            periodes_travaillees (debut_periode, fin_periode, jourtravaille)
                                                        SELECT
                                                            CASE
                                                                WHEN
                                                                    date(NEW.fin_poste)
                                                                    >
                                                                    date(NEW.debut_poste)
                                                                THEN datetime(date(NEW.debut_poste,'+1day'))
                                                                ELSE NEW.debut_poste
                                                            END debut_periode,
                                                            NEW.fin_poste
                                                            date(NEW.fin_poste)
                                                            FROM planning
                                                           ;
                                                                                                                ;
                                                        END;
                                                    """)
            # a chaque creation de poste
            

            # cette premiere version de saisie nécessite l utilisation de liste comme champ de saisie en deuxieme parma de execute(sql, liste)
            # la nature des champs dans la db dépoend donc de l ordre ds lequ les elements st jectes ds la liste python
            # bof
            self.dicorequetes['ecriture'].setdefault('saisir_entree',
                                                     "INSERT OR IGNORE INTO " + nom_table_liste_postes + " (debut_poste, fin_poste, nom_poste, categorie_poste) VALUES (?, ?, ?, ?)")

            #cette variante de saisie permet d utiliser des dicos comme champs de saisie en deuxieme parametre de execute(sql, dico)
            # la nature des champs ds la db depend donc de leur nom dans le dico python, donc mieux
            # 
            self.dicorequetes['ecriture'].setdefault('saisir_entree_variante_dico',
                                                     "INSERT INTO " + nom_table_liste_postes + " VALUES (debut_poste=:, fin_poste:=, nom_poste=:, categorie_poste=:)")
                                                 

                                                 

        

            
        
        def getRequeteTypedByName(self, TYPE, nom):
            """ fournit le texte d une requete de type TYPE"""
            if nom in self.dicorequetes[TYPE].keys():
                return self.dicorequetes[TYPE][nom]
            else:
                raise Exception("requete existe pas " + nom)
            
        def getRequeteMetaByName(self, nom):
            """ fournit le texte d une requete de type info sur struct db stockee ds db sqlite3"""
            return self.getRequeteTypedByName('meta',nom)

        def getRequeteLectureByName(self, nom):
            """fournit le texte d une requte de type lecture"""
            return self.getRequeteTypedByName('lecture', nom)

        def getRequeteCreaByName(self, nom):
            """fournit le texte d une requete de type creation"""
            return self.getRequeteTypedByName('crea', nom)
            
        
        def getListeRequeteLecture(self,nom):
            """renvoie la liste des requetes de type lecture"""
            return self.getRequeteTypedByName('meta',nom)

        def getRequeteEcritureByName(self, nom):
            """fournit le texte d une requte de type ecriture"""
            return self.getRequeteTypedByName('ecriture', nom)



        

    
        
        
        
    

    

