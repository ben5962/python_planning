CREATE TABLE planning(
                                                        idx_planning INTEGER NOT NULL PRIMARY KEY,
                                                        debut_poste timestamp,
                                                        fin_poste timestamp,
                                                        nom_poste TEXT,
                                                        categorie_poste TEXT,
                                                        CONSTRAINT debut_unique UNIQUE (debut_poste),
                                                        CONSTRAINT fin_unique UNIQUE (fin_poste))
                                                        ;