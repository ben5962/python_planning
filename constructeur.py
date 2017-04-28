class Constructeur(object):
##    def __init__(self):
##        self.allClasses = []

    def creerInstanceDepuisNom(self, objetModuleImporte, nom_constructeur, **args):
        print("module is " + objetModuleImporte)
        import importlib
        m = importlib.import_module(objetModuleImporte)
        classeDestinataire = getattr(m, nom_constructeur)#  TODO ajouter la maniere d ajouter le parametre au constructeur
        #ref : "python create class instance from class name"
        instance = classeDestinataire(**args)
        return instance

