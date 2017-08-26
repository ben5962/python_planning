CREATE VIEW 'essai_create_func' AS
SELECT idx INTEGER NOT NULL PRIMARY KEY,
debut_poste, 
ate(debut_poste) as date, 
isoweek(date(debut_poste) as iso 
from planning