CREATE TABLE jours_travailles (
                                                    jour TEXT,
                                                    CONSTRAINT jour_unique UNIQUE(jour) ON CONFLICT IGNORE
                                                    )
                                                    ;