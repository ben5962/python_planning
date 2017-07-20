
                                                create view 'plus_de_48'
                                                    as
                                                select
                                                    *
                                                from
                                                    vue_35_semaine 
                                                where
                                                    vue_35_semaine.heure_semaine_travaillees
                                                    > 48
                                                ;
                                                