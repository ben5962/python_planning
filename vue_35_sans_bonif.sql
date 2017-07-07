-- avant le passage � la sous requete, 
-- l original



SELECT 
-- les p�riodes
-- p1 : ann�e
	strftime('%Y', 
			datetime(jour_travaille, 
					'start of day', 
						'weekday 0')) 
						as annee, 
-- p2: mois
	strftime('%m', 
			datetime(jour_travaille, 
				'start of day', 
				'weekday 0')) 
				as mois, 
-- p3: semaine
( strftime('%j', 
	datetime(jour_travaille, 
			'start of day', 
			'-3 days', 
			'weekday 4')) - 1 ) / 7 + 1 
			as semaine, 
-- fin des p�riodes

-- d�but des calculs

-- c1 heures effectu�es dans la semaine
-- somme les differences d heures chaque jour.
--  technique : la diff�rence est en jour. 
--         conversion en heures? * 24. 
--          round pour faire bonne mesure. 
-- dans le group by, on indique que cette somme se limite
--- � la semaine:
round( 
		SUM( 
				(
				JulianDay(fin_periode) 
				- 
				JulianDay(debut_periode)
				) 
				* 24 )
				)
as heure_semaine_travaillees, 
-- constante : 4 heures sup pay�es par semaine trav
4 as constante_heure_sup_payee_25, 

-- c2 : calcul de la qt� heures hebdo
--  entre 35 et 43 heures depuis les heures effectuees 
max(0, min(round( SUM( (JulianDay(fin_periode) - JulianDay(debut_periode)) * 24 ) ) - 35, 43 - 35) ) 
as heures_sup_25_effectuees_semaine , 
-- c3: calcul de la qt� heures hebdo entre 43 et 48
max(0, min(round( SUM( (JulianDay(fin_periode) - JulianDay(debut_periode)) * 24 ) ) - 43, 48 - 43) ) 
as heures_sup_50_effectuees_semaine , 
-- c4: calcul de la qt� heurs hebdo au d�l� de 48
max(0, min(round( SUM( (JulianDay(fin_periode) - JulianDay(debut_periode)) * 24 ) ) - 48, 1000 - 48) ) 
as heures_sup_50_ille_semaine 
-- c4: qt� heures 25 restant dues
-- c5: qt� heures 50 restant dues
-- c6 : qt� heures ill� 50 restant dues
-- c7 : eqv heures trv des heures 25 restatn dues (c4x1,25)
-- c8 : eqv heures trv des heures 50 restant dues (c5x 1,50)
-- c9 : eqv heures trv des heures 50 ille restant dues (c6x 1,50)
-- C10 : total eqv heures heures restant dues hebdo
FROM periodes_travaillees GROUP BY annee, mois, semaine