import functools
#from metier import moisCalendaire
import utilitaireDates
import db
import devpy.develop as log
log.setLevel('INFO')
"""les cp:
acquisition : sauf accord d'aménagement (pas le cas)
ou dispo conv contraires, la période d'acqui des cp va du  1er juin au
31 mai.


principe: non cumul avec la rémun de travail.
or pb se pose ici. travail ET  cp : cp commence à minuit
sinon ce serait fin de poste 6h début de poste "cp" 7h

2,5j cp par mois => 30j par ans en heures 

calcul:
le plus favorable entre :
- somme(brut(1/5 -> 31/6)) x 1/10
- méthode de maintien du salaire: impossible puisque doit conn
  * rémun brute période de réf préc le cp (mois préc?)
  * horaire de trv incluant hs pendant période de congés

- pose de congés:
  par bloc d'une semaine et une semaine uniquement


  problèmes:
  - lors du calcul en jour ouvrables, la pose d'un jour de congés
  n amène qu'un jour de repos
  tandis que la pose de 5 jours amène une semaine de repos
  (on compte du lundi au vendredi)
  pour les jours ouvrés on compte une semaine de 6 jours.
  (du lundi au samedi)
  JAMAIS on ne compte de semaine de 7 jours. pourquoi?

  proposer décompter 35 jours de congés par an et poser 1 jour par semaine

  
"""
    
"""les cas limites:
- lorsqu un poste set termine alors qu il y a une semaine de vacances
la semaine de vacacnes est censée se substituer à 39 h de travail.
ainsi les heures de poste en plus sont censeés constituer des heures sup
il faut donc comprendre les heures de congés avec les heures travaillées
pour rattraper cette erreur
il faut notifier cette erreur
sinon (si le poste n'était pas à cheval entre jour et nuit,
il  y aurait heures sup.
il y a bien dol puisque meme si le repos s'étend au delà de la période de cp,
le repos n 'est pas payé.
ex  : s48 puis une semaine de congés puis démarrage le mardi = 35 + 8hs25 + 5hs50
vs s42 puis 6h grignottant semaine de congés puis démarrage mardi
cette notion de repos n a pas d importance pour les gens travaillant tjs
memes horaires mais est fondamentale pour le personnel dont les heures de
travaillent oscillent entre le jour et la nuit d une semaine à une autre.

le cas ne se présente jamais pour les personnent travaillant la journée, donc
personne ne réfléchit au sens de ca. 
"""


def getCumulHeuresTravailleesSemaine(a,s,methode=db.bdd().getCumulHeuresTravailleesSemaine):
    try:
        return int( methode(a,s))
    except TypeError:
        return int(methode)

def gen_heures_sup_semaines(aaaa, num_sem, hsup25payees=0, hsup50payees=0):
    c = getCumulHeuresTravailleesSemaine(aaaa,num_sem)
    hs = [ c,
           max(0, seuil(c, 35, 43) - hsup25payees) ,
           max(0, seuil(c, 43, 48) - hsup50payees) ,
           max(0, seuil(c, 48, 1000) - 0)
            ]
    log.debug("hsem {} de l annee {} vaut {}".format(num_sem, aaaa, hs))
    return hs





def heures_sup_restant_dues(heures):
    """hsrd = hss_effectuee - hsspayee.
       les heures négatives ?   c est le point le plus important:
       trois positions possibles:
         1) les heures sont perdues pour l employeur et le décompte se fait à la semaine, paiement au mois
         2) les heures ne sont pas perdues pour l employeur et le cumul se fait algébriquement sur le mois
         3) les heures ne sont pas perdues pour l employeur et le cumul se fait algébriquement sur l'année.
         4) il n'y a jamais de perte pour l'employeur et le compteur n est jamais perdu pour l employeur.
         je penche pour le type 3 pour l instant:
         il s'agit d une CORRECTION DU PAIEMENT REEL PAR RAPPORT A UN PAIEMENT DU
         pour qualifier un DOL
         PAR CONTRE QUEL QUE SOIT LE RESULTAT, LE COMPTEUR DE DIFF25
         EST REMIS A ZERO au 1er janvier

         des exceptions sont à prendre en compte:
         pendant certaines semaines de congés payées, on travaille.
         on est à la fois en congés et au travail.
         cela se résoud en considérant cela comme des heures supplémentaires:
         en effet, les cp sont censées se substituer à des jours de travail
         mais ils sont payés comme des jours de travail (les heures à poser
         pour un jour de cp correspond à la moyenne des heures d une semaine
         de travail normal)
       """
    """ALGO:    pour chaque semaine du mois:
        probleme | semaine à exclure | semaine à inclure
        si semaine_travaillée et semaine_cp => probleme 
        si non semaine travaillee et semeaince cp => semaine a exclure
        sinon semaine  à inclure
        pour chaque semaine à inclure du mois:
            pour chaque type_d heures sup:
                heure_sup_dues vs heures_sup_payees.
                si heures sup_dues:
                    ajouter (typeheures_sup : + heures_sup_dues)
                si heures_en_trop:
                    ajouter(typeheures_sup: cagnotte globale)
    fin_du_mois :
        pour chaque type_heures_sup:
            pour chaque_semaine:
                ajouter_type_heures_sup
            ajouter_cagnotte
            vider_cagnotte
            si_heures_sup:
                ajouter_heures_sup
        renvoyer tableau_heures_sup_mensuelles"""


