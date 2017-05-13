#-*-coding:utf8;-*-
#qpy:2
#qpy:consol
from metier import Entree
class bdd (object):
    """
    les données, indépendemment de leur mode d obtention
    (db, fichier, osef.... typiquement la tete de ligne du modele)
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
     3) connait toutes les annees disponibles
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

        
        pass

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
        self.realdb.saisirToutesEntrees(iterateurEntrees)
        
        
                



        

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

    def saisirToutesEntrees(self, iterateurEntrees):
        """saisit toutes les entrees dans la base"""
        texterequete = self.getBibliothecaireDba().getRequeteEcritureByName('saisir_entree')
        for entree in iterateurEntrees:
##        for entree in self.gen_dico_entree_ite():
##            print("ecriture de ", entree.getDebutPoste(),entree.getFinPoste(), entree.getNomPoste(), entree.getCategorie())
##            self.getDb().getCnx().execute(self.getBibliothecaireDba().getRequeteEcritureByName('saisir_entree'),
##                                          (entree.getDebutPoste(),
##                                           entree.getFinPoste(),
##                                           entree.getNomPoste(),
##                                           entree.getCategorie()
##                                           )
##                                          )
##        
##
##            self.getDb().getCnx().commit()
##            print("ecriture commitée")
            print("ecriture de ", entree),
            self.getCnx().execute(texterequete, entree)
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
        # autocommit.... pas touche pour l instant
        #isolation_level = None
        masque_options = param1 | param2
        #self.cnx = sqlite3.connect(db,isolation_level, masque_options)
        self.cnx = sqlite3.connect(db,masque_options)

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

    def getCursor(self):
        """renvoie un objet iterable sur les resultats
    d une requete"""
        return self.getCnx().cursor()

    def setSchemaDb(self):
        """cree la structure de la base si elle n existe pas"""
        print("creation du schemas")
        self.getCnx().execute(
            self.getBibliothecaireDba()
            .getRequeteCreaByName('creer_tables')
            )
        self.getCnx().execute(
            self.getBibliothecaireDba()
            .getRequeteCreaByName('creer_table_joursTravailles')
            )
        self.getCnx().execute(
            self.getBibliothecaireDba()
            .getRequeteCreaByName('creer_tables_periodesTravaillees')
            )
        self.getCnx().execute(
            self.getBibliothecaireDba()
            .getRequeteCreaByName('creer_trigger_ajout_jourstravailles_et_periodestravaillees')
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

    def iterAnneesDispo(self):
        """renvoie un iterateur aux annees disponibles"""
        texterequete = self.getBibliothecaireDba().getRequeteLectureByName('annees_dispo')
        return self.renvoyerCurseurRequeteLecture(texterequete)
    

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

            self.dicorequetes['lecture'].setdefault('annees_dispo','''SELECT DISTINCT strftime("%Y",debut_poste) from planning''')
            
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
                                                 '''CREATE TABLE {} (
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
            self.dicorequetes['crea'].setdefault('creer_tables_periodesTravaillees',
                                                 '''CREATE TABLE periodes_travaillees (
                                                    debut_periode TEXT,
                                                    fin_periode TEXT CHECK(fin_periode > debut_periode),
                                                    jourtravaille TEXT,
                                                    FOREIGN KEY (jourtravaille) REFERENCES joursTravailles(jour),
                                                    CONSTRAINT periode_unique UNIQUE(debut_periode, fin_periode, jourtravaille) 
                                                    )
                                                    ;''')

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



        

    
        
        
        
    

    

