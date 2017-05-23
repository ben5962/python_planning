#-*-coding:utf8;-*-
#qpy:2
#qpy:consol
from metier import Entree
from metier import timedelta_to_hour
from metier import diff_entre_deux_datestimes


from dateutil.parser import parse
import devpy.develop as log


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

            self.dicorequetes['meta'].setdefault('nombre_periodes_travaillees_saisies',
                                                 '''SELECT COUNT(*)
                                                    FROM
                                                    periodes_travaillees
                                                    ;''')
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

