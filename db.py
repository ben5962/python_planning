#-*-coding:utf8;-*-
#qpy:2
#qpy:consol

class bdd (object):
    """
    bdd est un proxy vers realdb et 
    1) . doit connaitre tous les postes.
    . (pour annu 1er jan 31 dec < 1607h):
    doit pouvoir renvoyer 
    une liste de postes 


    effectues sur une année ( 1er jan 0h 
    	a 31 dec 23h59 disons 1er jan 0h)
    	- si le 31 dec a - 1 est travaillé 
    	et que la fin du poste est au delà
    	
    en ajoutant la troncature du 
    poste du 31 déc nuit
     si necessaire
    . (pour hsup 35h): doit renvoyer 
    une liste de postes
    les postes aĺlant du premier
    lundi de la semaine compre
     de la semaine 1 iso 8901, l
     en la complétant éventuellement
     à la dernière semaine.
     2) connait tous les noms de classes de taches de verif 
   
     """
    import calendar
    import calendrierComptable

    def __init__(self):
        self.setListeNomsEtapesVerificationMensuelle()

        #self.cal = calendar.Calendar()
        pass

        

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
            return realdb().getAllPostes()
            
      


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
        self.setCnx()

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

    def setSchema(self,schema="schema_planning"):
        """doit mettre en base de donnees le schemas a valider en db"""
        
    
    def setFichierDb(self,filename):
        """ doit affecter la valeur filename a self.fichierdb
et s assurer que le fichier existe qu il est une base sqlite3
et que la base a le bon schemas"""
        self.fichierdb = filename
        db = self.getFichierDb()
        if not self.TestFichierDbExiste():
            """le fichier est cree en cnnct a fichier
q existe pas et fermant cnx"""
            print(self.getFichierDb() + "existe pas . le cree.""")
            self.createDbFile()
        print("teste si le schemas existe")
        if not self.TestSchemasDbExiste():
            print("schemas existe pas ou pas conforme. le cree""")
            self.setSchemaDb() # effet de bord: ecrit dans un fichier sql


    def TestSchemasDbExiste(self):
        """teste si la db obeit bien au schemas.
pour l instant test sommaire: ok si possede au moins une table grace a la
valeur de verite python vraie si liste non nulle.
TODO verifier si les champs de chaque table correspondent
en comparant la table speciale sqlite a une table custom de meme forme
stockant les noms de tables, leurs noms et types de champs et
leurs contraintes"""
        print("verif si schemas db existe et conforme")
        ListeTables = self.getCnx().execute(self.getBibliothecaireDba()
                                .getRequeteMetaByName('non_vide_si_table_planning_existe')[0],
                                            self.getBibliothecaireDba().getRequeteMetaByName('non_vide_si_table_planning_existe')[1]).fetchall()
        return ListeTables
    
    def isSqlite3(self,filename):
        """ fich sqlite3?"""
        TAILLE_HEADER_SQLITE3 = 100
        from os.path import isfile, getsize
        if not isfile(filename):
            print (filename + "est pas un fich")
            return False
        if getsize (filename) < TAILLE_HEADER_SQLITE3:
            print ("trop petit pr e fic sqlitr3")
            return False
        with open (filename, 'rb') as fd :
            header = fd.read (TAILLE_HEADER_SQLITE3)
            return header [:16] == 'SQLite format 3\x00'
            
    def TestFichierDbExiste(self):
        """teste l existance d un FICHIER sqlite3"""
        return self.isSqlite3(self.getFichierDb())

    def _connexion_effective(self):
        """effectue la connexion effective. sans condition"""
        import sqlite3
        db = self.getFichierDb()
        param1 = sqlite3.PARSE_DECLTYPES
        param2 = sqlite3.PARSE_COLNAMES
        masque_options = param1 | param2
        self.cnx = sqlite3.connect(db, masque_options)

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
            print("soit attribut cnx de realdb existe pas, soit objet_cnx pointe sur cnx fermée. dans les deux cas je dois creer un attribut cnx pour real_db et lui affecter une connexion ouverte donc en creer une nouvelle", e)
            self._connexion_effective()
        finally:
            print("que la connexion et l attribut cnx existaient ou pas avant cet appel, maintenant tout est en ordre")


    def fermerCnx(self,cnx):
        """ferme une cnx et le dit pr debug"""
        print("je ferme la cnx")
        cnx.close()

    def createDbFile(self):
        """cree un fichier db"""
        con = self.getCnx()
        self.fermerCnx(con)
        
            
            
            
    def getNomTablePostes(self):
        """renvoie le nom de la table des postes, premiere table so far"""
        return "planning"
    
    def getCnx (self):
        """renvoie le jeton de cnx.
        en cree un nv jmsi neceds
        EAFP way"""
        self.setCnx()
        return self.cnx

    def setSchemaDb(self):
        """cree la structure de la base si elle n existe pas"""
        print("creation du schemas")
        self.getCnx().execute(
            self.getBibliothecaireDba()
            .getRequeteCreaByName('creer_tables')
            )
        print("schemas doit maintenant etre cree")
                              
    
              
    def getAllPostes (self):
        """ resp faciliter debug en
renvoyant tous les postes 
sans retraitement"""
        return self.getCnx().execute(
        	self.getBibliothecaireDba()
                .getRequeteLectureByName('tous_postes')
                ).fetchall()
    

