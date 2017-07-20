
                                                CREATE VIEW 'vue_CP_semaine'
                                                AS
                                                SELECT
                                                    strftime('%Y', 
                                                        datetime(planning.debut_poste, 'start of day', 'weekday 0')) as annee,
                                                 strftime('%m', datetime(planning.debut_poste, 'start of day', 'weekday 0')) as mois, 
                                                 ( strftime('%j', datetime(planning.debut_poste, 'start of day', '-3 days', 'weekday 4')) - 1 ) / 7 + 1 as semaine, 
                                                 round( SUM( (JulianDay(fin_poste) - JulianDay(debut_poste)) * 24 ), 2 )as heure_semaine_CP
                                                 FROM 
                                                    planning 
                                                WHERE 
                                                    planning.nom_poste = 'CP'
                                                GROUP BY annee, mois, semaine
                                                ;