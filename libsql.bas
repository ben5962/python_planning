'********************************************************************************
'Copyright (C) 2003 Laurent Godard
'dev.godard@wanadoo.fr
'
'Dévéloppement financé par la société SPENO
'
'This library is free software; you can redistribute it and/or
'modify it under the terms of the GNU Lesser General Public
'License as published by the Free Software Foundation; either
'version 2.1 of the License, or (at your option) any later version.

'This library is distributed in the hope that it will be useful,
'but WITHOUT ANY WARRANTY; without even the implied warranty of
'MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
'Lesser General Public License for more details.
'http://www.opensource.org/licenses/lgpl-license.php

'You should have received a copy of the GNU Lesser General Public
'License along with this library; if not, write to the Free Software
'Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
'******************************************************************************

Option Explicit

Global Arret as boolean

Function CalcSQL1(NomSource, Requete, Optional AfficheTitre, Optional BorneMax, Optional BorneMin)

dim CodeErreur as long, message as string
dim oDBContext as object, RetourBase as boolean
dim oDB as object, LaBase as object
dim LaRequete as object, LeResultSet as object
dim LesColonnes as object, LaColonne as object
dim NbChamp as long
dim i as long
dim tabResultat()
dim AfficherTitre as boolean, decal as long


'Initialisations
Redim tabResultat(0,0)
CodeErreur=0
Arret=false
on error goto GestionErreur

const NbSecondes=30

NomSource=Trim(NomSource)
Requete=Trim(Requete)

'Vérification des arguments
if NomSource="" then
	CodeErreur=1
endif

if Requete="" then
	CodeErreur=2
endif

'Traitement des erreurs d'arguments
if codeErreur<>0 then
	goto GestionErreur
endif

'Traitement des paramètres optionels
	
if IsMissing(BorneMin) then
	BorneMin=0
else
	if not IsNumeric(BorneMin) then
		CodeErreur=5
		goto GestionErreur
	endif
endif

if IsMissing(BorneMax) then
	BorneMax=-1
else
	if not IsNumeric(BorneMax) then
		CodeErreur=5
		goto GestionErreur
	endif
endif

if IsMissing(AfficheTitre) then
	AfficherTitre=false
else
	if val(Affichetitre)=1 then
		AfficherTitre=true
	else
		AfficherTitre=false
	endif
endif

'Vérification de l'existence de la source
oDBContext = CreateUnoService("com.sun.star.sdb.DatabaseContext")
RetourBase=oDBContext.hasByName(NomSource)

If not RetourBase then
	CodeErreur=4
	goto GestionErreur
endif

'connection à la source

oDB=oDBContext.getbyname(NomSource)
'Pour des raisons de sécurité, les login et password sont à gérer dans la source de données
LaBase=oDB.getConnection("","") 


'preparation de la requete
LaRequete=LaBase.createStatement()

LaRequete.QueryTimeout=NbSecondes

'envoie de la requete
LeResultSet=laRequete.executeQuery(Requete)

dim NbLignes, LaValeur

'boucle sur les enregistrements
dim Suivant as boolean


Suivant=LeResultSet.next

if Not Suivant then
	CodeErreur=3
	goto GestionErreur
endif

NbLignes=0
NbChamp=LeResultSet.getColumns.count
ReDim TabResultat(1 to 1,1 to NbChamp)

if AfficherTitre then
	decal=1
	LesColonnes=LeResultSet.getColumns
	For i=1 to nbChamp
		TabResultat(1,i)=LesColonnes(i-1).name
	next i
	NbLignes=nbLignes+1
else
decal=0
endif

for i=0 to BorneMin-1
	LeResultSet.next
next i

do

Nblignes=NbLignes+1
'la ligne suivante est tres tres consomatrice
Redim Preserve TabResultat(1 to NbLignes,1 to NbChamp)
	LesColonnes=LeResultSet.getColumns
	for i=1 to nbChamp
		laColonne=Lescolonnes(i-1)
		LaValeur=lacolonne.string
			if Not isNull(LaValeur) then
				if isNumeric(LaValeur) then
					TabResultat(NbLignes,i)=Val(LaValeur)
				else
					TabResultat(NbLignes,i)=LaValeur
				endif
			else
				TabResultat(NbLignes,i)="Null"
			endif	
	next i
	
