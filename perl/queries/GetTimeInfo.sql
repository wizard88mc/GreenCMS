/*
Query che ritorna l'anno, il trimestre, la data d'inizio e fine di un esame

<afId> viene gestito automaticamente dagli script perl e viene sosituito con l'id di un insegnamento.

Tabelle utilizzate: -af = insegnamenti
		    -corsi = corsi di laurea
		    -aa = anni accademici
		    -calendari/periodi/af_periodi = informazioni dulle date/anni ecc.

*/

SELECT anni.descr as anno, periodi.descr as trimestre, calendari.inizio_periodo as inizio, calendari.fine_periodo as fine
FROM af, calendari, anni, periodi, af_periodi
WHERE af.id = "<afId>"
AND af_periodi.af_id = af.id
AND af_periodi.periodo_id = periodi.id
AND af_periodi.anno_id = anni.id
AND periodi.id = calendari.periodo_id
AND af.aa_id = calendari.aa_id;
