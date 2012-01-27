/*
Query che ritorna il cognome e il nome del responsabile dell'esame corrispondente ad un id.

<afId> viene gestito automaticamente dagli script perl e viene sosituito con l'id di un insegnamento.

Tabelle utilizzate: -af = insegnamenti
		    -carichi = tabella di relazione tra af e personale
		    -personale = persone

*/

SELECT personale.cognome, personale.nome, titoli.titolo as titolo_id, personale.website as website
FROM personale, af, carichi, titoli
WHERE af.id = "<afId>"
AND carichi.af_id = af.id
AND carichi.responsabile = 1
AND personale.titolo_id = titoli.id
AND carichi.personale_id = personale.id; 
