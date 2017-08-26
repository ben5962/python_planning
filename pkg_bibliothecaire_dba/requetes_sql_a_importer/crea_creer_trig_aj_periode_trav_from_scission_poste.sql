CREATE TRIGGER t1 AFTER INSERT ON planning
                                                    WHEN (( NEW.categorie_poste = 'travaillé') AND( date( NEW.debut_poste )  < date ( NEW.fin_poste )) )
                                                    -- entrée à cheval sur deux jours,
                                                    -- il faut la splitter avant insertion
                                                    -- vers periode_travaillée
                                                    BEGIN
                                                    -- CONTRAT D INSERTION
                                                    -- 1er insert : de debut_poste
                                                    -- à fin(jour_calendaire(debut_poste))
                                                    -- C26
                                                    INSERT INTO
                                                        periodes_travaillees (debut_periode, fin_periode, jour_travaille)
                                                    VALUES (
                                                            datetime(NEW.debut_poste),
                                                            datetime(NEW.debut_poste, '+1 day','start of day'),
                                                            date(NEW.debut_poste)
                                                            )
                                                    ;
                                                     -- FIN DU 1ER INSERT C26
                                                     -- CONTRAT D INSERTION
                                                     -- 2eme insert: de fin(jour_calendaire(debut_poste)
                                                     -- à fin_poste
                                                     -- C27
                                                     INSERT INTO
                                                     periodes_travaillees
                                                     (debut_periode, fin_periode, jour_travaille)
                                                     VALUES (datetime(NEW.debut_poste, '+1 day', 'start of day'),
                                                             datetime(NEW.fin_poste),
                                                             date(NEW.fin_poste)
                                                             )
                                                    ; -- FIN DE 2EME INSERT C27
                                                    END; --fin du trigger 