class bibliothecaire_dba (object):
        """ resp conn texte ttes les
        requetes creation
        lecture 
        ecriture
        """
        def __init__(self):
            self.setDicoRequetes()
            
        def setDicoRequetes (self):
            nom_table_liste_postes = "planning"
            self.dicorequetes = {}
            # les clefs existant pas provoquent des KeyErrors
            self.dicorequetes.setdefault('agregation', {})
            self.dicorequetes.setdefault('lecture', {})
            self.dicorequetes.setdefault('ecriture', {})
            self.dicorequetes.setdefault('meta', {})
            self.dicorequetes.setdefault('crea', {})
            self.dicorequetes['meta'].setdefault('non_vide_si_table_planning_existe',
                                                 ("SELECT name from sqlite_master where type='table' and name = ?",
                                                  (nom_table_liste_postes,)
                                                  )
                                                 )
            self.dicorequetes['meta'].setdefault('nombre_postes_saisis',
                                                       "SELECT COUNT(*) FROM "
                                                        + nom_table_liste_postes
                                                       )
            # convertisseur de texte vers timestamp existe par defaut. rend non nécessaire l ecriture d un convertisseur sqllite3->py
            # pour le text iso8601 string (sqlite3) -> timestamp (python)
            # car déjà fourni
            # sinon ben def converter_timestamp, sqlite3.register_converter("timestamp", converter_timestamp)
            
            self.dicorequetes['lecture'].setdefault('tous_postes',
                                                    """SELECT debut_poste as 'd [timestamp]', fin_poste as 'f [timestamp]', nom_poste, categorie_poste from """
                                                     + nom_table_liste_postes
                                                    )
            self.dicorequetes['lecture'].setdefault('postes_debutes_ou_termines_ou_les_deux_dans_annee',
                                                    ("""SELECT debut_poste as 'd [timestamp]', fin_poste as 'f [timestamp]' from """
                                                     + nom_table_liste_postes
                                                     + """WHERE  d > ?  AND f <= ?""", "" )
                                                    )
            self.dicorequetes['crea'].setdefault('creer_tables',
                                                 "CREATE TABLE {} ( debut_poste TEXT, fin_poste TEXT, nom_poste TEXT, categorie_poste TEXT, CONSTRAINT debut_unique UNIQUE (debut_poste), CONSTRAINT fin_unique UNIQUE (fin_poste))".format(nom_table_liste_postes)
                                                 )

            self.dicorequetes['crea'].setdefault('creer_tables_datetimeexperimentalsqlite3',
                                                 "CREATE TABLE {} ( debut_poste timestamp, fin_poste timestamp, nom_poste TEXT, categorie_poste TEXT, CONSTRAINT debut_unique UNIQUE (debut_poste), CONSTRAINT fin_unique UNIQUE (fin_poste))".format(nom_table_liste_postes)
                                                 )
            

            # cette premiere version de saisie nécessite l utilisation de liste comme champ de saisie en deuxieme parma de execute(sql, liste)
            # la nature des champs dans la db dépoend donc de l ordre ds lequ les elements st jectes ds la liste python
            # bof
            self.dicorequetes['ecriture'].setdefault('saisir_entree',
                                                     "INSERT INTO " + nom_table_liste_postes + " (debut_poste, fin_poste, nom_poste, categorie_poste) VALUES (?, ?, ?, ?)")

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


