/*
Query che ritorna gli id degli insegnamenti dei corsi di laurea in informatica dell'anno corrente escludendo gli sdoppiamenti e i corsi integrati. 

<tipocorso>: può essere L (laurea in informatica) o LM (laurea magistrale)
<descrizione>: può essere INFORMATICA o INFORMATICA%2009

I due tag precedenti sono gestiti automaticamente dagli script perl che andranno a sostituirli a seconda della necessità.

Lo script seleziona dalla tabella af (degli insegnamenti) gli id degli esami appartenenti al corso di laurea corretto e dell'anno corrente.

Tabelle usate: -aa = anno caccademico
	       -af = inegnamenti
	       -corsi = corsi di laurea
	       
NOTA: data 5.10.2011 aggiunto af.status=1 per cambiamento rad

*/


SELECT af.id
FROM corsi, aa, af, af_descri, tipi_af, corsi_cp, cp
WHERE aa.id = corsi.aa_id 
AND aa.corrente = 1 
AND corsi.tipocorso = "<tipocorso>"
AND corsi.descr LIKE '<descrizione>'
AND corsi.id = af.corso_id
AND af.af_descri_id = af_descri.id
AND af.tipo_af_id = tipi_af.id
AND tipi_af.sigla NOT LIKE 'CI'
AND af_descri.descr_ita NOT LIKE '%(sdoppiamento)%'
AND af.corso_cp_id = corsi_cp.id
AND corsi_cp.cp_id = cp.id
ORDER BY af.nr_esame;