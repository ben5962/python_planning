CREATE TABLE planning (
                                                     idx_planning NOT NULL INTEGER PRIMARY KEY,
                                                    debut_poste TEXT,
                                                    fin_poste TEXT,
                                                    nom_poste TEXT,
                                                    categorie_poste TEXT,
                                                    CONSTRAINT debut_unique UNIQUE (debut_poste),
                                                    CONSTRAINT fin_unique UNIQUE (fin_poste))