Suivant=LeResultset.next

loop until not Suivant or Arret or (NbLignes=BorneMax-BorneMin+decal and BorneMax>-1)


CalcSQL1=TabResultat()

exit Function

'traitement d'erreur
GestionErreur:
	select case CodeErreur
		Case 1:
			message="Le nom de la source de données ne peut être vide"
		Case 2:
			message="La requête ne peut être vide"
		Case 3:
			message="Aucun Enregistrement"
		case 4:
			message="Source de données inconnue"
		case 5:
			message="Erreur dans les bornes"
		case else
			message="Erreur Inconnue"	
	end select
	tabResultat(0,0)=message
	CalcSQL1=tabResultat()

End function

'--------------------------------------------------------------
'--------------------------------------------------------------
'--------------------------------------------------------------

Function Quote(chaine) as string
'double les quotes de l'argument chaine
'encadre l'argument entre quotes
dim temp as string
dim i as long

temp=chaine
i=instr(temp,"'")
while i>0
	temp=left(temp,i)+"'"+mid(temp,i+1)
	i=i+2
	i=instr(i,temp,"'")	
wend

Quote="'"+temp+"'"

end function
'--------------------------------------------------------------
'--------------------------------------------------------------
'--------------------------------------------------------------


Sub ArretUrgence
	Arret=true
end sub

'--------------------------------------------------------------
'--------------------------------------------------------------
'--------------------------------------------------------------
Function CalcSQL2(NomFeuille,CelluleCible,NomSource, Requete)

dim CodeErreur as long, message as string
dim oDBContext as object, RetourBase as boolean
dim LeCellRange
dim ParamSource(2) as new com.sun.star.beans.PropertyValue
Dim FeuilleRes

'Initialisations
CodeErreur=-1

'on error goto GestionErreur

NomSource=Trim(NomSource)
Requete=Trim(Requete)

'Vérification des arguments
if NomSource="" then
	CodeErreur=1
endif

if Requete="" then
	CodeErreur=2
endif

If NomFeuille="" then
	CodeErreur=3
endif

'Traitement des erreurs d'arguments

if codeErreur>0 then
	goto GestionErreur
endif

'Vérification de l'existence de la source
oDBContext = CreateUnoService("com.sun.star.sdb.DatabaseContext")
RetourBase=oDBContext.hasByName(NomSource)

If not RetourBase then
	CodeErreur=4
	goto GestionErreur
endif


'Définition feuille Cible
If not thisComponent.sheets.hasByName(NomFeuille) then
	CodeErreur=3
	goto GestionErreur
endif
FeuilleRes=thisComponent.sheets.getByName(NomFeuille)
LeCellRange=FeuilleRes.getCellRangeByName(CelluleCible+":"+CelluleCible)

'Importation Base
paramSource(0).name="DatabaseName"
paramSource(0).value=NomSource'"SDDGrosseTable"
paramSource(1).name="SourceType"
paramSource(1).value=com.sun.star.sheet.DataImportMode.SQL
paramSource(2).name="SourceObject"
paramSource(2).value=Requete'"select * from grosseTable where numligne>12500"

'Importe
LeCellRange.doImport(paramSource())

'Tout s'est bien passé
CodeErreur=0

'Nettoyer les cellules restante
'remplir les celules de la ligne suivante avec "-----"

'traitement d'erreur
GestionErreur:
	select case CodeErreur
		case 0: 'Pas d'erreur
			message="Ok - MaJ "+NomFeuille+" - "+CelluleCible
		Case 1:
			message="Le nom de la source de données ne peut être vide"
		Case 2:
			message="La requête ne peut être vide"
		Case 3:
			message="Spécifier une feuille cible valide, différente de la feuille en cours"
		case 4:
			message="Source de données inconnue"
		case else
			message="Erreur Inconnue"	
	end select

CalcSQL2=message

End function
'--------------------------------------------------------------
'--------------------------------------------------------------
'--------------------------------------------------------------
Function CalcSQL3(NomSource, Requete, Optional Bornes, Optional Titre)

dim CodeErreur as long, message as string
dim oDBContext as object, RetourBase as boolean
dim LeCellRange
dim ParamSource(2) as new com.sun.star.beans.PropertyValue
Dim FeuilleRes, NomFeuille as string
dim montableau()
dim LesDataBases, leDataRange, LesCells

