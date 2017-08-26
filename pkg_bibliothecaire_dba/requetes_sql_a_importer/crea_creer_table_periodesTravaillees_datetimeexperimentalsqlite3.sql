CREATE TABLE periodes_travaillees (
                                                    debut_periode timestamp,
                                                    fin_periode timestamp CHECK(fin_periode > debut_periode),
                                                    jour_travaille DATE,
                                                    CONSTRAINT periode_unique UNIQUE(debut_periode, fin_periode, jour_travaille) 
                                                    )
                                                    ;