
                                                CREATE VIEW 'vue_35_semaine_hsup_sans_bonif'
                                                AS
                                                SELECT strftime('%Y', datetime(jour_travaille, 'start of day', 'weekday 0')) as annee,
                                                strftime('%m', datetime(jour_travaille, 'start of day', 'weekday 0')) as mois,
                                                ( strftime('%j', datetime(jour_travaille, 'start of day', '-3 days', 'weekday 4')) - 1 ) / 7 + 1 as semaine, 
                                                round( SUM( (JulianDay(fin_periode) - JulianDay(debut_periode)) * 24 ) )as heure_semaine_travaillees,
                                                4 as heure_sup_payee_25,
                                                 max(0, 
                                                     min(round( SUM( 
                                                                     (JulianDay(fin_periode)
                                                                     -
                                                                     JulianDay(debut_periode)) 
                                                * 24 ) ) - 35, 43 - 35)
                                                )	as heures_sup_25_effectuees_semaine ,
                                                
                                                 max(0, 
                                                     min(round( SUM( 
                                                     (JulianDay(fin_periode) - JulianDay(debut_periode)) 
                                            		* 24 ) ) - 43, 48 - 43)
                                                )	as heures_sup_50_effectuees_semaine ,
                                                
                                                max(0, 
                                                     min(round( SUM( 
                                                     (JulianDay(fin_periode) - JulianDay(debut_periode)) 
                                                        * 24 ) ) - 48, 1000 - 48)
                                                    )	as heures_sup_50_ille_semaine 	
                                                FROM periodes_travaillees
                                                GROUP BY annee, mois, semaine
                                                ;
                                                