class Entree(object):
    
    """{'day': 13, 'month': 12, 'year': 2014, 'poste': 'P1'}
une entree est une a deux dates et un un type de pose et
une categorie de poste il a la responsabilite de renvovyer une representation
exte et qqch qui lui permettra d etre envoye et retour dans la base de donnees"""
    import constantes
    import datetime
    def __init__(self,ligne_poste):
        self.ligne_poste = ligne_poste
        self.setNomPoste()
        self.setDebutPoste()
        self.setFinPoste()
        self.setCategorie()

    def getLignePoste(self):
        return self.ligne_poste

    def getYear(self):
        return self.getLignePoste()['year']

    def getMonth(self):
        return self.getLignePoste()['month']

    def getDay(self):
        return self.getLignePoste()['day']

    def setNomPoste(self):
        self.nom_poste = self.getLignePoste()['poste']

    def getNomPoste(self):
        return self.nom_poste

    def getHeureDebut(self):
        return self.constantesGetHeureDebutFromNomPoste(self.getNomPoste())

    def constantesGetHeureDebutFromNomPoste(self,nomposte):
        import constantes
        return constantes.postes[nomposte]['heure_debut']

    def setDebutPoste(self):
        import datetime
        
        date_debut_poste = datetime.date(
            self.getYear(),
            self.getMonth(),
            self.getDay()
            )                                        
        heure_debut_poste = datetime.time(self.getHeureDebut())
        self.debut_poste = datetime.datetime.combine(date_debut_poste,
                                                     heure_debut_poste)
    def getDebutPoste(self):
        return self.debut_poste

    def constantesGetDureeFromNomPoste(self,nomposte):
        import constantes
        return constantes.postes[nomposte]['duree']

    def getDureePoste(self):
        return self.constantesGetDureeFromNomPoste(self.getNomPoste())

    def setFinPoste(self):
        import datetime
        self.fin_poste = self.getDebutPoste() + datetime.timedelta(hours = self.getDureePoste())

    def getFinPoste(self):
        return self.fin_poste

    def setCategorie(self):
        self.categorie = self.constantesGetCategorieFromNomPoste(self.getNomPoste())

    def constantesGetCategorieFromNomPoste(self, nomposte):
        import constantes
        return constantes.postes[nomposte]['categ']

    def getCategorie(self):
        return self.categorie
    
    def representation(self):
        return "{},{},{}, {}".format(self.getDebutPoste(), self.getFinPoste(), self.getNomPoste(), self.getCategorie())

    def to_dict(self):
        return { 'debut_poste' : self.getDebutPoste(), 'fin_poste' : self.getFinPoste(), 'nom_poste' : self.getNomPoste(), 'categorie' : self.getCategorie() }

    
        

        

    
        
        
        
    
class larbin (object):
    """a la resp de
    remplir la base de postes
    depuis les fichiers texte
    a la resp de remplir la base
    de fiches de p reelles
    a la resp de converting depuis la base les postes en journees trav
    a la resp de remplir la base de journees travaillees
    """
    def __init__(self):
        self.db = realdb()
        self.bib = bibliothecaire_dba()

    def getDb(self):
        return self.db

    def getBibliothecaireDba(self):
        return self.bib
    
    def a_saisir(self):
        import xpld
        
        fichiers_larbin = ["2014.txt","2015.txt","2016.txt"]
        for fichier in fichiers_larbin:
            with open(fichier) as f:
                for ligne_fichier in f:
                    for ligne_poste in xpld.xpld().xplode_ite(ligne_fichier):
                        print(Entree(ligne_poste).representation())

    def a_saisir_test_dico(self):
        import xpld
        
        fichiers_larbin = ["2014.txt","2015.txt","2016.txt"]
        for fichier in fichiers_larbin:
            with open(fichier) as f:
                for ligne_fichier in f:
                    for ligne_poste in xpld.xpld().xplode_ite(ligne_fichier):
                        print(Entree(ligne_poste).to_dict())

    def gen_dico_entree_ite(self):
        import xpld
        
        fichiers_larbin = ["2014.txt","2015.txt","2016.txt"]
        for fichier in fichiers_larbin:
            with open(fichier) as f:
                for ligne_fichier in f:
                    for ligne_poste in xpld.xpld().xplode_ite(ligne_fichier):
                        yield Entree(ligne_poste)

    def saisir(self):
        for entree in self.gen_dico_entree_ite():
            print("ecriture de ", entree.getDebutPoste(),entree.getFinPoste(), entree.getNomPoste(), entree.getCategorie())
            self.getDb().getCnx().execute(self.getBibliothecaireDba().getRequeteEcritureByName('saisir_entree'),
                                          (entree.getDebutPoste(),
                                           entree.getFinPoste(),
                                           entree.getNomPoste(),
                                           entree.getCategorie()
                                           )
                                          )
        

            self.getDb().getCnx().commit()
            print("ecriture commitée")


    def test_saisir(self):
        for entree in self.gen_dico_entree_ite():
            print(entree.getDebutPoste(), entree.getFinPoste(), entree.getNomPoste(), entree.getCategorie())

    def verifier_travail(self):
        """verifie que le nombre de saisies dans la base n est pas nul"""
        tuple_resultat = self.getDb().getCnx().execute(self.getBibliothecaireDba()
                                    .getRequeteMetaByName('nombre_postes_saisis')
                                    ).fetchone()
        nb = tuple_resultat[0] #le nombre doit etre extrait du tuple
        for member in tuple_resultat:
            print("le nombre d elements de planning saisis est de : {}"
                  .format(nb)
                  )
        if nb:  #vrai si non nul
            return True
        else:
            return False
        

