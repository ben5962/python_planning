CREATE TRIGGER
                                                    ajoutperiodestravtrig
                                                    AFTER
                                                        INSERT ON
                                                        planning
                                                    WHEN NEW.categorie_poste = 'travaillé'
                                                    BEGIN
                                                        INSERT OR IGNORE INTO
                                                            jours_travailles (jour)
                                                        SELECT date(NEW.debut_poste) UNION SELECT date(NEW.fin_poste)
                                                        
                                                        ;

                                                        INSERT INTO
                                                            periodes_travaillees (debut_periode, fin_periode, jourtravaille)
                                                        SELECT
                                                            NEW.debut_poste,

                                                            CASE
                                                                WHEN
                                                                    date(NEW.fin_poste)
                                                                    >
                                                                    date(NEW.debut_poste)
                                                                THEN datetime(date(NEW.debut_poste,'+1day'))
                                                                ELSE NEW.fin_poste
                                                            END fin_periode,
                                                            date(NEW.debut_poste)
                                                            FROM planning
                                                           ;
                                                           
                                                        INSERT INTO
                                                            periodes_travaillees (debut_periode, fin_periode, jourtravaille)
                                                        SELECT
                                                            CASE
                                                                WHEN
                                                                    date(NEW.fin_poste)
                                                                    >
                                                                    date(NEW.debut_poste)
                                                                THEN datetime(date(NEW.debut_poste,'+1day'))
                                                                ELSE NEW.debut_poste
                                                            END debut_periode,
                                                            NEW.fin_poste
                                                            date(NEW.fin_poste)
                                                            FROM planning
                                                           ;
                                                                                                                ;
                                                        END;
                                                    