# -*- coding: utf-8 -*-
import odfpy_wrapper

#
r = odfpy_wrapper.Rapport("demo_odfpy_wrapper")

# une table, une ligne
# il faut absolument déter le nb de col
# à la créat du tableau
t = r.creerTableau(10)
r.ajouterFilsA(pere=r.getDocument().text,fils=t)
l = r.creerLigne()
for i in range(10):
    c = r.creerCellule(i)
    r.ajouterFilsA(pere=l, fils=c)

r.ajouterFilsA(pere=t, fils=l)
# jusque là tab une ligne a fonctionné. essayons 2eme ligne
l = r.creerLigne()
for i in range(10):
    c = r.creerCellule("plop")
    r.ajouterFilsA(pere=l, fils=c)

r.ajouterFilsA(pere=t, fils=l)

# fin de l essai 2eme ligne. fonctionne

# essayons de fusionner les cellules hz 2 et 3.
l = r.creerLigne()
c = r.creerCellule("plop")
r.ajouterFilsA(pere=l, fils=c)

c = r.creerCellule("plop", numbercolumnsspanned = "2")
r.ajouterFilsA(pere=l, fils=c)
c = r.creerCelluleRecouverte()
r.ajouterFilsA(pere=l, fils=c)

for i in range(7):
    c = r.creerCellule("plop")
    r.ajouterFilsA(pere=l, fils=c)

r.ajouterFilsA(pere=t, fils=l)

# fin de l essai de fusion cellules hz 2 et 3. fonctionne.
# essai d ajout d un deuxieme tableau à la suite: test de la fonction
# d ajout de tableau à la volée
t = r.tbl(1)
l = r.ligne(t)
r.cell("DEMANDE DE RAPPEL SUR HEURES SUPPLEMENTAIRES",l)
# TODO : essai tel quel:
# commenté, on essaie ligne comme état  la version ligne v1 qui
# prend tableau en param. et qui attache de suite la ligne au tableau
#r.finligne(l,t)
# fin de l essai d ajout d un deuxieme tableau à la suite
# ajout d un troisieme tableau: essai d ajout de tranche:
t = r.tbl(3)
l = r.ligne(t)
r.tranche(l,["rha", "blbl", "meuh"])
l = r.ligne(t)
r.tranche(l,["mouias", "bof", "ok"])
#ok
r.texteLibre(" ")
r.texteLibre("ce texte est libre")
r.sauverDocument()