dim i as long, j as long
dim VirerTitre as boolean, ChkBornes as boolean
dim max1 as long,min1 as long,max2 as long,min2 as long,decal as long, rang as long
dim BorneMin as long, BorneMax as long
dim decoupe, laLigne

'Initialisations
CodeErreur=-1

on error goto GestionErreur

NomSource=Trim(NomSource)
Requete=Trim(Requete)

'Vérification des arguments
if NomSource="" then
	CodeErreur=1
endif

if Requete="" then
	CodeErreur=2
endif

if codeErreur>0 then
	goto GestionErreur
endif

'Traitement des erreurs d'arguments

if IsMissing(Titre) then
	VirerTitre=false
else
	VirerTitre=true
endif

if IsMissing(Bornes) then
	chkBornes=false
else
	chkBornes=true
	decoupe=split(Bornes,":")
	if ubound(decoupe)<>1 then 
		CodeErreur=5
		goto GestionErreur
	endif
	if not isNumeric(decoupe(0)) or not isNumeric(decoupe(1)) then
		CodeErreur=5
		goto GestionErreur
	endif
	BorneMin=decoupe(0)
	BorneMax=decoupe(1)	
endif

'Vérification de l'existence de la source
oDBContext = CreateUnoService("com.sun.star.sdb.DatabaseContext")
RetourBase=oDBContext.hasByName(NomSource)

If not RetourBase then
	CodeErreur=4
	goto GestionErreur
endif


'Définition feuille Cible
NomFeuille="TempCalcSQL"
If not thisComponent.sheets.hasByName(NomFeuille) then
	FeuilleRes=thisComponent.sheets.InsertNewByName(NomFeuille,1)
else
	FeuilleRes=thisComponent.sheets.getByName(NomFeuille)
endif
if FeuilleRes.isVisible then
	FeuilleRes.isVisible=false
endif
LeCellRange=FeuilleRes.getCellRangeByName("A1:A1")

'Importation Base
paramSource(0).name="DatabaseName"
paramSource(0).value=NomSource'"SDDGrosseTable"
paramSource(1).name="SourceType"
paramSource(1).value=com.sun.star.sheet.DataImportMode.SQL
paramSource(2).name="SourceObject"
paramSource(2).value=Requete'"select * from grosseTable where numligne>12500"

'Importe
LeCellRange.doImport(paramSource())


'Cherche le databaseRange temporaire
lesdatabases=thiscomponent.databaseranges
for i=0 to lesdatabases.count-1
	if not lesdatabases(i).isUserDefined then
		leDataRange=lesdatabases(i)
		exit for
	endif
next i

lesCells=leDataRange.ReferredCells

montableau=lescells.getdataArray()

'Nettoyage com.sun.star.sheet.CellFlags.VALUE + com.sun.star.sheet.CellFlags.DATETIME + com.sun.star.sheet.CellFlags.STRING)
LesCells.ClearContents(1+2+4)

'1: lignes
'2: colonnes


max1=ubound(monTableau)
max2= ubound(monTableau(0))
min2=0
min1=1

if chkBornes then
	if bornemax<max1 then
		max1=borneMax
	endif
	if borneMin>min1 then
		min1=borneMin
	endif
endif


if virerTitre then
	decal=0
else 
	decal=1
endif

Dim retour(min1 to max1+decal, 0 to max2)

if not VirerTitre then
	laLigne=montableau(0)
	rang=lbound(retour(),1)
	for j=0 to max2
		retour(rang,j)=laLigne(j)
	next j
endif


for i=min1 to max1
	laligne=monTableau(i)
	rang=i+decal
	for j=0 to max2
		retour(rang,j)=laLigne(j)
	next j
next i

CalcSQL3=retour()

exit function

'traitement d'erreur
GestionErreur:
	select case CodeErreur
		Case 1:
			message="Le nom de la source de données ne peut être vide"
		Case 2:
			message="La requête ne peut être vide"
		Case 3:
			message="Spécifier une feuille cible valide, différente de la feuille en cours"
		case 4:
			message="Source de données inconnue"
		case 5:
			message="Format de bornes non valide : ""<min>:<max>"""
		case else
			message="Erreur Inconnue"	
	end select

CalcSQL3=message

End function

