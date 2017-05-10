# coding: utf-8
import unittest
import sqlite3
from fichiersTemporaires import writeFichierTemporaire, getFichierTemporaire, readFichierTemporaire
#import module_repertoire
#import os

# Autogenerated with DRAKON Editor 1.28

def creer_fichier_random(rep):
    #item 278
    import tempfile
    import os
    #item 279
    ou = os.path.abspath(rep)
    
    with tempfile.NamedTemporaryFile(delete=False, dir=ou) as bigfile:
        bigfile.seek(size - 1)
        bigfile.write("0")


def creer_rep():
    #item 285
    import tempfile
    import os
    #item 284
    ch = tempfile.mkdtemp(dir=os.getcwd())
    return ch


def les_requetesql_ne_veulent_pas_de_newline_en_plein_milieu(chaine):
    #item 124
    return  chaine.replace('\n',' ')

class testbdd(unittest.TestCase):
    """nettoyage table vs space ok space partout"""
    



    def assertSameFileContent(self, fich1, fich2):
        #item 306
        assertion = False
        for ligne in readFichierTemporaire(fich1):
            l = readLineFichierTemporaire(fich2)
            if ligne == l:
                assertion = True
                print("les lignes sont similaires")
            else:
                print("les fichiers diffèrent: ",ligne, " vs ", l)
        return assertion


    def setUpClass(cls):
        #item 110
        """AVANT TOUS LES TESTS 
        env test:
        une bdd en mémoire"""
        #item 54
        cls.cnx = sqlite3.connect(':memory:')
        """ nettoyage tab vs space ok. spaces ok"""
        with open('schema.sql','r') as f:
            req = f.read()
            req = les_requetesql_ne_veulent_pas_de_newline_en_plein_milieu(req)
            """il faut utiliser l objet de classe partage cnx pour
            pouvoir partager et modifier son etat"""
            cur = cls.cnx.cursor()
            cur.execute(req)
        #item 297
        
        cls.de = getFichierTemporaire()
        data = ["1,2,3 1 2016 P1","1 2 2016 P2"]
        for l in data:
            writeFichierTemporaire(cls.de, l)
        
        cls.modele = getFichierTemporaire()
        data = ["1 1 2016 P1", "2 1 2016 P1", "3 1 2016 P1", "1 2 2016 P2"]
        for m in data:
            writeFichierTemporaire(cls.modele, m)
        
        cls.vers = getFichierTemporaire()


    def tearDownClass(cls):
        #item 111
        """supprimer les bases ouvertes en memoire...
        en refermant la connexion"""
        """ il faut utiliser un objet partage de classe cnx pour
        pouvoir le modifier sur site"""
        
        cls.cnx.close()
        #item 295
        # raise NotImplemented


    def test_DB_schema(self):
        #item 117
        """verifie que la table est bien creee:
        elle est bien creee si son nom est bien dans la liste des tables"""
        #item 118
        cur = self.__class__.cnx.cursor()
        
        nom_table = 'planning'
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (nom_table,))
        # la req preparee avec des '?' serait plus safe. elle prend (uneseq,)
        
        table_trouvee = cur.fetchone()[0] 
        # resultat de fetchone est une seq.
        
        
        self.assertEqual(table_trouvee, nom_table)


    def test_DB_syntaxte_sql(self):
        #item 313
        # je veux vérifier la syntaxe d'un trigger
        # afin qu a la création d un poste (debut_poste, fin_poste),
        # le(s) JourTravaille(jourcalendaire) et periode_travaillee(deb, fin, jourcal)
        # soient créés à la volée.
        
        # il faut donc vérifier la syntaxe d un trigger : TODO
        
        # si poste est à cheval sur deux jours, 
        #    il faut saisir deux jourtravaille et deux periode_travaillee
        #    sinon une de chaque.
        # il faut mettre au point cette logique : TODO
        #item 314
        # il faut mettre un truc
        pass
        #item 315
        #con = sqlite3.connect(':memory:')
        #con = sqlite3.connect(':memory:')
        #con.execute("create table postes (debut_poste TEXT, fin_poste TEXT);")
        #con.execute('INSERT INTO postes(debut_poste, fin_poste) VALUES (datetime("2017-05-06 06:00:00"), datetime("2017-05-06  18:00:00")),(datetime("2017-05-07 18:00:00"), datetime("2017-05-08 06:00:00"));')
        #con.commit()
        #con.execute('select count(*) from postes;').fetchone()con.execute('create temp table DATES_UNIQUES( date_poste TEXT );')
        #con.commit()


    def test_DOMAINE_annee_valide(self):
        #item 218
        import xpld
        objet_xpld = xpld.xpld()
        #item 219
        
        self.assertEqual(objet_xpld.validate_year("aaa"),False)
        self.assertEqual(objet_xpld.validate_year("2012"),True)
        self.assertEqual(objet_xpld.validate_year("1998"),False)
        self.assertEqual(objet_xpld.validate_year("2022"),False)


    def test_DOMAINE_mois_invalide_notmonth(self):
        #item 211
        import xpld
        objet_xpld = xpld.xpld()
        #item 212
        
        
        self.assertEqual(objet_xpld.validate_month("aaa"),False)


    def test_DOMAINE_mois_invalide_oob(self):
        #item 204
        import xpld
        objet_xpld = xpld.xpld()
        #item 205
        
        
        self.assertEqual(objet_xpld.validate_month("13"),False)


    def test_DOMAINE_mois_valide(self):
        #item 197
        import xpld
        objet_xpld = xpld.xpld()
        #item 198
        self.assertEqual(objet_xpld.validate_month("1"),True)
        
        self.assertEqual(objet_xpld.validate_month("12"),True)


    def test_DOMAINE_poste_invalide_notinpostekeys(self):
        #item 172
        import xpld
        objet_xpld = xpld.xpld()
        #item 174
        ligne = "1,2,3 1 2016 P1"
        ligne_no_poste = "1,2 1 2016"
        ligne_cp = "1,2,3 1 2016 CP"
        # verif du domaine du type ligne : type jours + type mois + type annee + type poste:
        
        self.assertRaises(ValueError,objet_xpld.validate_poste,"XK")


    def test_DOMAINE_poste_valide(self):
        #item 190
        import xpld
        objet_xpld = xpld.xpld()
        #item 191
        self.assertEqual(objet_xpld.validate_poste("P1"),True)
        self.assertEqual(objet_xpld.validate_poste("P2"),True)
        self.assertEqual(objet_xpld.validate_poste("P3"),True)
        self.assertEqual(objet_xpld.validate_poste("P4"),True)
        self.assertEqual(objet_xpld.validate_poste("P5"),True)
        self.assertEqual(objet_xpld.validate_poste("P6"),True)
        self.assertEqual(objet_xpld.validate_poste("P7"),True)
        self.assertEqual(objet_xpld.validate_poste("R1"),True)
        self.assertEqual(objet_xpld.validate_poste("RCP"),True)
        self.assertEqual(objet_xpld.validate_poste("AM"),True)


    def test_DOMAINE_valider_ligne(self):
        #item 225
        import xpld
        objet_xpld = xpld.xpld()
        #item 226
        ligne = "1,2,3 1 2016 P1"
        ligne_no_poste = "1,2 1 2016"
        ligne_cp = "1,2,3 1 2016 CP"
        ligne_valide_un_seul_jour_pour_ce_poste = "1 2 2016 P1"
        # verif du domaine du type ligne : type jours + type mois + type annee + type poste:
                
        self.assertEqual(objet_xpld.valider_ligne(ligne), True)
        self.assertEqual(objet_xpld.valider_ligne(ligne_cp), True)
        self.assertEqual(objet_xpld.valider_ligne(ligne_no_poste), False)
        self.assertEqual(objet_xpld.valider_ligne(ligne_valide_un_seul_jour_pour_ce_poste), True)


    def test_EXTRACT_get_divers(self):
        #item 232
        
        ligne = "1,2,3 1 2016 P1"
        #item 234
        import xpld
        objet_xpld = xpld.xpld()
        #item 233
        
        # verif des differentes extractions jours, mois, annee, poste
        self.assertEqual(objet_xpld.split_virg("1,2,3"),[1,2,3])
        self.assertEqual(objet_xpld.get_days(ligne),"1,2,3")
        self.assertEqual(objet_xpld._get_split_or_die(ligne,'jours'),"1,2,3")
        self.assertEqual(objet_xpld.get_month(ligne),1)
        self.assertEqual(objet_xpld.get_year(ligne),2016)
        self.assertEqual(objet_xpld.get_poste(ligne),"P1")


    def test_EXTRACT_get_poste(self):
        #item 163
        import xpld
        ligne = "1,2,3 1 2016 P1"
        poste_voulu = "P1"
        poste_obtenu = xpld.xpld().get_poste(ligne)
        self.assertEqual(poste_voulu,poste_obtenu)


    def test_EXTRACT_xplode(self):
        #item 242
        import xpld
        objet_xpld = xpld.xpld()
        #item 240
        
        ligne = "1,2,3 1 2016 P1"
        #item 241
        
        
        
        # verif utilitaire reel version en une fois
        self.assertEqual(objet_xpld.xplode(ligne),[{'day': 1, 'month':1, 'year':2016, 'poste' : 'P1'},
        {'day': 2, 'month':1, 'year':2016, 'poste': 'P1'},{'day': 3, 'month':1, 'year':2016, 'poste' : 'P1'}])
        # verif utilitaire reel version iterateur
        ite = objet_xpld.xplode_ite(ligne)
        for i in [1,2,3]:
            self.assertEqual(next(ite), {'day':i, 'month' : 1, 'year': 2016, 'poste': 'P1'})


    def test_IO_file_operations_filefound_littlefile_xplode(self):
        #item 270
        import xpld
        objet_xpld = xpld.xpld()
        #item 271
        #main : argparse et verifs sur boucle principale
        #verif exception si ouverture de fichier pas present
        import fileDoesNotExist
        def file_noo():
            objet_xpld.file_operations(objet_xpld.xplode, self.__class__.de, self.__class__.vers)
        
        bool2FichiersOntMemeContenu = self.assertSameFileContent(self.__class__.vers, self.__class__.modele)
        
        self.assertEqual(True, bool2FichiersOntMemeContenu)


    def test_NAMESPACE_moduleparse_fileparse(self):
        #item 259
        import xpld
        objet_xpld = xpld.xpld()
        #item 262
        import argparse
        #item 263
        import module_parse_xpld
        #item 261
        
        
        # le fichier 
        # comme param de argparse
        parsed2 = argparse.Namespace()
        parsed2.gui = False
        parsed2.file = True
        parsed2.filer = "2016.bak"
        parsed2.filew = "2016.ras"
        #parsed2.jours = None
        #parsed2.mois = None
        #parsed2.annee = None
        #parsed2.poste = None
        parse_jours2 = parsed2
        #parse_module_jours2 = module_parse_xpld.parse(['-f',"2016.bak"])
        parse_module_jours2 = module_parse_xpld.parse(['file',"-r","2016.bak", "-w", "2016.ras"])
        self.assertEqual(parse_jours2, parse_module_jours2)


    def test_NAMESPACE_moduleparse_subligne(self):
        #item 180
        import xpld
        objet_xpld = xpld.xpld()
        #item 184
        
        
        
        import argparse
        parsed = argparse.Namespace()
        
        
        parsed.file = False
        parsed.jours = "1,2,3"
        parsed.mois = "1"
        parsed.annee = "2016"
        parsed.poste = "P1"
        parsed.gui   = False
        
        #test de module_parse_xpld
        import module_parse_xpld
        parse_jours = parsed
        parse_module_jours = module_parse_xpld.parse(['ligne','1,2,3','1','2016','P1'])
        self.assertEqual(parse_jours, parse_module_jours)


    def test_SYNTAXE_lambda(self):
        #item 157
        import functools
        somme = functools.reduce (lambda x, y: x + y, [1,1,1,1,1])
        self.assertEqual(somme,5)


    def test_SYNTAXE_re(self):
        #item 137
        import re
        #item 139
        ligne = "1,2,3,12,22,30 1 2016 P1"
        #item 138
        pat = re.compile(r"""(^(\d+,*)+) (\d{1,2}) (\d{4,4}) (\w{2,2})""")
        #item 140
        match = re.search(pat, ligne)
        #item 141
        if match:
            jours = match.group(1)
            mois = match.group(3)
            annee = match.group(4)
            poste = match.group(5)
            self.assertEqual(jours, "1,2,3,12,22,30")
            self.assertEqual(mois,"1")
            self.assertEqual(annee, "2016")
            self.assertEqual(poste, "P1")
        else:
            self.assertFalse()


    def test_SYNTAXE_re_nommee(self):
        #item 147
        import re
        #item 149
        ligne = "1,2,3,12,22,30 1 2016 P1"
        #item 148
        pat = re.compile(r"""
        (?P<jours>^(\d+,*)+)\s
        (?P<mois>\d{1,2})\s
        (?P<annee>\d{4,4})\s
        (?P<poste>\w{2,2})
        """,re.VERBOSE)
        #item 150
        match = re.search(pat, ligne)
        #item 151
        if match:
            jours = match.group('jours')
            mois = match.group('mois')
            annee = match.group('annee')
            poste = match.group('poste')
            self.assertEqual(jours, "1,2,3,12,22,30")
            self.assertEqual(mois,"1")
            self.assertEqual(annee, "2016")
            self.assertEqual(poste, "P1")
        else:
            self.assertFalse()

    setUpClass = classmethod(setUpClass)
    tearDownClass = classmethod(tearDownClass)
