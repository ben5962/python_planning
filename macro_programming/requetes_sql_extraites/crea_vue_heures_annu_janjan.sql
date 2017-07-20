
                                                CREATE view 'VUE_heures_annu_janjan'
                                                AS
                                                SELECT 
                                                strftime('%Y', datetime(jour_travaille))
                                                as annee, 
                                                strftime('%m', datetime(jour_travaille)) as mois, 
                                                ( strftime('%j', datetime(jour_travaille, 'start of day', '-3 days', 'weekday 4')) - 1 ) / 7 + 1 as semaine,
                                                 round( SUM( (JulianDay(fin_periode) - JulianDay(debut_periode)) * 24 ) )
                                                 as heure_semaine_travaillees 
                                                FROM periodes_travaillees 
                                                GROUP BY annee

                                                ;

                                                    