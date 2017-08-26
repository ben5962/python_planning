'''
Created on 22 juil. 2017

@author: Utilisateur
'''
import os.path
import ntpath
import glob
import sys
# aaaaaaaaaaaaaaaaaaaaaaaaaaaargh
from pathlib import Path
p = Path('.')
p = '..' / p
sys.path.insert(0, os.path.abspath(p))
from pkg_utilitaires_repertoires.glob_etc import *
# fin de aaaaaaaaaaaaaaaaargh

class bibliothecaire_dba (object):
        """ resp conn texte ttes les
        requetes creation
        lecture
        ecriture
        """
        def __init__(self):
            self.types_de_requete = set()
            self.setDicoRequetes()


        def getNomTablePlanning(self):
            return "planning"

        def setDicoRequetes (self):
            nom_table_liste_postes = self.getNomTablePlanning()
            ###### DEBUT DECLARATIONS #########################
            def initialiser_structure_dicorequetes():
                self.dicorequetes = {}

                # les clefs existant pas provoquent des KeyErrors
            def ajouter_type_requete_structure_dicorequetes(typerequete):
                self.dicorequetes.setdefault(typerequete, {})

            def creerglobs():
                nom_rel_rep_dest = 'requetes_sql_a_importer'
                chemin_repertoire = os.path.join(os.path.dirname(__file__), nom_rel_rep_dest)
                chemin_courant = os.path.abspath(__file__)
                globs = getListeFichiersGlobsDansChemin(getAssemblageCheminFicheretSousRep(chemin_courant,
                                                                                          nom_rel_rep_dest),
                                                '*.sql')
                return globs

            def ajouter_types_requetes_structure_dicorequetes(globs):
                for script_sql in globs:
                    nom_fichier = ntpath.basename(script_sql)
                    type_requete = nom_fichier[0:nom_fichier.index('_')]
                    self.types_de_requete.add(type_requete)

                for type_requete in self.types_de_requete:
                    ajouter_type_requete_structure_dicorequetes(type_requete)




            def importer_texte_requetes(globs):
                for script_sql in glo:
                    nom_fichier = ntpath.basename(script_sql)
                    # lettre apres le '_' de  méta_ 
                    nom_script =  nom_fichier[nom_fichier.index('_') + 1:]
                    # jusqu'au . de .sql
                    nom_script =  nom_script[0:nom_script.index('.')]
                    type_requete = nom_fichier[0:nom_fichier.index('_')]
                    with open(script_sql, encoding='utf8') as s:
                        self.dicorequetes[type_requete].setdefault(nom_script,s.read())






            ######## FIN DECLARATIONS #####################

            initialiser_structure_dicorequetes()
            glo = creerglobs()
            ajouter_types_requetes_structure_dicorequetes(glo)
            importer_texte_requetes(glo)



