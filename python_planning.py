import sqlite3
####  VARIABLES
db_name = 'planning.db'
fichier_plannings = 'plannings.txt'
postes = {'P1' : {'heure_debut' : 6, 'duree': 12 },
          'P2' : {'heure_debut' : 18, 'duree': 12}}

#########  FIN  VARIABLES

######### UTILITAIRES
def isSQLite3(filename):
    from os.path import isfile, getsize

    if not isfile(filename):
        print "pas un fichier"
        return False
    if getsize(filename) < 100: # SQLite database file header is 100 bytes
        print "taille <100"
        return False

    with open(filename, 'rb') as fd:
        header = fd.read(100)
        return header[:16] == 'SQLite format 3\x00'


def _nettoyer(chaine):
    return chaine.strip()

def _explodeline(ligne):
    """'1,2,3 4 2016 P1' -> {'jour':1, 'mois':4, 'annee':2016, 'poste':P1}' puis '{'jour':2, 'mois':4, 'annee':2016, 'poste':P1}'...
       utilisable comme for la_ligne in  explodeline(ligne):
       laligne[jour] ...."""
    jours, mois, annee, poste = ligne.split(' ')
    tableau_jours = jours.split(',')
    for jour in tableau_jours:
        print {'jour': int(jour), 'mois': int(mois), 'annee': int(annee), 'poste' : poste}
        yield {'jour': int(jour), 'mois': int(mois), 'annee': int(annee), 'poste' : poste}

def _datetimedebutposte(dic_poste):
    import datetime
    """ {'jour': int(jour), 'mois': int(mois), 'annee': int(annee), 'poste' : poste} -> datetime debut poste"""
    date_debut = datetime.date(dic_poste['annee'], dic_poste['mois'], dic_poste['jour'])
    heure_debut = datetime.time(postes[dic_poste['poste']]['heure_debut'])
    return datetime.datetime.combine(date_debut, heure_debut)

def _datetimefinposte(dic_poste):
    import datetime
    """ {'jour': int(jour), 'mois': int(mois), 'annee': int(annee), 'poste' : poste} -> datetime fin poste"""
    poste_debut = _datetimedebutposte(dic_poste)
    return poste_debut + datetime.timedelta(hours = postes[dic_poste['poste']]['duree'])
    
    


def insertdate(debut, fin, cur,debug=True,cnx=None):
    import datetime
    import sqlite3
    if debug is not True:
        cur.execute("""INSERT INTO planning(debut_poste, fin_poste) VALUES (?,?); """,( debut, fin) )
        cnx.commit()
    else:
        print("""INSERT INTO planning({d}, {f}) VALUES (?,?); """).format(d=poste_debut, f=poste_fin)

def logique_remplir_base(fichier):
    with open(fichier, 'r') as f:
        print("ouverture de :{f}").format(f=fichier)
        for ligne in f:
            print("parse de : {l}").format(l=ligne)
            for laligne in _explodeline(_nettoyer(ligne)):
                print("utilisation de {l}").format(l=laligne)
                insertdate(debut=_datetimedebutposte(laligne), fin=_datetimefinposte(laligne), cur=cursor, debug=False, cnx=db_loc)
        
    
def valider_ligne(ligne):
    """1,2,3 4 2016 P1 -> True
1,2,3, 4 2016 P1 -> False
1,2,3 4 2016 P1\n -> False
"""
    
################ FIN UTILITAIRES

#############  REQUETES
req_postesentredeuxdates = """SELECT
debut_poste as 'd [timestamp]',
fin_poste as 'f [timestamp]'
from planning WHERE  d > ?  AND f <= ?"""

##############  FIN REQUETES

def creation_db(cur,cnx):
    if cur is not None and cnx is not None:
       
        cur.execute("""CREATE TABLE planning(
          id INTEGER PRIMARY KEY,
          debut_poste DATETIME,
          fin_poste DATETIME);""")
        cnx.commit()


def read_db(cur, cnx):
    print("entree dans readdb")
    nb = cur.execute("""SELECT Count(*) FROM planning; """)
    print("il y a " + str(nb.fetchone()[0]) + " enregistrements")
    if cur is not None and cnx is not None:
        cur.execute("""
SELECT * FROM planning;
""")
        for champ in cur:
            print champ
            print "-" * 5
    else:
        print("cur is Noe or cnx is None")
       
def req_lecture(requete_prepa,params):
    """execute une requete en lecture -> curseur"""
    cursor.execute(requeteprepa,params)
    

def connecter(db_name):
    db_loc  = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    return db_loc




if isSQLite3(db_name):
    print(db_name + " existe")
    db_loc = connecter(db_name)
    print db_loc
    cursor = db_loc.cursor()
    print cursor
    try:
        read_db(cursor, db_loc)
    except sqlite3.Error as e:
        print e
else:
    print(db_name +  "n existe pas")
    db_loc = connecter(db_name)
    print db_loc
    cursor = db_loc.cursor()
    print cursor
    creation_db(cursor, db_loc)
    cursor.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='planning';""")
    print(cursor.fetchone()[0])
    #insertdate("1,2,3,4,5 4 2016 P1", cur=cursor, debug=False, cnx=db_loc)
    #insertdate("2 1 2015 P2", cur=cursor, debug=False, cnx=db_loc)
    logique_remplir_base('monplanning.txt')
    read_db(cursor, db_loc)
##    
    

















