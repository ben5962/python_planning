# -*- coding: utf-8 -*-
from odf.opendocument import OpenDocumentText
from odf.table import Table, TableColumn, TableRow, TableCell, CoveredTableCell
from odf.text import P

class Rapport(object):
    def __init__(self,destination):
        self.setDocument()
        self.setDestination(destination)

    

    def setDestination(self,destination):
        self.destination = destination + ".odt"

    def getDestination(self):
        return self.destination

    def setDocument(self):
        self.document = OpenDocumentText()


    def getDocument(self):
        return self.document

    def _creerNColTableau(self,nb):
        return TableColumn(numbercolumnsrepeated=nb)

    def creerTableau(self,nb_colonnes):
        t = Table()
        self.ajouterFilsA(t,self._creerNColTableau(nb_colonnes))
        self.nb_colonnes = nb_colonnes
        return t

    def tbl(self,nbcol):
        tt = self.creerTableau(nbcol)
        self.ajouterFilsA(
            pere=self.getDocument().text,
            fils=tt)
        return tt

    def ligne(self, *args, **kwargs):
        # choix entre les deux versions
        # ligne v1 avec param tableau
        # rattache au tableau et renvoie l
        # ligne v2 sans param tableau renvoie l seulement
        v = kwargs.get('version', "ligneV1")
        if v == "ligneV1":
            tableau = args[0]
            l = self.ligneV1(tableau)
            return l
        if v == "ligneV2":
            l = self.ligneV2()
            return l

    def ligneV1(self, tableau):
        """cree o ligne et le rattache au tabl passé en param
        renvoie la ligne pour affectation de var car besoin de l o
        l plus tard (rattachement des cellules)"""
        l = self.creerLigne()
        # essai de rattachement de l à tabl dans la foulée
        # peut etre l est il copié dans tableau 
        # -> ajout de cell à postériori ne modifiera pas l injecté ds t
        # peut etre est il copié ds tabl à chaque modif
        # peut etre les val st partagées (x)
        # -> chd nv ajout avec mm val var devrait écraser contexte.
        # essayons
        # val partagees et fonctionne qd meme (x) soit.
        # faudra voir un jour comment c est ecrit
        self.ajouterFilsA(pere=tableau, fils=l)
        return l

    def ligneV2(self):
        """ ne cree que la ligne"""
        l = self.creerLigne()
        return l
        

    def cell(self, texte, ligne, **kwargs):
        """creer Cellule en plus court
        rattache directement à la ligne la cellule après créa
        pas besoin de renvoyer l o cellule apres crea
        """
        c = self.creerCellule(texte, **kwargs)
        self.ajouterFilsA(pere=ligne, fils=c)

    def tranche(self, ligne, liste=None):
        if liste is None:
            i = 1
            while i < self.nb_colonnes:
                self.cell("", ligne)
        else:
            for elem in liste:
                self.cell(elem, ligne)

    def finligne(self,ligne,tableau):
        """rattache la ligne au tableau parce que je ne crois pas
        que le rattachement direct au tableau fonctionne"""
        self.ajouerFilsA(pere=tableau, fils=ligne)
        

    def creerLigne(self):
        return TableRow()

    def creerCellule(self,donnee, **kwargs):
        tc = TableCell(valuetype="string")
        nbCellulesRecouvertes = kwargs.get('numbercolumnsspanned', None)
        if nbCellulesRecouvertes:
            tc = TableCell(valuetype="string", numbercolumnsspanned=int(nbCellulesRecouvertes))
        tc.addElement(P(text=str(donnee)))
        return tc

    def creerCelluleRecouverte(self):
        """une cellule fusionnee hz de 3
        c'est :
        - 1 cellule normale
        - 2 cellules recouvertes
        la cellule recouverte c'est une covered..."""
        return CoveredTableCell()

    def texteLibre(self,texte):
        """ajouter un P libre"""
        self.ajouterFilsA(pere=self.getDocument().text,fils=P(text=texte))

    def ajouterFilsA(self,pere,fils):
        pere.addElement(fils)

    def sauverDocument(self):
        self.getDocument().save(self.getDestination())

    

    
        
        