#             self.dicorequetes['migra'].setdefault('ajout_pk_a_table_planning',
#                                                   '''pragma foreign_keys=off;
#
# BEGIN TRANSACTION;
# ALTER TABLE planning RENAME TO anc_planning;
#
# CREATE TABLE
# nv_planning(
#     idx_planning INTEGER NOT NULL PRIMARY KEY,
#     debut_poste timestamp,
#     fin_poste timestamp,
#     nom_poste TEXT,
#     categorie_poste TEXT,
#     CONSTRAINT debut_unique UNIQUE (debut_poste),
#     CONSTRAINT fin_unique UNIQUE (fin_poste));
#
# INSERT INTO nv_planning SELECT * FROM anc_planning;
# ALTER TABLE nv_planning RENAME TO planning;
# COMMIT;
# PRAGMA foreign_keys=on;
#      ''')
#
#             self.dicorequetes['meta'].setdefault('nom_des_tables',
#                                                  '''
#                                                 SELECT
#                                                 *
#                                                 FROM
#                                                 sqlite_master
#                                                 WHERE type="table"
#                                                 ;
#                                                 ''')
#             self.dicorequetes['meta'].setdefault('non_vide_si_table_planning_existe',
#                                                  ("SELECT name from sqlite_master where type='table' and name = ?",
#                                                   (nom_table_liste_postes,)
#                                                   )
#                                                  )
#             self.dicorequetes['meta'].setdefault('nombre_postes_saisis',
#                                                        "SELECT COUNT(*) FROM "
#                                                         + nom_table_liste_postes
#                                                        )
#
#             self.dicorequetes['meta'].setdefault('nombre_periodes_travaillees_saisies',
#                                                  '''SELECT COUNT(*)
#                                                     FROM
#                                                     periodes_travaillees
#                                                     ;''')
#             self.dicorequetes['meta'].setdefault('lister_tables_sql',
#                                                  '''SELECT
#                                                          name
#                                                     FROM
#                                                         sqlite_master
#                                                     WHERE
#                                                         type="table"
#                                                         ;
#                                                         ''')
#             self.dicorequetes['meta'].setdefault('nombre_postes_saisis',
#                                                        "SELECT COUNT(*) FROM "
#                                                         + nom_table_liste_postes
#                                                        )
#             self.dicorequetes['meta'].setdefault('nombre_enr_table_param',
#                                                  '''SELECT
#                                                      COUNT(*)
#                                                     FROM
#                                                         <TABLE>
#                                                     ;
#                                                  ''')
#
#             # convertisseur de texte vers timestamp existe par defaut. rend non nécessaire l ecriture d un convertisseur sqllite3->py
#             # pour le text iso8601 string (sqlite3) -> timestamp (python)
#             # car déjà fourni
#             # sinon ben def converter_timestamp, sqlite3.register_converter("timestamp", converter_timestamp)
#             self.dicorequetes['lecture'].setdefault('periodes_cp_entre_deux_dates',
#                                                     '''SELECT
#                                                             debut_poste as "debut_poste [timestamp]",
#                                                             fin_poste as "fin_poste [timestamp]"
#                                                         FROM
#                                                             planning
#                                                         WHERE
#                                                                 planning.categorie_poste = 'absence'
#                                                             AND
#                                                                 nom_poste = 'CP'
#                                                             AND
#                                                                 date( planning.debut_poste )
#                                                                     BETWEEN
#                                                                         date ( ? )
#                                                                     AND
#                                                                         date ( ? )
#                                                         ; -- NON CLASSE
#
#                                                     ''')
#
#             self.dicorequetes['lecture'].setdefault('periodes_travaillees_entre_deux_dates',
#                                                     '''SELECT
#                                                             debut_periode as "debut_periode [timestamp]",
#                                                             fin_periode as "fin_periode [timestamp]"
#                                                         FROM
#                                                             periodes_travaillees
#                                                         WHERE
#                                                             date( periodes_travaillees.jour_travaille )
#                                                             BETWEEN
#                                                                     date ( ? )
#                                                                 AND
#                                                                     date( ? )
#                                                             ; -- C33''')
#
#             self.dicorequetes['lecture'].setdefault('annees_dispo','''SELECT DISTINCT strftime("%Y",debut_poste) from planning''')
#
#             self.dicorequetes['lecture'].setdefault('tous_postes',
#                                                     """SELECT debut_poste as 'd [timestamp]', fin_poste as 'f [timestamp]', nom_poste, categorie_poste from """
#                                                      + nom_table_liste_postes
#                                                     )
#             self.dicorequetes['lecture'].setdefault('postes_debutes_ou_termines_ou_les_deux_dans_annee',
#                                                     ("""SELECT debut_poste as 'd [timestamp]', fin_poste as 'f [timestamp]' from """
#                                                      + nom_table_liste_postes
#                                                      + """WHERE  d > ?  AND f <= ?""", "" )
#                                                     )
#             self.dicorequetes['lecture'].setdefault('astuce_noms_colonnes',
#                                                     '''
#                                                     SELECT
#                                                     *
#                                                     FROM
#                                                     <NOM_TABLE>
#                                                     limit 1
#                                                     ;
#                                                     ''')
#             self.dicorequetes['crea'].setdefault('vue_35_semaine',
#                                                    """
#                                                     CREATE VIEW vue_35_semaine
#                                                     AS
#                                                     SELECT
#                                                         strftime('%Y', datetime(jour_travaille, 'start of day', 'weekday 0')) as annee,
#                                                         strftime('%m', datetime(jour_travaille, 'start of day', 'weekday 0')) as mois,
#                                                         ( strftime('%j', datetime(jour_travaille, 'start of day', '-3 days', 'weekday 4')) - 1 ) / 7 + 1 as semaine,
#                                                         round( SUM( (JulianDay(fin_periode) - JulianDay(debut_periode)) * 24  ) )as heure_semaine_travaillees
#                                                     FROM periodes_travaillees
#                                                     GROUP BY annee, mois, semaine
#                                                     ;
#                                                     """)
#
#             self.dicorequetes['crea'].setdefault('vue_CP_semaine',
#                                                  """
#                                                 CREATE VIEW 'vue_CP_semaine'
#                                                 AS
#                                                 SELECT
#                                                     strftime('%Y',
#                                                         datetime(planning.debut_poste, 'start of day', 'weekday 0')) as annee,
#                                                  strftime('%m', datetime(planning.debut_poste, 'start of day', 'weekday 0')) as mois,
#                                                  ( strftime('%j', datetime(planning.debut_poste, 'start of day', '-3 days', 'weekday 4')) - 1 ) / 7 + 1 as semaine,
#                                                  round( SUM( (JulianDay(fin_poste) - JulianDay(debut_poste)) * 24 ), 2 )as heure_semaine_CP
#                                                  FROM
#                                                     planning
#                                                 WHERE
#                                                     planning.nom_poste = 'CP'
#                                                 GROUP BY annee, mois, semaine
#                                                 ;""")
#
#             self.dicorequetes['crea'].setdefault('vue_35_semaine_hsup_sans_bonif',
#                                                 """
#                                                 CREATE VIEW 'vue_35_semaine_hsup_sans_bonif'
#                                                 AS
#                                                 SELECT strftime('%Y', datetime(jour_travaille, 'start of day', 'weekday 0')) as annee,
#                                                 strftime('%m', datetime(jour_travaille, 'start of day', 'weekday 0')) as mois,
#                                                 ( strftime('%j', datetime(jour_travaille, 'start of day', '-3 days', 'weekday 4')) - 1 ) / 7 + 1 as semaine,
#                                                 round( SUM( (JulianDay(fin_periode) - JulianDay(debut_periode)) * 24 ) )as heure_semaine_travaillees,
#                                                 4 as heure_sup_payee_25,
#                                                  max(0,
#                                                      min(round( SUM(
#                                                                      (JulianDay(fin_periode)
#                                                                      -
#                                                                      JulianDay(debut_periode))
#                                                 * 24 ) ) - 35, 43 - 35)
#                                                 )    as heures_sup_25_effectuees_semaine ,
#
#                                                  max(0,
#                                                      min(round( SUM(
#                                                      (JulianDay(fin_periode) - JulianDay(debut_periode))
#                                                 * 24 ) ) - 43, 48 - 43)
#                                                 )    as heures_sup_50_effectuees_semaine ,
#
#                                                 max(0,
#                                                      min(round( SUM(
#                                                      (JulianDay(fin_periode) - JulianDay(debut_periode))
#                                                         * 24 ) ) - 48, 1000 - 48)
#                                                     )    as heures_sup_50_ille_semaine
#                                                 FROM periodes_travaillees
#                                                 GROUP BY annee, mois, semaine
#                                                 ;
#                                                 """
#                                                  )
#             self.dicorequetes['crea'].setdefault('plus_de_48_heures',
#                                                  """
#                                                 create view 'plus_de_48'
#                                                     as
#                                                 select
#                                                     *
#                                                 from
#                                                     vue_35_semaine
#                                                 where
#                                                     vue_35_semaine.heure_semaine_travaillees
#                                                     > 48
#                                                 ;
#                                                 """)
#
#             self.dicorequetes['crea'].setdefault('hs_dues_hebdo',
#                                                  """
#                                                 CREATE VIEW
#                                                     'hs_dues_hebdo'
#                                                 AS
#                                                 SELECT
#                                                     table_hs_hebdo.a as a,
#                                                     table_hs_hebdo.m as m,
#                                                     table_hs_hebdo.s as s,
#                                                     table_hs_hebdo.t as t,
#                                                     table_hs_hebdo.hs_25_hebdo - table_hs_hebdo.cte as hs_25_dues,
#                                                     table_hs_hebdo.hs_50_hebdo as h50_l,
#                                                     table_hs_hebdo.hs_ille_hebdo as h50_i,
#                                                     table_hs_hebdo.hs_50_hebdo + table_hs_hebdo.hs_ille_hebdo as hs_50_dues,
#                                                     (table_hs_hebdo.hs_25_hebdo - table_hs_hebdo.cte) * 1.25 as eqv_t_hs_25_dues,
#                                                     table_hs_hebdo.hs_50_hebdo * 1.5 as eqv_t_hs_50_l_dues,
#                                                     table_hs_hebdo.hs_ille_hebdo * 1.5 as eqv_t_hs_50_i_dues,
#                                                     (table_hs_hebdo.hs_50_hebdo * 1.5) + (table_hs_hebdo.hs_ille_hebdo * 1.5) + (table_hs_hebdo.hs_25_hebdo - table_hs_hebdo.cte) * 1.25 as eqv_t_tot_h_dues
#                                                 FROM
#                                                     (
#                                                     SELECT
#                                                         table_h_hebdo.annee as a,
#                                                         table_h_hebdo.mois as m,
#                                                         table_h_hebdo.semaine as s,
#                                                         table_h_hebdo.trav as t,
#                                                         4 as cte,
#                                                         max(0, min(table_h_hebdo.trav - 35, 43 - 35) )  as hs_25_hebdo,
#                                                         max(0, min(table_h_hebdo.trav - 43, 48 - 43) ) as hs_50_hebdo,
#                                                         max(0, min(table_h_hebdo.trav - 48, 1000 - 48) )  as hs_ille_hebdo
#                                                     FROM
#                                                         ( SELECT
#                                                         --  LA SUBQUERY DE BASE : a m s hs_trav_hebdo
#                                                         -- les périodes
#                                                         -- p1 : année
#                                                         strftime('%Y',
#                                                                 datetime(jour_travaille,
#                                                                         'start of day',
#                                                                         'weekday 0'))
#                                                                 as annee,
#                                                         -- p2: mois
#                                                         strftime('%m',
#                                                                 datetime(jour_travaille,
#                                                                 'start of day',
#                                                                 'weekday 0'))
#                                                             as mois,
#                                                         -- p3: semaine
#                                                         ( strftime('%j',
#                                                                 datetime(jour_travaille,
#                                                                 'start of day',
#                                                                 '-3 days',
#                                                                 'weekday 4')) - 1 ) / 7 + 1
#                                                         as semaine,
#                                                         -- fin des périodes
#
#                                                         -- début des calculs
#
#                                                         -- c1 heures effectuées dans la semaine
#                                                         -- somme les differences d heures chaque jour.
#                                                         --  technique : la différence est en jour.
#                                                         --         conversion en heures? * 24.
#                                                         --          round pour faire bonne mesure.
#                                                         -- dans le group by, on indique que cette somme se limite
#                                                         --- à la semaine:
#                                                         round(
#                                                                 SUM(
#                                                                         (
#                                                                             JulianDay(fin_periode)
#                                                                             -
#                                                                             JulianDay(debut_periode)
#                                                                         )
#                                                                     * 24 )
#         )
#                                                                 as trav
#
#
#
#                                                         FROM periodes_travaillees GROUP BY annee, mois, semaine
#                                                         ) table_h_hebdo
#                                                     ) table_hs_hebdo
#                                                             ;
#
#
#
#                                                 """
#
#                                                  )
#             self.dicorequetes['crea'].setdefault('vue_heures_annu_janjan',
#                                                  """
#                                                 CREATE view 'VUE_heures_annu_janjan'
#                                                 AS
#                                                 SELECT
#                                                 strftime('%Y', datetime(jour_travaille))
#                                                 as annee,
#                                                 strftime('%m', datetime(jour_travaille)) as mois,
#                                                 ( strftime('%j', datetime(jour_travaille, 'start of day', '-3 days', 'weekday 4')) - 1 ) / 7 + 1 as semaine,
#                                                  round( SUM( (JulianDay(fin_periode) - JulianDay(debut_periode)) * 24 ) )
#                                                  as heure_semaine_travaillees
#                                                 FROM periodes_travaillees
#                                                 GROUP BY annee
#
#                                                 ;
#
#                                                     """)
#             self.dicorequetes['crea'].setdefault('vue_cumul_annu_juin_a_mai',
#                                                     """create view
#                                                         'vue_cumul_annu_juin_a_mai'
#                                                             as
#                                                             select
#                                                             sem_annu_juin_a_mai.annee_annu as annee_annu,
#                                                             sem_annu_juin_a_mai.mois as mois ,
#                                                             sum(sem_annu_juin_a_mai.heure_semaine_travaillees) as vol_annu
#                                                             from
#
#                                                             -- fonctionne. il faut grouper par annee_annu maintenant
#                                                             (SELECT
#                                                             CAST(strftime('%Y', datetime(jour_travaille))  AS INTEGER) as repere,
#                                                             CAST(strftime('%m', datetime(jour_travaille))  AS INTEGER) > 5 as bool,
#                                                             strftime('%Y', datetime(jour_travaille)) as resultat_si_vrai,
#                                                             strftime('%Y', datetime(jour_travaille)) - 1 as resultat_si_faux,
#
#                                                             CASE
#                                                                     WHEN cast(strftime('%m', datetime(jour_travaille)) as INTEGER) > 5 THEN strftime('%Y', datetime(jour_travaille))
#                                                                     ELSE strftime('%Y', datetime(jour_travaille, '-1 year'))
#                                                             END annee_annu,
#
#                                                             strftime('%Y', datetime(jour_travaille))
#                                                                     as annee,
#                                                             strftime('%m', datetime(jour_travaille)) as mois,
#                                                             ( strftime('%j', datetime(jour_travaille, 'start of day', '-3 days', 'weekday 4')) - 1 ) / 7 + 1
#                                                             as semaine,
#                                                             datetime(jour_travaille, 'start of day', '-3 days', 'weekday 4') as debut_semaine,
#                                                              round( SUM( (JulianDay(fin_periode) - JulianDay(debut_periode)) * 24 ) )
#                                                              as heure_semaine_travaillees
#                                                             FROM periodes_travaillees
#                                                             GROUP BY annee_annu, mois, semaine
#                                                             ORDER BY annee_annu, mois, semaine ) sem_annu_juin_a_mai
#                                                             GROUP BY annee_annu
#                                                             ;
#                                                             """)
#
#             """
# TODO: crea vue prenant en compte les jours feries
# afin de
# crea vue fusionner prenant en compte les heures sup
# - les jours ou jours fériers
# SELECT
#
# strftime('%Y',
#
#     datetime(planning.debut_poste, 'start of day', 'weekday 0')
#     ) as annee,
# date(planning.debut_poste) as jour,
# round((JulianDay(planning.fin_poste) -
# JulianDay(planning.debut_poste)) * 24, 2) as duree,
# planning.nom_poste
#
# FROM
#   planning
# WHERE
#    planning.categorie_poste = 'absence'
#  AND
#   planning.nom_poste = 'CP'
#
#
#
# 'vue_35_semaine'
#
#
#
#
#
#
# -- je veux choisir
# -- chaque annee_cp, mois_cp, semaine
# --    (le rattachement des semaines au mois est
# --    sur le mode des heures sup)
# -- afin de renvoyer le nombre de jours de cp chaque semaine
#
#
# -- premiere partie du select:
# -- je veux l'annee à laquelle est rattachée le jour cp
# -- les jours cp sont sur une seule journee
# -- je peux donc prendre la date de debut_poste
# --   ou
# --   la date de fin_poste
# --  mais la conversion en date est inutile:
# -- stfrtime prend indifférement une ch date ou datetime
#
#      -- l'annee de
#     -- la semaine à laquelle appartient
#     -- le dernier jour
#     -- de la semaine de cp
#
#
#
# SELECT
#
# strftime('%Y',
#
#     datetime(planning.debut_poste, 'start of day', 'weekday 0')
#     ) as annee,
# planning.debut_poste,
# planning.fin_poste,
# planning.nom_poste
#
# FROM
#   planning
# WHERE
#    planning.categorie_poste = 'absence'
#  AND
#   planning.nom_poste = 'CP'
#
#   ; """
#             self.dicorequetes['crea'].setdefault('creer_tables',
#                                                  '''CREATE TABLE {} (
#                                                      index_planning INTEGER NOT NULL PRIMARY KEY,
#                                                     debut_poste TEXT,
#                                                     fin_poste TEXT,
#                                                     nom_poste TEXT,
#                                                     categorie_poste TEXT,
#                                                     CONSTRAINT debut_unique UNIQUE (debut_poste),
#                                                     CONSTRAINT fin_unique UNIQUE (fin_poste))'''
#                                                  .format(nom_table_liste_postes)
#                                                  )
#
#             self.dicorequetes['crea'].setdefault('creer_tables_datetimeexperimentalsqlite3',
#                                                  '''CREATE TABLE {}(
#                                                           index_planning INTEGER NOT NULL PRIMARY KEY,
#                                                         debut_poste timestamp,
#                                                         fin_poste timestamp,
#                                                         nom_poste TEXT,
#                                                         categorie_poste TEXT,
#                                                         CONSTRAINT debut_unique UNIQUE (debut_poste),
#                                                         CONSTRAINT fin_unique UNIQUE (fin_poste))
#                                                         ;'''
#                                                  .format(nom_table_liste_postes)
#                                                  )
#
#             # cette requete cree la table de JoursTravailles et la table de periodes_travaillees et ajoute le triger de creation de ces champs
#             self.dicorequetes['crea'].setdefault('creer_table_joursTravailles',
#                                                  '''CREATE TABLE jours_travailles (
#                                                     jour TEXT,
#                                                     CONSTRAINT jour_unique UNIQUE(jour) ON CONFLICT IGNORE
#                                                     )
#                                                     ;''')
#             self.dicorequetes['crea'].setdefault('creer_table_periodesTravaillees',
#                                                  '''CREATE TABLE periodes_travaillees (
#                                                     debut_periode TEXT,
#                                                     fin_periode TEXT CHECK(fin_periode > debut_periode),
#                                                     jour_travaille TEXT,
#                                                     CONSTRAINT periode_unique UNIQUE(debut_periode, fin_periode, jour_travaille)
#                                                     )
#                                                     ;''')
#
#             self.dicorequetes['crea'].setdefault('creer_table_periodesTravaillees_datetimeexperimentalsqlite3',
#                                                  '''CREATE TABLE periodes_travaillees (
#                                                     debut_periode timestamp,
#                                                     fin_periode timestamp CHECK(fin_periode > debut_periode),
#                                                     jour_travaille DATE,
#                                                     CONSTRAINT periode_unique UNIQUE(debut_periode, fin_periode, jour_travaille)
#                                                     )
#                                                     ;''')
#
#             self.dicorequetes['crea'].setdefault('creer_trig_aj_periode_trav_from_scission_poste',
#                                                  '''CREATE TRIGGER t1 AFTER INSERT ON planning
#                                                     WHEN (( NEW.categorie_poste = 'travaillé') AND( date( NEW.debut_poste )  < date ( NEW.fin_poste )) )
#                                                     -- entrée à cheval sur deux jours,
#                                                     -- il faut la splitter avant insertion
#                                                     -- vers periode_travaillée
#                                                     BEGIN
#                                                     -- CONTRAT D INSERTION
#                                                     -- 1er insert : de debut_poste
#                                                     -- à fin(jour_calendaire(debut_poste))
#                                                     -- C26
#                                                     INSERT INTO
#                                                         periodes_travaillees (debut_periode, fin_periode, jour_travaille)
#                                                     VALUES (
#                                                             datetime(NEW.debut_poste),
#                                                             datetime(NEW.debut_poste, '+1 day','start of day'),
#                                                             date(NEW.debut_poste)
#                                                             )
#                                                     ;
#                                                      -- FIN DU 1ER INSERT C26
#                                                      -- CONTRAT D INSERTION
#                                                      -- 2eme insert: de fin(jour_calendaire(debut_poste)
#                                                      -- à fin_poste
#                                                      -- C27
#                                                      INSERT INTO
#                                                      periodes_travaillees
#                                                      (debut_periode, fin_periode, jour_travaille)
#                                                      VALUES (datetime(NEW.debut_poste, '+1 day', 'start of day'),
#                                                              datetime(NEW.fin_poste),
#                                                              date(NEW.fin_poste)
#                                                              )
#                                                     ; -- FIN DE 2EME INSERT C27
#                                                     END; --fin du trigger ''')
#             self.dicorequetes['crea'].setdefault('creer_trig_aj_periode_trav_from_copy_poste','''
#                                                     CREATE TRIGGER t2 AFTER INSERT ON planning
#                                                     WHEN (( NEW.categorie_poste = 'travaillé' ) AND ( date (NEW.debut_poste ) = date (NEW.fin_poste ) ) )
#                                                     -- entree sur un seul jour
#                                                     -- insertion telle quelle de debut_poste et fin_poste vers période_travaillée
#                                                     BEGIN
#                                                     -- CONTRAT D INSERTION
#                                                     -- 1 UNIQUE INSERT: de debut_poste à fin_poste
#                                                     -- C28
#                                                     INSERT INTO
#                                                     periodes_travaillees
#                                                     (debut_periode, fin_periode, jour_travaille)
#                                                     VALUES (
#                                                             datetime(NEW.debut_poste),
#                                                             datetime(NEW.fin_poste),
#                                                             date(NEW.debut_poste)
#                                                             )
#                                                     ; -- FIN DE L INSERT UNIQUE C28
#                                                     END; -- FIN DU TRIGGER C29''')
#
#             self.dicorequetes['crea'].setdefault('creer_trigger_ajout_jourstravailles_et_periodestravaillees',
#                                                  """CREATE TRIGGER
#                                                     ajoutperiodestravtrig
#                                                     AFTER
#                                                         INSERT ON
#                                                         planning
#                                                     WHEN NEW.categorie_poste = 'travaillé'
#                                                     BEGIN
#                                                         INSERT OR IGNORE INTO
#                                                             jours_travailles (jour)
#                                                         SELECT date(NEW.debut_poste) UNION SELECT date(NEW.fin_poste)
#
#                                                         ;
#
#                                                         INSERT INTO
#                                                             periodes_travaillees (debut_periode, fin_periode, jourtravaille)
#                                                         SELECT
#                                                             NEW.debut_poste,
#
#                                                             CASE
#                                                                 WHEN
#                                                                     date(NEW.fin_poste)
#                                                                     >
#                                                                     date(NEW.debut_poste)
#                                                                 THEN datetime(date(NEW.debut_poste,'+1day'))
#                                                                 ELSE NEW.fin_poste
#                                                             END fin_periode,
#                                                             date(NEW.debut_poste)
#                                                             FROM planning
#                                                            ;
#
#                                                         INSERT INTO
#                                                             periodes_travaillees (debut_periode, fin_periode, jourtravaille)
#                                                         SELECT
#                                                             CASE
#                                                                 WHEN
#                                                                     date(NEW.fin_poste)
#                                                                     >
#                                                                     date(NEW.debut_poste)
#                                                                 THEN datetime(date(NEW.debut_poste,'+1day'))
#                                                                 ELSE NEW.debut_poste
#                                                             END debut_periode,
#                                                             NEW.fin_poste
#                                                             date(NEW.fin_poste)
#                                                             FROM planning
#                                                            ;
#                                                                                                                 ;
#                                                         END;
#                                                     """)
#             # a chaque creation de poste
#
#
#             # cette premiere version de saisie nécessite l utilisation de liste comme champ de saisie en deuxieme parma de execute(sql, liste)
#             # la nature des champs dans la db dépoend donc de l ordre ds lequ les elements st jectes ds la liste python
#             # bof
#             self.dicorequetes['ecriture'].setdefault('saisir_entree',
#                                                      "INSERT OR IGNORE INTO planning (debut_poste, fin_poste, nom_poste, categorie_poste) VALUES (?, ?, ?, ?)")
#
#             #cette variante de saisie permet d utiliser des dicos comme champs de saisie en deuxieme parametre de execute(sql, dico)
#             # la nature des champs ds la db depend donc de leur nom dans le dico python, donc mieux
#             #
#             self.dicorequetes['ecriture'].setdefault('saisir_entree_variante_dico',
#                                                      "INSERT INTO planning VALUES (debut_poste=:, fin_poste:=, nom_poste=:, categorie_poste=:)")
#
#
#
#
#
#


        def getRequeteTypedByName(self, TYPE, nom):
            """ fournit le texte d une requete de type TYPE"""
            if nom in self.dicorequetes[TYPE].keys():
                return self.dicorequetes[TYPE][nom]
            else:
                print("pour le type {} j ai : {}".format(TYPE, self.dicorequetes[TYPE].keys()))
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


        def getListeRequeteLecture(self):
            """renvoie la liste des requetes de type lecture"""
            return self.dicorequetes['lecture'].keys()

        def getRequeteEcritureByName(self, nom):
            """fournit le texte d une requte de type ecriture"""
            return self.getRequeteTypedByName('ecriture', nom)

        def getListeTypesRequetes(self):
            return self.types_de_requete

        def getListeRequetes(self):
            l = list()
            for t in self.types_de_requete:
                l.append(self.dicorequetes[t].keys())
            return l

        def getCountRequetes(self):
            compte = 0
            for t in self.types_de_requete:
                compte = compte + len(self.dicorequetes[t])
                print('pour le type : {} : {} requetes'.format(t, len(self.dicorequetes[t])))
            print('au total: {} requetes'.format(compte))
