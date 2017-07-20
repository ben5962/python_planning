SELECT
                                                            debut_poste as "debut_poste [timestamp]",
                                                            fin_poste as "fin_poste [timestamp]"
                                                        FROM
                                                            planning
                                                        WHERE
                                                                planning.categorie_poste = 'absence'
                                                            AND
                                                                nom_poste = 'CP'
                                                            AND
                                                                date( planning.debut_poste )
                                                                    BETWEEN
                                                                        date ( ? )
                                                                    AND
                                                                        date ( ? )
                                                        ; -- NON CLASSE
                                                    
                                                    