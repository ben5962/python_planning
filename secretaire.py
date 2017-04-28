class Secretaire(object):

    def __init__(self):
        self.types_rapports = ["cumul39heures"]

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

    def creer_fichier_odf(self,nom_fichier):
        from odf.opendocument import OpenDocumentText
        self.setNomFichierODF(nom_fichier)
        textdoc = OpenDocumentText()
        self.setHandleFichierODF(textdoc)
        return textdoc
    

    def ajouterAuRapport(self, annee):
        if self.getType() == "cumul39heures":
            s = self.getHandleFichierODF().styles
            from odf.text import H, P, Span
            """ avec secretary: """
            >>> import secretary
            >>> from secretary import Renderer
            >>> engine = Renderer()
            >>> result = engine.render('template.odt', valeur_injectee = "bah tu l attendais pas ceelle la!")
            >>> output = open('document_rendu.odt','wb')
            >>> output.write(result)
            

    def creerRapport(self):
        document = creer_fichier_odf(nom_fichier="{}{}.odf".format(self.getAnnee(),self.getMois()))
        
                          
            
            
