/*
Query che ritorna il nome dell'isegnamento corrispondente ad un id

<afId> viene gestito automaticamente dagli script perl e viene sosituito con l'id di un insegnamento.

Tabelle utilizzate: -af = insegnamenti
		    -af_descri = descrizioni degli insegnamenti
*/

SELECT af_descri.descr_ita
FROM af_descri, af
WHERE af.id = "<afId>"
AND af.af_descri_id = af_descri.id;
