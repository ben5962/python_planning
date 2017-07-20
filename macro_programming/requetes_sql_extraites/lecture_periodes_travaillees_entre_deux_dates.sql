SELECT
                                                            debut_periode as "debut_periode [timestamp]",
                                                            fin_periode as "fin_periode [timestamp]"
                                                        FROM
                                                            periodes_travaillees
                                                        WHERE
                                                            date( periodes_travaillees.jour_travaille )
                                                            BETWEEN
                                                                    date ( ? )
                                                                AND
                                                                    date( ? ) 
                                                            ; -- C33