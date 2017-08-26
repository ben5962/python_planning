CREATE TABLE periodes_travaillees (
                                                    debut_periode TEXT,
                                                    fin_periode TEXT CHECK(fin_periode > debut_periode),
                                                    jour_travaille TEXT,
                                                    CONSTRAINT periode_unique UNIQUE(debut_periode, fin_periode, jour_travaille) 
                                                    )
                                                    ;