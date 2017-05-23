#-*-coding:utf8;-*-
#qpy:2
#qpy:consol
from metier import Entree
from metier import timedelta_to_hour
from metier import diff_entre_deux_datestimes


from dateutil.parser import parse
import devpy.develop as log


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

    def TestDonneesDbExistent(self):
        """teste si chaque table comporte au moins mettons 50 enregistrements"""
        verite = True
        for t in self.listerToutesTablesSQL():
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

    def setContentDb(self):
        """remplit la base via larbin si pas remplie"""
        if not self.__nb_lignes_db(): # faux <=> renvoie 0
            print("remplissons la base: elle ne contient aucune entrée actuellement")
            import larbin
            l = larbin.larbin()
            l.saisir()
            
            
        else:
            print("base déjà remplie, rien à faire")
            print("ont déjà été saisis {} postes et {} périodes travaillées".format(self.getNombrePostesSaisis(),
                                                                                    self.getNombrePeriodesTravailleesSaisies()
                                                                                    )
                  )

    def __nb_lignes_db(self):
        return self.getNombrePostesSaisis()
            
            


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
              ]
            )
        return result


    def getListePeriodesTravailleesEntreDeuxDates(self,d1,d2):
        """ datetime.date x datetime.date -> [(dtime_deb, dtime_fin),..(,)]"""
        return self.getCnx().execute(self.getBibliothecaireDba()
                                               .getRequeteLectureByName('periodes_travaillees_entre_deux_dates'),
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
            print("ecriture de ", entree),
            self.getCnx().execute(texterequete, entree)
        self.getCnx().commit()

    def saisir_entree(self, tuple_entree):
        """ saisit 1 entree dans la base """
        texterequete = self.getBibliothecaireDba().getRequeteEcritureByName('saisir_entree')
        print("ecriture de ", tuple_entree),
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
            print("soit attribut cnx de realdb existe pas, soit objet_cnx pointe sur cnx fermée. dans les deux cas je dois creer un attribut cnx pour real_db et lui affecter une connexion ouverte donc en creer une nouvelle", e)
            self._connexion_effective()
        finally:
            print("que la connexion et l attribut cnx existaient ou pas avant cet appel, maintenant tout est en ordre")


    def fermerCnx(self):
        """ferme une cnx et le dit pr debug"""
        print("je ferme la cnx")
        self.getCnx().close()

    def createDbFile(self):
        """cree un fichier db"""
        con = self.getCnx()
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
        print("creation du schemas")
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
