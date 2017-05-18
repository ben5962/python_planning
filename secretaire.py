#-*-coding:utf8;-*-
import odfpy_wrapper
import calendar
import locale
import sys

from metier import moisCalendaire


class Secretaire(object):
    """mode emploi:
        - s = Secretaire(2010)
        - s.EcrireRapports['39heures'] """



    def __init__(self, annee, listeTaches=None, bdd=None):
        self.setTypeRapport()
        self.setAnnee(annee)
        self.setBdd(bdd)
        self.getBdd().remplirBase()
        #self.setNomTemplate()
        self.setNomFichierDestination()
        self.setRapport()
        #self.setListeTaches()
        #self.setVariableEnglobante(variableEnglobante)

    def setBdd(self,bdd):
        if bdd is not None:
            self.bdd = bdd
        else:
            from db import bdd
            self.bdd = bdd()

    def getBdd(self):
        if hasattr(self,'bdd'):
            return self.bdd
        else:
            self.setBdd()
            return self.bdd        

    

    def setListeTaches():
        """prend un l ite si fourni, sinon fournit un ite sur une liste de
        taches internes"""
        if listeTaches is None:
            self.listeTaches = getBdd().getListeTaches()

    def setRapport(self):
        """met un objet rapport odf dansl e contexte commun
        - parce  que plus pratique à manipuler"""
        self.Rapport = odfpy_wrapper.Rapport(self.getNomFichierDestination())

    def getRapport(self):
        return self.Rapport

    def r(self):
        return self.getRapport()
        

    def setVariableEnglobante(self, variableEnglobante):
        """ l objet qui contiendra l acces à toutes les méthodes
        nécessaires pour remplir le template"""
        self.variableEnglobante = variableEnglobante

    def setTypeRapport(self,type_rapport):
        self.type_rapport = type_rapport

    def setAnnee(self, annee):
        self.annee = annee

    def getAnnee(self):
        return self.annee

    


    def setTypeRapport(self):
        """pour l instant en dur """
        self.TypeRapport = "39heures"

    def getTypeRapport(self):
        return self.TypeRapport

    def setNomFichierTemplate(self):
        self.nom_template = "template" + self.getTypeRapport() + ".odt"

    def getNomTemplate(self):
        return self.nom_template

    def setNomFichierDestination(self):
        self.nom_destination = str(self.getAnnee()) + "_" + self.getTypeRapport() + ".odt"

    def getNomFichierDestination(self):
        return self.nom_destination

    def EcrireRapports(self,listeRapports):
        for type_rapport in listeRapports:
            if type_rapport == "39heures":
                self.RemplirRapportComplet39heures()
        self.r().sauverDocument()
            

    def RemplirRapportComplet39heures(self):
        #titre 39h

        self.r().texteLibre(" ")
        self.r().texteLibre(" ")
        t = self.r().tbl(1)
        l = self.r().ligne(t)
        self.r().cell("DEMANDE DE RAPPEL SUR HEURES SUPPLEMENTAIRES",l)
        # pondre chaque sous rapport mensuel
        for mois in self.getBdd().iterMonthNumber():
            self.RemplirRapport39heuresMensuel(mois,self.getAnnee())
                
        # pondre le total annuel
        self.RemplirRapport39heuresAnnuel(self.getAnnee())
        
        

    def RemplirRapport39heuresMensuel(self,mois,annee):
        """ chaque mois = un rapport année """
        self.setTitreTableauxMensuels(mois,annee)
        self.r().texteLibre(" ")
        self.r().texteLibre(" ")
        self.pres_TableauMensuelHeuresEffectuees()
        self.setEnTeteTableauMensuelheuresEffectuees()
        m = moisCalendaire(annee,mois)
        for semaine in m.iterSemainesHsup39(): #DONE : metier.moisCalendaire fournit itérateur sur semaine FAIT
            self.ligne_heures_sem_faites(semaine)
        self.ligne_cumul_heures_mens_faites()
        self.r().texteLibre(" ")
        self.phrase_resumant_heures_mens_faites()

    def ligne_heures_sem_faites(self,semaine):
        """ prend un param semaine (aaaa, num_sem)
        renvoie rien
        effet de bord : ajoute un objet tranche au contexte de rapport en cours
        (moche!)"""
        from metier import semaineCalendaire
        import locale
        import calendar
        t = self.r().tbl(6)
        l = self.r().ligne(t)
        # "W25"
        pres_sem = "W" + str(semaine[1])
        # "du lundi 1er avril 2015 au dimanche 7 avril 2016"
        # créa d o SemaineCalendaire(aaaa, num_semaine) à la volée car on en a besoin
        s = semaineCalendaire(semaine[0],semaine[1])
         #c1
        interv_sem = s.getBornesEnFrancais()
         #c2
        total_hebdo = self.getBdd().getCumulHeuresTravailleesSemaine(scal = s)
        
        self.r().tranche(l, [pres_sem,interv_sem,total_hebdo,"",""])

    def pres_TableauMensuelHeuresEffectuees(self):
        t = self.r().tbl(3)
        l = self.r().ligne(t)
        self.r().tranche(l,["","HEURES EFFECTUEES",""])

    def setEnTeteTableauMensuelheuresEffectuees(self):
        t = self.r().tbl(6)
        l = self.r().ligne(t)
        self.r().tranche(l,["num semaine","bornes","total hebdo","39-43h","43-48h",">48"])

    def ligne_cumul_heures_mens_faites(self):
        pass

    def phrase_resumant_heures_mens_faites(self):
        pass
        
                                   
        
 

    def setTitreTableauxMensuels(self,mois,annee):
        # TITRE MOIS
        t = self.r().tbl(3)
        l = self.r().ligne(t)
        if sys.platform in ['win32']:
            locale.setlocale(locale.LC_ALL,'fra')
        mois_en_francais = calendar.month_name[mois]
        ch = ''.join([
            "Demande de rappel sur heures supplémentaires rattachées au mois de",
            " ",
            mois_en_francais,
            " ",
            "de l'année",
            " ",
            str(self.getAnnee())]
                     )
        self.r().tranche(l,["",ch,""])
        
