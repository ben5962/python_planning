# coding: utf-8
import unittest
import sqlite3
#import module_repertoire
#import os

# Autogenerated with DRAKON Editor 1.27

def nline2_1line(chaine):
    #item 124
    return  chaine.replace('\n',' ')

class testbdd(unittest.TestCase):



    def setUp(self):
        #item 110
        """AVANT TOUS LES TESTS 
        env test:
        une bdd en mémoire"""
        #item 54
        #cnx = sqlite3.connect(':memory:')
        with open('schema.sql','r') as f:
        	req = f.read()
                req = nline2_1line(req)
        	cur = cnx.cursor()
                cur.execute(req)


    def tearDown(self):
        #item 111
        """supprimer les bases ouvertes en memoire...
        en refermant la connexion"""
        
        cnx.close()


    def test_schema(self):
        #item 117
        """verifie que la table est bien creee:
        elle est bien creee si son nom est bien dans la liste des tables"""
        #item 118
        cur = cnx.cursor()
        nom_table = 'planning'
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (nom_table,))
        # la req preparee avec des '?' serait plus safe. elle prend (uneseq,)
        
        table_trouvee = cur.fetchone()[0] 
        # resultat de fetchone est une seq.
        
        
        self.assertEqual(table_trouvee, nom_table)

cnx = sqlite3.connect(':memory:')
