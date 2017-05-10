class Secretaire(object):

    def __init__(self, objetRapport):
        self.type_rapport = objetRapport.getType()

    def setTypeRapport(self,type_rapport):
        self.type_rapport = type_rapport

    def setAnnee(self, annee):
        self.annee = annee

    def getAnnee(self):
        return self.annee

    def getTypeRapport(self):
        
        return self.typeRapport()

    def setNomFichierODF(self,nom_fichier):
        self.nom_fichier_odf = nom_fichier

    def setHandleFichierODF(self, handle):
        self.handle_fichier_odf = handle

    def getHandleFichierODF(self):
        return self.handle_fichier_odf

    def creer_fichier_odf(self,nom_fichier_destination="rapport_{}_{}_{}.odf".format(self.getTypeRapport(),self.getAnnee(),self.getMois()),objet_racine,nom_template):
##        from odf.opendocument import OpenDocumentText
##        self.setNomFichierODF(nom_fichier)
##        textdoc = OpenDocumentText()
##        self.setHandleFichierODF(textdoc)
##        return textdoc
       from secretary import Renderer
       engine = Renderer()
       result = engine.renderer(nom_template)
       output = open(nom_fichier_destination, 'wb')
       output.write(result)
       output.close()
       
        
    

    def ajouterAuRapport(self, annee):
        if self.getType() == "cumul39heures":
##            s = self.getHandleFichierODF().styles
##            from odf.text import H, P, Span
            """ avec secretary: """

##            >>> result = self.getEngine().render('template.odt', valeur_injectee = "bah tu l attendais pas ceelle la!")
##            >>> output = open('document_rendu.odt','wb')
##            >>> output.write(result)
            pass
            
    def setEngine(self):
        import secretary
        from secretary import Renderer
        engine = Renderer()
        self.engine = engine

    def getEngine(self):
        return self.engine

    def creerRapport(self,iterateur):
        document = self.creer_fichier_odf(objet_racine = iterateur)
        self.setEngine()

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
             
        
                          
            
            
