import functools
#from metier import moisCalendaire
import utilitaireDates
class bdd(object):
    def iterAnneesDispo(self):
        for a in [2013,2014, 2015, 2016]:
            yield a


def getCumulHeuresTravailleesSemaine(a,s):
    return 44

def gen_heures_sup_semaines(aaaa, num_sem):
    c = getCumulHeuresTravailleesSemaine(aaaa,num_sem)
    hs = [ c,
           max(0, seuil(c, 35, 43) - 4) ,
           max(0, seuil(c, 43, 48) - 0) ,
           max(0, seuil(c, 48, 1000) - 0)
            ]
    print("hsem {} de l annee {} vaut {}".format(num_sem, aaaa, hs))
    return hs


def seuil(base, mn, mx):
    if mx < mn:
        raise("max > min")
    else:
        return max(0,min(base - mn, mx - mn))


def iter_heures_sup_semaines_mois(a, m):
##    M = moisCalendaire(m,a)
##    for semaine in M.iterSemaine():
    for num_semaine in utilitaireDates.iterSemaine(a,m):
        yield gen_heures_sup_semaines(a, num_semaine)

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
    print("M {} de l annee {} vaut {} ".format(m, a, M))
    return M


def iter_heures_sup_mois(a):
    for mois in range(1,13):
        yield gen_heures_sup_mois(mois, a)



def gen_heures_sup_annee(a):
    A = functools.reduce(
    somme_terme_a_terme,
    iter_heures_sup_mois(a),
    [0,0,0,0] )
    print("A {}vaut {}".format(a, A))
    return A



def iter_heures_sup_annees():
    for a in bdd().iterAnneesDispo():
        yield gen_heures_sup_annee(a)



def total():
    T = functools.reduce(
        somme_terme_a_terme,
        iter_heures_sup_annees(),
        [0,0,0,0])
    print("grand total vaut {}".format(T))
    
