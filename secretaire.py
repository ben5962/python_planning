#-*-coding:utf8;-*-
import odfpy_wrapper
import calendar
import locale
import sys
import db


class Secretaire(object):
    """mode emploi:
        - s = Secretaire(2010)
        - s.EcrireRapports['39heures'] """



    def __init__(self, annee):
        self.setTypeRapport()
        self.setAnnee(annee)
        #self.setNomTemplate()
        self.setNomFichierDestination()
        self.setRapport()
        #self.setVariableEnglobante(variableEnglobante)

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
        t = self.r().tbl(1)
        l = self.r().ligne(t)
        self.r().cell("DEMANDE DE RAPPEL SUR HEURES SUPPLEMENTAIRES",l)
        # pondre chaque sous rapport mensuel
        for mois in db.bdd().iterMonthNumber():
            self.RemplirRapport39heuresMensuel(mois,self.getAnnee())
                
        # pondre le total annuel
        self.RemplirRapport39heuresAnnuel(self.getAnnee())
        
        

    def RemplirRapport39heuresMensuel(self,mois,annee):
        """ chaque mois = un rapport année """
        # TITRE MOIS
        # ligne 1 décla intention
        t = self.r().tbl(3)
        l = self.r().ligne(t)
        self.r().cell("",l)
        self.r().cell("Demande de rappel sur heures supplémentaires rattachées au mois de",l)
        self.r().cell("",l)
        # ligne 2 mois     
        l = self.r().ligne(t)
        self.r().cell("",l)
        if sys.platform in ['win32']:
            locale.setlocale(locale.LC_ALL,'fra')
        self.r().cell(calendar.month_name[mois],l)
        self.r().cell("",l)
        # ligne 3 "de l année"
        l = self.r().ligne(t)
        self.r().cell("",l)
        self.r().cell("de l'année",l)
        self.r().cell("",l)
        # ligne 4 "année"
        l = self.r().ligne(t)
        self.r().cell("",l)
        self.r().cell(str(annee),l)
        self.r().cell("",l)
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
        self.r().cell("Les semaines sont rattachées au mois de ont les semaines achevées au cours de ce mois ",l)
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
             
        
                          
            
            
