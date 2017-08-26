create view
                                                        'vue_cumul_annu_juin_a_mai'
                                                            as
                                                            select 
                                                            sem_annu_juin_a_mai.annee_annu as annee_annu, 
                                                            sem_annu_juin_a_mai.mois as mois ,
                                                            sum(sem_annu_juin_a_mai.heure_semaine_travaillees) as vol_annu
                                                            from 

                                                            -- fonctionne. il faut grouper par annee_annu maintenant
                                                            (SELECT 
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
                                                            ORDER BY annee_annu, mois, semaine ) sem_annu_juin_a_mai
                                                            GROUP BY annee_annu
                                                            ;
                                                            