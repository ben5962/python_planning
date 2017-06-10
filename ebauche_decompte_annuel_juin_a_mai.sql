-- fonctionne. il faut grouper par annee_annu maintenant
SELECT 
CAST(strftime('%Y', datetime(jour_travaille))  AS INTEGER) as repere,
CAST(strftime('%m', datetime(jour_travaille))  AS INTEGER) > 5 as bool,
strftime('%Y', datetime(jour_travaille)) as resultat_si_vrai,
strftime('%Y', datetime(jour_travaille)) - 1 as resultat_si_faux,

CASE 
	WHEN cast(strftime('%m', datetime(jour_travaille)) as INTEGER) > 5 THEN strftime('%Y', datetime(jour_travaille))
	ELSE strftime('%Y', datetime(jour_travaille, '-1 year'))
END annee_annu, 

strftime('%Y', datetime(jour_travaille))
	as annee, 
strftime('%m', datetime(jour_travaille)) as mois, 
( strftime('%j', datetime(jour_travaille, 'start of day', '-3 days', 'weekday 4')) - 1 ) / 7 + 1 
as semaine,
datetime(jour_travaille, 'start of day', '-3 days', 'weekday 4') as debut_semaine,
 round( SUM( (JulianDay(fin_periode) - JulianDay(debut_periode)) * 24 ) )
 as heure_semaine_travaillees 
FROM periodes_travaillees 
GROUP BY annee_annu, mois, semaine
ORDER BY annee_annu, mois, semaine;



-- avant le case, les tests donnent le bon résultat. pour année, pour bool pour resutltat_si_vrai pour resultat_si faux.
-- dans le case la valeur renvoyée pour l annee n est psa la bonne. 
-- => utiliser les buitin de date? 

SELECT 
CAST(strftime('%Y', datetime(jour_travaille))  AS INTEGER) as repere,
CAST(strftime('%m', datetime(jour_travaille))  AS INTEGER) > 5 as bool,
strftime('%Y', datetime(jour_travaille)) as resultat_si_vrai,
strftime('%Y', datetime(jour_travaille)) - 1 as resultat_si_faux,

CASE 
	WHEN strftime('%m', datetime(jour_travaille)) > 5 THEN strftime('%Y', datetime(jour_travaille))
	ELSE strftime('%Y', datetime(jour_travaille)) - 1
END annee_annu, 

strftime('%Y', datetime(jour_travaille))
	as annee, 
strftime('%m', datetime(jour_travaille)) as mois, 
( strftime('%j', datetime(jour_travaille, 'start of day', '-3 days', 'weekday 4')) - 1 ) / 7 + 1 
as semaine,
datetime(jour_travaille, 'start of day', '-3 days', 'weekday 4') as debut_semaine,
 round( SUM( (JulianDay(fin_periode) - JulianDay(debut_periode)) * 24 ) )
 as heure_semaine_travaillees 
FROM periodes_travaillees 
GROUP BY annee_annu, mois, semaine;





-- mon raisonnement:
-- taggerles semaines avec annee annu. annee annu c est l'annee si on a passé le début de l'année (mois > mois_fin)
-- c'est l'anne précédente si on n a pas passé ledébut de l année.
-- marche pas : donne des semaines à 160 heures.

-- autre pb : mon annee_annu vaut 0 
SELECT 
CAST(strftime('%Y', datetime(jour_travaille))  AS INTEGER) as repere,
CAST(strftime('%m', datetime(jour_travaille))  AS INTEGER) > 5 as bool,
strftime('%Y', datetime(jour_travaille)) as resultat_si_vrai,
strftime('%Y', datetime(jour_travaille)) - 1 as resultat_si_faux,

CASE 
	WHEN CAST(strftime('%m', datetime(jour_travaille))  AS INTEGER) > 5 THEN strftime('%Y', datetime(jour_travaille))
	ELSE CAST(strftime('%m', datetime(jour_travaille)) AS INTEGER) - 1
END annee_annu, 

strftime('%Y', datetime(jour_travaille))
	as annee, 
strftime('%m', datetime(jour_travaille)) as mois, 
( strftime('%j', datetime(jour_travaille, 'start of day', '-3 days', 'weekday 4')) - 1 ) / 7 + 1 
as semaine,
datetime(jour_travaille, 'start of day', '-3 days', 'weekday 4') as debut_semaine,
 round( SUM( (JulianDay(fin_periode) - JulianDay(debut_periode)) * 24 ) )
 as heure_semaine_travaillees 
FROM periodes_travaillees 
GROUP BY annee_annu, mois, semaine;