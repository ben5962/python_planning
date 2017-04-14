#-*-coding:utf8;-*-
#qpy:2
#qpy:console

class db (object):
    """. doit connaitre tous les postes.
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
     à la dernière semaine. """
    def getPostes (self,name):
        
        if name == "all":
            return realdb().getAllPostes()
            
      
    pass
      


class realdb (object):
    """fait toutes les requetes
    vers la db que ce soit
    - la crea de la strucure de la table
    - dispo pour son remplissage
    - dispo pour les req en lecture si présence de champs"""
    def __init__(self, fichdb='planning.db'):
        """ besoins: nomfichdb"""
        self.setBibliothecaire_Dba()
        self.fichierdb = "" # initialise par setFichierDb
        self.setFichierDb (fichdb)
        # apres cette etape le fichier existe forcement
        # la db a le bon schemas
        # structure
        #self.cnx = "" # initialise par setCnx
        self.setCnx()

    def setBibliothecaire_Dba(self):
        """initialise un bibliothecaire. le lie a l objet realdb"""
        self.bibliothecaire_dba = bibliothecaire_dba()

    def getBibliothecaire_Dba(self):
        """si pas de bibli, le cree. sinon utilise l existant"""
        if self.bibliothecaire_dba is None:
            self.setBibliothecaire_Dba()
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
        ListeTables = self.getCnx().execute(self.getBibliothecaire_Dba()
                                .getRequeteMetaByName('nom_tables_existantes')[0],
                                            self.getBibliothecaire_Dba().getRequeteMetaByName('nom_tables_existantes')[1]).fetchall()
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
    
    def setCnx (self):
        """ fournit cnx a db existante """
        import sqlite3
        print("creation de la cnx")
        db = self.getFichierDb()
        param1 = sqlite3.PARSE_DECLTYPES
        param2 = sqlite3.PARSE_COLNAMES
        masque_options = param1 | param2
        self.cnx = sqlite3.connect(db, masque_options)
        print("cnx doit etre cree desormais")


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
        print("recup d une cnx")
        import sqlite3
        self.setCnx()
        return self.cnx
##        try:
##            print("cnx existe deja?")
##            self.cnx.execute("SELECT 1 FROM ? LIMIT 1", (self.getNomTablePostes(),)) #FAIL IF self.cnx does not exist
##        except AttributeError or sqlite3.ProgrammingError :
##            print("existe pas dois la creer")
##            self.setCnx()
##        finally: 
##            return self.cnx

    def setSchemaDb(self):
        """cree la structure de la base si elle n existe pas"""
        print("creation du schemas")
        self.getCnx().execute(
            self.getBibliothecaire_Dba()
            .getRequeteCreaByName('creer_tables')
            )
        print("schemas doit maintenant etre cree")
                              
    
              
    def getAllPostes (self):
        """ resp faciliter debug en
renvoyant tous les postes 
sans retraitement"""
        self.getCnx().execute(
        	bibliothecaire_dba.getRequeteLectureByName('tous_postes'))
    pass

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
            self.dicorequetes['meta'].setdefault('nom_tables_existantes',
                                                 ("SELECT name from sqlite_master where type='table' and name = ?",
                                                  (nom_table_liste_postes,)
                                                  )
                                                 )
            self.dicorequetes['agregation'].setdefault('nb_postes_saisis',
                                                       ("SELECT COUNT(*) FROM table "
                                                        + nom_table_liste_postes, )
                                                       )
            self.dicorequetes['lecture'].setdefault('tous_postes',
                                                    ("""SELECT debut_poste as 'd [timestamp]', fin_poste as 'f [timestamp]' from """
                                                     + nom_table_liste_postes, "" )
                                                    )
            self.dicorequetes['lecture'].setdefault('postes_debutes_ou_termines_ou_les_deux_dans_annee',
                                                    ("""SELECT debut_poste as 'd [timestamp]', fin_poste as 'f [timestamp]' from """
                                                     + nom_table_liste_postes
                                                     + """WHERE  d > ?  AND f <= ?""", "" )
                                                    )
            self.dicorequetes['crea'].setdefault('creer_tables',
                                                 "CREATE TABLE {} ( debut_poste TEXT, fin_poste TEXT, type_poste TEXT, CONSTRAINT debut_unique UNIQUE (debut_poste), CONSTRAINT fin_unique UNIQUE (fin_poste))".format(nom_table_liste_postes)
                                                 )
                                                 

        

            
        
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
        self.fin_poste = self.getDebutPoste() + datetime.timedelta(self.getDureePoste())

    def getFinPoste(self):
        return self.fin_poste

    
    
    def representation(self):
        return "{},{},{}".format(self.getDebutPoste(), self.getFinPoste(), self.getNomPoste())
        

        

    
        
        
        
    
class larbin (object):
    """a la resp de
    remplir la base de postes
    depuis les fichiers texte
    a la resp de remplir la base
    de fiches de p reelles
    """
    def doit(self):
        import xpld
        fichiers_larbin = ["2014.txt","2015.txt","2016.txt"]
        for fichier in fichiers_larbin:
            with open(fichier) as f:
                for ligne_fichier in f:
                    for ligne_poste in xpld.xpld().xplode_ite(ligne_fichier):
                        print(Entree(ligne_poste).representation())
    

class auditeur  (object ):
    """a la rep de lancer
    une tache errpaye nommee ou
    toutes les taches errpaye
    et presenter le resultat dans un
    rapport formate"""
    pass


class fpaiereelle (object):
    """resp repr fpaie reelle
    pour un mois donne et une
    annee donnee.
    """
    def __init__(self, mois=1, annee=2002, hsup25=0, hsup50=0, hdim10=0, hjf100=0, hnuit10=0):
        this.mois = mois
        this.annee = annee
        this.hsup25 = hsup25
        this.hsup50 = hsup50
        this.hdim10 = hdim10
        this.hnuit10 = hnuit10
        this.hjf100 = hjf100
    pass


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