##Traceback (most recent call last):
##  File "<pyshell#38>", line 1, in <module>
##    a.saisir()
##  File "C:\Users\Utilisateur\Documents\GitHub\python_planning\db.py", line 430, in saisir
##    (entree.to_dict()['debut_poste'], entree.to_dict()['fin_poste'], entree.to_dict['nom_poste'],
##TypeError: 'method' object is not subscriptable
##>>> import sqlite3
##>>> a = sqlite3.connect(":memory:")
##>>> a.execute("create table essai (dt datetime)")
##<sqlite3.Cursor object at 0x02326C60>
##>>> a.commit()
##>>> import datetime
##>>> a = { le_datetime : datetime.datetime.now() }
##Traceback (most recent call last):
##  File "<pyshell#44>", line 1, in <module>
##    a = { le_datetime : datetime.datetime.now() }
##NameError: name 'le_datetime' is not defined
##>>> a = { "le_datetime" : datetime.datetime.now() }
##>>> a
##{'le_datetime': datetime.datetime(2017, 4, 15, 9, 8, 19, 169198)}
##>>> a = sqlite3.connect(":memory:")
##>>> a.execute("create table essai (dt datetime)")
##<sqlite3.Cursor object at 0x02326C20>
##>>> a.commit()
##>>> dico = { "le_datetime" : datetime.datetime.now() }
##>>> a.execute("insert into essai values (dt =: le_datetime) ", dico)
##Traceback (most recent call last):
##  File "<pyshell#51>", line 1, in <module>
##    a.execute("insert into essai values (dt =: le_datetime) ", dico)
##sqlite3.OperationalError: unrecognized token: ":"
##            
        

    



class Regle(object):
    """ a la responsabilité:
- de creer une regle sous forme de champ d init dans fpaie reelle
- de creer un seuil
- de calculer le delta
- de chiffrer le delta
"""


    
                
                
        
    
    



class jourTravaille(object):
    """ doit representer la pkus petite
unite dont sont composees
les semaines 39 (dc besoin num sem
et num mois)
et les annees annu (ts jrs depuis 1er 
jan au 31 dec)
liste de periodes de trav (deb fin)
sur 24h
-connait le num de sem auquel il 
appartient
-connait le num mois auquel il 
appartient
    		- connait le num annee ausuel il 
    		appartient
"""
    
    pass

class semaineTravaillee(object):
    """pour les 39h regroupe les jours
travaillés de la semaine
chaque semaine comporte 7 jours
et doit etre rattachee a un mois.
cas limite: la semaine a cheval 
sur deux mois. doit elle etre rattachee
au mois ou elle commence ou au mois ou elle
se termine?
1er cas alors il faut inclure la semaine
de postes pas terminee au 31 dec
et exclure la 1ere semaine de jan
si elle est incomplete (commence pas par
	lundi).
2eme cas alors il faut inclure a la
1ere semaine de janvier, incomplete,
les jours de la dern sem de dec, incomplete
en effet annee du 1er jan au 31 dec.
donc exclusion des sem incomplete au 31
de l annee en cours
donc regul sur mois annee suivante
donc regul prec rattache au mois de janvier
"""
    pass
