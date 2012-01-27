/*
Query che ritorna informazioni generali legate ad un insegnamento.
In particolare: -propedeuticità
		-prerequisiti
		-testi didattici
		-audili didattici
		-programma dell'insegamento
		-ordinamento
		-tipologia
		-ambito
		-ssd
		-curriculum
<afId> viene gestito automaticamente dagli script perl e viene sosituito con l'id di un insegnamento.
<langId> - 1 italiano
	 - 2 inglese
*/

SELECT af.propedeuticita, af.prerequisiti, testi.testididattici, testi.ausilididattici, testi.programmacorso, corsi.normativa as ordinamento, tipologie.descr as tipologia, ambiti.descr as ambito, GROUP_CONCAT(ssd.sigla) as ssd, cp.descr as curriculum, af.nr_esame
FROM af, testi, tasc, tasc_ssd, ssd, tipologie, ambiti, corsi, corsi_cp, cp
WHERE af.id = "<afId>"
AND af.corso_id = corsi.id
AND testi.af_id = af.id 
AND testi.lingua_id = <langId>
AND tasc.af_id = af.id
AND tasc.ambito_id = ambiti.id
AND tasc.tipologia_id = tipologie.id
AND tasc.id = tasc_ssd.tasc_id
AND tasc_ssd.ssd_id = ssd.id
AND af.corso_cp_id = corsi_cp.id
AND corsi_cp.cp_id = cp.id
GROUP BY af.id;