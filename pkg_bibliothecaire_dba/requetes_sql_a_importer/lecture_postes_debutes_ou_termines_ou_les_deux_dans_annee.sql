SELECT debut_poste as 'd [timestamp]', fin_poste as 'f [timestamp]' 
                                                    from planning 
                                                    WHERE  d > ?  AND f <= ?