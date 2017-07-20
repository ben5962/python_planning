
                                                CREATE VIEW
                                                    'hs_dues_hebdo'
                                                AS
                                                SELECT
                                                    table_hs_hebdo.a as a,
                                                    table_hs_hebdo.m as m,
                                                    table_hs_hebdo.s as s,
                                                    table_hs_hebdo.t as t,
                                                    table_hs_hebdo.hs_25_hebdo - table_hs_hebdo.cte as hs_25_dues,
                                                    table_hs_hebdo.hs_50_hebdo as h50_l,
                                                    table_hs_hebdo.hs_ille_hebdo as h50_i,
                                                    table_hs_hebdo.hs_50_hebdo + table_hs_hebdo.hs_ille_hebdo as hs_50_dues,
                                                    (table_hs_hebdo.hs_25_hebdo - table_hs_hebdo.cte) * 1.25 as eqv_t_hs_25_dues,
                                                    table_hs_hebdo.hs_50_hebdo * 1.5 as eqv_t_hs_50_l_dues,
                                                    table_hs_hebdo.hs_ille_hebdo * 1.5 as eqv_t_hs_50_i_dues,
                                                    (table_hs_hebdo.hs_50_hebdo * 1.5) + (table_hs_hebdo.hs_ille_hebdo * 1.5) + (table_hs_hebdo.hs_25_hebdo - table_hs_hebdo.cte) * 1.25 as eqv_t_tot_h_dues
                                                FROM
                                                    (
                                                    SELECT 
                                                        table_h_hebdo.annee as a, 
                                                        table_h_hebdo.mois as m,
                                                        table_h_hebdo.semaine as s,
                                                        table_h_hebdo.trav as t,
                                                        4 as cte,
                                                        max(0, min(table_h_hebdo.trav - 35, 43 - 35) )  as hs_25_hebdo,
                                                        max(0, min(table_h_hebdo.trav - 43, 48 - 43) ) as hs_50_hebdo,
                                                        max(0, min(table_h_hebdo.trav - 48, 1000 - 48) )  as hs_ille_hebdo
                                                    FROM 
                                                        ( SELECT
                                                        --  LA SUBQUERY DE BASE : a m s hs_trav_hebdo
                                                        -- les périodes
                                                        -- p1 : année
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
                                                        -- fin des périodes

                                                        -- début des calculs

                                                        -- c1 heures effectuées dans la semaine
                                                        -- somme les differences d heures chaque jour.
                                                        --  technique : la différence est en jour. 
                                                        --         conversion en heures? * 24. 
                                                        --          round pour faire bonne mesure. 
                                                        -- dans le group by, on indique que cette somme se limite
                                                        --- à la semaine:
                                                        round( 
                                                                SUM( 
                                                                        (
                                                                            JulianDay(fin_periode) 
                                                                            - 
                                                                            JulianDay(debut_periode)
                                                                        ) 
                                                                    * 24 )
				)
                                                                as trav



                                                        FROM periodes_travaillees GROUP BY annee, mois, semaine
                                                        ) table_h_hebdo
                                                    ) table_hs_hebdo
                                                            ;


                                                
                                                