/*
Query che ritorna i cfu totali di un insegnamento

<afId> viene gestito automaticamente dagli script perl e viene sosituito con l'id di un insegnamento.

Tabelle utilizzate: -af = insegnamenti
		    -tasc = tabella con molte informazioni relative agli esami      

*/

SELECT SUM(tasc.cfu) as cfu
FROM tasc, af
WHERE af.id = "<afId>"
AND tasc.af_id = af.id
GROUP BY af.id;