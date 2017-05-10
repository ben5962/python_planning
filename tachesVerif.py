def getNomTaches():
    import tachesVerif
    return [str(x) for x in dir(tachesVerif) if "tache" in repr(x)]


class PrincipeEtapeVerificationMensuelle (object):
    """une regle doit
        - ajouter tache de verif a 
        un rapprt de verif
         fiche de p d un 
        mois donne ou d une liste de mois
        sous con 
        - fournit fiche paye reelle du mois sous l angle de la verf
        - foirnir la fiche de paye caclculee sous l angle de la verif
        - conclure sur la presence ou non d erreur
        - qtifier en unites heures (categ diff selon categ bonif diff selon categ )
        l erreur
        - deleguer le chiffrage de l err et l afficher
        - envoyer le chiffrage vers un sommateur de fin de rapport
        """
    def setAnnee(self,annee):
        self.annee = annee

    def setMois(self,mois):
        self.mois = mois
        



        
    def getSpecifiqueFpaieReelle (self):
        """accesseur dans la fiche de paye reelle du bon mois de la bonne annee
au champ interessant l etape de verif.
ce champ peut varier d une etape à l autre.
donc accesseur implémenté spécifiquement dans chaque etape de verif
ainsi:
 - le champ est déjà présent dans la fiche de paye réelle
 - il n y a plus qu à accéder à ce champ
"""
        pass
            
    def setSpecifiqueFpaieCalc (self):
        """ce champ est calcule a partir du planning (pbblement)
comme le mode de calcul """
        
        pass
        
    def getSpecifiqueFpaieCalc (self):
        self.setSpecifiqueFpaieCalc ()
        pass

    def getNomChampCalcule(self):
        """ renvoie le nom du champ calcule"""

    def setRapport(self):
        """ cense renvoyer un iterable de lignes, disons une liste
indiquant:
le nom du champ calcule, la valeur calculee (obtenue theoriquement)
la valeur reelle
la difference, le fait que l employeur doit de l argent au salarie ou non
"""
        rapport_etape.append(''.join(["étape de ", self.getNomChampCalcule()]))
        du = self.getSpecifiqueFpaieCalc()
        paye = self.getSpecifiqueFpaieRelle()
        manque_a_payer = du - paye
        
        if du > paye:
            rapport_etape.append("heures du : " + du)
            rapport_etape.append("heures payees: " + paye)
            rapport_etape.append("manque à payer: " + manque_a_payer)
        else:
            rapport_etape.append("ok heures dues : " + du)
            rapport_etape.append("ok heures payees: " + paye)
            
            
class EtapeVerificationHeureSupplementaireMensuelle(PrincipeEtapeVerificationMensuelle):
    """ les verifications d heures supplematairess ont des etapes spécifiques de cacul:
        - les postes de planning à prendre en compte débordent du mois:
          * en effet pour le décompte des heures sup39 il faut prendre les semaines qui se terminent
          dans le mois pris en consideration. donc commencer AVANT le début du mois.
            * il faut ensuite trancher les mois en semaines terminées et les comparer au seuil légal
            pour la semaine. il faut ensuite classer les heures dépassant le seuil en catégories dans
            un tableau (de 39 à 43 = 25%, de 43 à 48 = 50%,  plus de 48 = interdit)
          * de meme les postes de planning à prendre en compte pour l annualisation 
          débutent effectivement le 1er janvier à 0h et se terminent effectivement le 31 déc à minuit,
          ou du premier jour 0h du mois choisi au premier jour 0h du mois choisi année suivante,
          mais ce calcul n est pas à faire tous les mois mais seulement sur la derniere fiche de paye
          de la période considérée.
        - en commun : * un seuil sur une période considérée
                      * une liste d'une ou plusieurs sous-périodes à considérer
                      * les postes sur les bords de la période sont à retailler.
        
                 
"""
    def setAnnee(self,annee):
        PrincipeEtapeVerificationMensuelle.setAnnee(self,annee)

    def setMois(self,mois):
        PrincipeEtapeVerificationMensuelle.setMois(self,mois)

         
class tacheVerificationHeuresSupplementairesAnnualisation  (EtapeVerificationHeureSupplementaireMensuelle):
    """tache de verification annu mensuelle"""
    def __init__(self):
        super (EtapeVerificationHeuresSupplementairesAnnualisation,self).__init__(year,month)

    def isMoisVerifAnnualisation(self):
        if isLastMois(periode_annualisation):
            rapport_etape.append("c est le mois de cumul de l annualisation")
        else :
            rapport_etape.append("ca n est pas le mois de cumul de l annualisation")

    
    
    
