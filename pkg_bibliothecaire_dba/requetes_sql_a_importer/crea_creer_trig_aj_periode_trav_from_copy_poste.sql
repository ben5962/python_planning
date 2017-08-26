
                                                    CREATE TRIGGER t2 AFTER INSERT ON planning
                                                    WHEN (( NEW.categorie_poste = 'travaillé' ) AND ( date (NEW.debut_poste ) = date (NEW.fin_poste ) ) )
                                                    -- entree sur un seul jour
                                                    -- insertion telle quelle de debut_poste et fin_poste vers période_travaillée
                                                    BEGIN
                                                    -- CONTRAT D INSERTION
                                                    -- 1 UNIQUE INSERT: de debut_poste à fin_poste
                                                    -- C28
                                                    INSERT INTO
                                                    periodes_travaillees
                                                    (debut_periode, fin_periode, jour_travaille)
                                                    VALUES (
                                                            datetime(NEW.debut_poste),
                                                            datetime(NEW.fin_poste),
                                                            date(NEW.debut_poste)
                                                            )
                                                    ; -- FIN DE L INSERT UNIQUE C28
                                                    END; -- FIN DU TRIGGER C29