def heures_sup_25_effectuees(heures):
    return max(0,seuil(heures, 35, 43))

def heures_sup_50_effectuees(heures):
    return max(0,seuil(heures, 43, 48))

def heures_illegales_effectuees(heures):
    return max(0,seuil(heures, 48, 1000))

def heures_effectuees_semaine(heures):
    """mode emploi: heures_effectuees(getCumulHeuresTravailleesSemaine(a,s))
       renvoie: [heures, heures25, heures50, heures_ille]"""
    return [heures, heures_sup_25_effectuees(heures), heures_sup_50_effectuees(heures), heures_illegales_effectuees(heures)]

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


def iter_heures_sup_annees_param(iter_annees=db.bdd().iterAnneesDispo,
                                 generateur_heures_sup_annees = gen_heures_sup_annee_a
                                 ):
    BOOL_ITER_ANNEES_DOMAINE_OK = (iter_annees in [ db.bdd().iterAnneesDispo ])
    BOOL_GENE_HEURES_SUP_ANNEES_DOMAINE_OK = ( generateur_heures_sup_annees in
                                               [gen_heures_sup_annee_a,
                                                gen_heures_sup_annee2,
                                                gen_heures_sup_annee]
                                               )
    if not BOOL_ITER_ANNEES_DOMAINE_OK:
        raise("iter annees pas dans bon domaine")
    if not BOOL_GENE_HEURES_SUP_ANNEES_DOMAINE_OK:
        raise("gene heures sup domaine pas ok")
    
    
    for a in iter_annees:
        annee = int(a)
        yield gen_heures_sup_annees(a)



    


    



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
    

def total3():
    
    TI = ['TOTAL ANNEES']
    E = ['a', 'tot', '>35', '>43', '>48']
    L = list(iter_heures_sup_annees_a())

    T = functools.reduce(
        somme_terme_a_terme,
        iter_heures_sup_annees2(),
        [0,0,0,0])
    T = ['TOTAL'] + T
    log.info(" ")
    log.info("si l on arrete le décompte chaque mois, comme cela devrait etre le cas,")
    log.info("et qu on oppose ce qui devrait etre paye à ce qui a effectivement été payé,")
    log.info(" ne décomptant que ce qui mnaque mois par mois,")
    log.info("alors on arrive au décompte suivant:")
    log.info("modifier gen_semaines pour cumul au mois soit 4h par sem trav")

    """
        ANALYSE DE VARIABILITE de total2
        chaque fonction total utilise:
        2. une var TI  la liste contenant titre du tableau e
        3. une var E liste contenznt l entete du tableau
        5. une fonction  D'AFFICHAGE list
           envoyant ds une liste L
           une liste par étape du calcul de cumul des années,
           préfixés du nom de l année.

           ces listes par étape doivent etre produites ET
           préfixées à la volée.
           pour l instant je n'ai pas trouvé mieux que d écrire
           une nouvelle fonction itérant sur les années [0,0,0,0]
           afin qu'elle produise des années [annee, 0,0,0,0]
           basée sur une copie de iter_heures_sup_annees:
           iter_heures_sup_annees_a()
              -> [annee, 0,0,0,0] - pas de sous-iter
           
        
       
                A. cette fonction utilise une fcontion
                   de type iter_heures_sup_annees:
                           iter_heures_sup_annees_a qui utilise une fonction de type
                              gen_heure_sup annees, ici
                              gen_heures_sup_annees_a
                              qui:
                               - n effectue AUCUN EFFET DE BORD
                                 not. affiche PAS TI E L et A 
                               - renvoie chaque [0,0,0,0] calc de mois de l année
                                 PREFIXE DE L ANNEE (DECORE)
       1. une fonction T (cumul) calculant terme à terme les éléments d un tab4 'reduce'
                A. cette fonction utilise une fcontion
                   de type iter_heures_sup_annees:
                           iter_heures_sup_annees_2 qui utilise pour chq annee
                           une fonction de type gen_heure_sup annees, ici
                              gen_heures_sup_annees_2
                              qui :
                                 - effecue affichage de 
                                   TI E L et A pour les mois
                                   i) cet affichage fait appel à
                                      une fonction de type iter heures_sup:
                                      - iter_heures_sup_mois2
                               
                                 - renvoie [0,0,0,0] calc de mois de l année
                                    NON DECORE utilisant iter_heures_sup_mois.
        




        6. une fonction Tprime enrobant l affichange de T
        7 une fonction affichant TI, E, chaque étape de L, Tprime
        

        """



        
    
    