class Seuil(object):
    """definit les seuils.
renvoit des tranches d heures dans ces seuils
contre [35], 29 doit renvoyer [29,0]
contre [35], 36 doit renvoyer [35,1]
contre [35,43], 40 doit renvoyer [35,5,0]
contre [35,43,48] 47 doit renvoyer [35,8,4]
contre [35,43,48] 49 doit renvoyer [35,8,5,1] et traiter le fait que interdit"""
    
    def __init__(self, *args):
        self.args = args
        self.tranches = []

    def getTranches(self, nbheures):
        """un ecart entre chaque poteau = 1 de plus que le nb de poteaux"""
        TOUS_DEPASSES = 1000
        nb_poteaux = len(self.args)
        nb_tranches = nb_poteaux + 1
        """ initialisation de tranches"""
        self.tranches  = [ 0 for x in range(nb_tranches) ]
        """trouver la position dans args du plus petit poteau supérieur à nbheures"""
        try:
            plus_petit_majorant = min([pos for pos, valeur in enumerate(self.args) if valeur >= nbheures])
        except ValueError:
            print("nbheures depasse tous les seuils. interdit legalement.")
            plus_petit_majorant = TOUS_DEPASSES
        finally:
            for seuil in self.args:
                if nbheures <= seuil:
                    self.tranches.append(nbheures)
                else:
                    self.tranches.append(seuil)
                    nbheures = nbheures - seuil

            
    
class tacheVerificationHs39Mensuelle (PrincipeEtapeVerificationMensuelle):
    """tache de verfication hs mensuelle"""
    def __init__(self, annee, mois):
        self.annee = annee
        self.mois = mois

    def doit(self):
        accumulateur_semaines_mois = { 'heures_totales_semaine' : 0,
                                       'heures_de35a39' : 0,
                                       'heures_de_39_a_43' : 0,
                                       'heures_de43_a_48': 0,
                                       'heures_superieures_a_48_interdites' : 0}
        for bornes_semaine_debut, borne_semaine_fin in getBornesSemainesMoisComptable(self.getAnnee(),self.getMois()):
            seuil = Seuil(39,43,48)
            listeJourneesTravailles = bdd.getJourneesTravailles(debut=borne_semaine_debut, fin=borne_semaine_fin)
            for liste in pouet:
                # mis ca pour l err de syntaxe de pytddmon
                pass


class VerifierFichePaye(object):
    def __init__(self, mois=1, annee=2002, etapes=None):
        setMois()
        setAnnee()
        setEtapes()

    def setMois(self,mois):
        self.mois = mois

    def setAnnee(self,annee):
        self.annee = annee

    def setEtapes(self,etapes):
        """il FAUT construire une nouvelle liste"""
        if etapes is not None:
            self.etapes = list(etapes)
        else:
            self.etapes = []

    def getEtapes(self):
        return self.etapes

    def doit(self):
        for etape in self.getEtapes():
            import constructeur
            cons = constructeur.Constructeur()
            cons.creerInstanceDepuisNom("tachesVerif",etape,annee=self.getAnnee(), mois=self.getMois()).doit()

            
class Fpaie (object):
    """resp repr fpaie réelles et calculées
    pour un mois donne et une
    annee donnee.
    """
    def __init__(self, mois=1, annee=2002, hsup25=0, hsup50=0, hdim10=0, hjf100=0, hnuit10=0):
        self.mois = mois
        self.annee = annee
        self.hsup25 = hsup25
        self.hsup50 = hsup50
        self.hdim10 = hdim10
        self.hnuit10 = hnuit10
        self.hjf100 = hjf100

    def getMois(self):
        return self.mois




class Fpaiereelle(Fpaie):
    """c est une fpaie, mais dont les calculs
    annu, hsup25 etc etc sont bases sur le planning,
    pas sur la saisie de fiches de paie
    il prend en plus une valeur booleenne annualisation
    et une valeur booleenne mois_de_decompte_annualisation"""
    def __init__(self,  mois=1, annee=2002, hsup25=0, hsup50=0, hdim10=0, hjf100=0, hnuit10=0):
        print("Initialisation de l'étudiant {0}".format(id(self)))
        super(Fpaie, self).__init__(self, mois=1, annee=2002, hsup25=0, hsup50=0, hdim10=0, hjf100=0, hnuit10=0)
        
        
