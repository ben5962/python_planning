import functools
#from metier import moisCalendaire
import utilitaireDates
import db
import devpy.develop as log
log.setLevel('INFO')

    



def getCumulHeuresTravailleesSemaine(a,s):
    return int(db.bdd().getCumulHeuresTravailleesSemaine(a,s))

def gen_heures_sup_semaines(aaaa, num_sem):
    c = getCumulHeuresTravailleesSemaine(aaaa,num_sem)
    hs = [ c,
           max(0, seuil(c, 35, 43) - 0) ,
           max(0, seuil(c, 43, 48) - 0) ,
           max(0, seuil(c, 48, 1000) - 0)
            ]
    log.debug("hsem {} de l annee {} vaut {}".format(num_sem, aaaa, hs))
    return hs

def gen_heures_sup_semaines2(aaaa, num_sem):
    c = getCumulHeuresTravailleesSemaine(aaaa,num_sem)
    hs = [ c,
           max(0, seuil(c, 35, 43) - 0) ,
           max(0, seuil(c, 43, 48) - 0) ,
           max(0, seuil(c, 48, 1000) - 0)
            ]
    log.debug("hsem {} de l annee {} vaut {}".format(num_sem, aaaa, hs))
    return ['w' + str(num_sem)] + hs


def seuil(base, mn, mx):
    log.debug("lancement de seuil avec base = {}, mn = {}, mx= {}"
              .format(base, mn, mx))
    if mx < mn:
        raise("max > min")
    else:
        return max(0,min(base - mn, mx - mn))


def iter_heures_sup_semaines_mois(a, m):
##    M = moisCalendaire(m,a)
##    for semaine in M.iterSemaine():
    for num_semaine in utilitaireDates.iterSemaine(a,m):
        yield gen_heures_sup_semaines(a, num_semaine)


def iter_heures_sup_semaines_mois2(a, m):
##    M = moisCalendaire(m,a)
##    for semaine in M.iterSemaine():
    for num_semaine in utilitaireDates.iterSemaine(a,m):
        yield gen_heures_sup_semaines2(a, num_semaine)

def somme_terme_a_terme (a, b):
    c = []
    for indice in range(0,len(a)):
        c.append(a[indice] + b[indice])
    return c


def gen_heures_sup_mois(m,a):
    M = functools.reduce(
        somme_terme_a_terme,
        iter_heures_sup_semaines_mois(a,m),
         [0,0,0,0]
        )
    log.debug("M {} de l annee {} vaut {} ".format(m, a, M))
    return M

def gen_heures_sup_mois2(m,a):
    TI = ["mois de {} {}".format(m,a)]
    E  = ['s', 'tot','h>39', 'h>43', 'h>48']
    S = list(iter_heures_sup_semaines_mois2(a,m))
    M = functools.reduce(
        somme_terme_a_terme,
        iter_heures_sup_semaines_mois(a,m),
         [0,0,0,0]
        )
    #M = ["CUMUL SEM"] + M
    log.info(TI)
    log.info(E)
    for ligne in S:
        log.info(ligne)
    log.info(["CUMUL SEM"] + M)
    log.debug("M {} de l annee {} vaut {} ".format(m, a, M))
    return [str(m), M]


def iter_heures_sup_mois(a):
    for mois in range(1,13):
        yield gen_heures_sup_mois(mois, a)

def iter_heures_sup_mois2(a):
    for mois in range(1,13):
        yield gen_heures_sup_mois2(mois, a)



def gen_heures_sup_annee(a):
    A = functools.reduce(
    somme_terme_a_terme,
    iter_heures_sup_mois(a),
    [0,0,0,0] )
    log.debug("A {}vaut {}".format(a, A))
    return A

def gen_heures_sup_annee_a(a):
    A = functools.reduce(
    somme_terme_a_terme,
    iter_heures_sup_mois(a),
    [0,0,0,0] )
    log.debug("A {}vaut {}".format(a, A))
    return [a] + A

def gen_heures_sup_annee2(a):
    TI = [''.join(['ANNEE ', str(a)])]
    E = ['m', 'tot', '>35', '>43', '>48']
    L = list(iter_heures_sup_mois2(a))
    
    A = functools.reduce(
    somme_terme_a_terme,
    iter_heures_sup_mois(a),
    [0,0,0,0] )
    log.debug("A {}vaut {}".format(a, A))
    log.info(TI)
    log.info(E)
    for ligne in L:
        log.info(ligne)
    log.info(["CUMUL MOIS"] + A)
    return A



def _acces_premier_element_tuple(t):
    return t[0]

def iter_heures_sup_annees():
    for a in db.bdd().iterAnneesDispo():
        annee = int(a)
        yield gen_heures_sup_annee(a)

def iter_heures_sup_annees2():
    for a in db.bdd().iterAnneesDispo():
        annee = int(a)
        yield gen_heures_sup_annee2(a)    

def iter_heures_sup_annees_a():
    for a in db.bdd().iterAnneesDispo():
        annee = int(a)
        yield gen_heures_sup_annee_a(a)


    



def total():
    T = functools.reduce(
        somme_terme_a_terme,
        iter_heures_sup_annees(),
        [0,0,0,0])
    print("grand total vaut {}".format(T))


def total2():
    TI = ['TOTAL ANNEES']
    E = ['a', 'tot', '>35', '>43', '>48']
    L = list(iter_heures_sup_annees_a())

    T = functools.reduce(
        somme_terme_a_terme,
        iter_heures_sup_annees2(),
        [0,0,0,0])
    T = ['TOTAL'] + T
    
        
    log.info(TI)
    log.info(E)
    for ligne in L:
        log.info(ligne)
    log.info(T)
    log.info(T)
    log.info("si l on fait un décompte qui vous est favorable (le total sur 3 ans -plus la période est longue, plus les totaux se lissent-")
    log.info("le total d heures supplémentaires à 25 % s'élève à {} heures".format(T[2]))
    log.info("ce qui, comparé à 564 heures à 25% payées sur ces 3 années (47 x 4 x 3années)")
    log.info("représente encore {} hors bonification heures à 25% non payées. ".format(T[2] - 3 * 47 * 4))
    log.info("ce qui représente après bonification {} equivalent heures dûes".format((T[2] - 3 * 47 * 4) * 1.25))
    log.info("d autre part, les heures à 50% (de 43 à 48 heures ne sont jamais rémunérées")
    log.info("cela représente {} hors bonification sur 3 ans jamais rémunérées".format(T[3]))
    log.info("soit {} heures bonifiées".format(T[3] * 1.5))
    log.info("ramené en équivalent heures - bonification de 25% et 50%- cela représente {} heures dûes".format(((T[2] - 3 * 47 * 4) * 1.25) + (T[3] * 1.50)))
    log.info("enfin, sur ces 3 ans, {} heures ont été effectuées au-delà du maximum légal de 48 heures.".format(T[4]))
    log.info("comment comptez vous les rémunérer? à 100% cela ajoute encore {} heures dûes".format(T[4] * 2))

    
    
        
    
    