##        # ligne 1 décla intention
##        t = self.r().tbl(3)
##        l = self.r().ligne(t)
##        self.r().cell("",l)
##        self.r().cell("Demande de rappel sur heures supplémentaires rattachées au mois de",l)
##        self.r().cell("",l)
##        # ligne 2 mois     
##        l = self.r().ligne(t)
##        self.r().cell("",l)
##        if sys.platform in ['win32']:
##            locale.setlocale(locale.LC_ALL,'fra')
##        self.r().cell(calendar.month_name[mois],l)
##        self.r().cell("",l)
##        # ligne 3 "de l année"
##        l = self.r().ligne(t)
##        self.r().cell("",l)
##        self.r().cell("de l'année",l)
##        self.r().cell("",l)
##        # ligne 4 "année"        l = self.r().ligne(t)
##        self.r().cell("",l)
##        self.r().cell(str(self.getAnnee()),l)
##        self.r().cell("",l)
        # ligne 5 ligne hypothèse
        l = self.r().ligne(t)
        self.r().cell("",l)
        self.r().cell(" Dans l'hypothèse de la non validité de l'annualisation, sont considérées comme produisant des heures supplémentaires les volumes hebdomadaires supérieurs à 39 heures, absentes de la fiche de paye et non payées. ( les heures entre 35 et 39 heures sont présentes sur la fiche de paye et déjà payées). ",l)
        self.r().cell("",l)
        # ligne 6 ligne 
        l = self.r().ligne(t)
        self.r().cell("",l)
        self.r().cell("les numéros de semaines sont celles de la norme iso8601.",l)
        self.r().cell("",l)
        # ligne 7 demarche semaine
        l = self.r().ligne(t)
        self.r().cell("",l)
        self.r().cell("Les semaines sont rattachées au mois où elles s'achèvent ",l)
        self.r().cell("",l) 



    def RemplirRapport39heuresAnnuel(self,annee):
        """ chaque annee = un rapport """
        pass


        
        
        
        
        
        

    def remplir_template(self):
##        from odf.opendocument import OpenDocumentText
##        self.setNomFichierODF(nom_fichier)
##        textdoc = OpenDocumentText()
##        self.setHandleFichierODF(textdoc)
##        return textdoc
       from secretary import Renderer
       engine = Renderer()
       result = engine.renderer(self.getNomFichierTemplate(), Auditeur=self.getVariableEnglobante())
       output = open(self.getNomFichierDestination(), 'wb')
       output.write(result)
       output.close()
       
        
    


### preuve que fonctionne ok avec importation d objet:
### soit le template:
##{%for verifsMensuelles  in Audit.IterverifsMensuelles() %}
##{{ verifsMensuelles.getNomMois() }}
##{% endfor %}
## 
## il pond une liste de mois par le code suivant le squelette demandé:        
##>>> import secretary
##>>> from secretary import Renderer
##>>> engine = Renderer()
##>>> class Audit(object):
##	def __init__(self,annee):
##		self.annee = annee
##		
##	def IterverifsMensuelles(self):
##		mois = 1
##		while mois < 13:
##			yield VerifsMensuelles(mois,self.annee)
##			mois +=1
##
##			
##>>> class VerifsMensuelles(object):
##	def __init__(self,mois,annee):
##		self.mois = mois
##		self.annee = annee
##
##		
##>>> class VerifsMensuelles(object):
##	def __init__(self,mois,annee):
##		self.mois = mois
##		self.annee = annee
##
##	
##>>> class VerifsMensuelles(object):
##	def __init__(self,mois,annee):
##		self.mois = mois
##		self.annee = annee
##	def getNomMois(self):
##		import calendar
##		return calendar.month_name[self.mois]
##
##	
##>>> result = engine.renderer('template_essaibouclefor_iterateur.odt', Audit=Audit(2016))
##Traceback (most recent call last):
##  File "<pyshell#25>", line 1, in <module>
##    result = engine.renderer('template_essaibouclefor_iterateur.odt', Audit=Audit(2016))
##AttributeError: 'Renderer' object has no attribute 'renderer'
##>>> result = engine.render('template_essaibouclefor_iterateur.odt', Audit=Audit(2016))
##>>> output = open('document_rendu.odt','wb')
##>>> output.write(result)
##9883
##>>> output.close()
             
        
                          
            
            
