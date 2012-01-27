/*
Query che ritorna le ore relative ad un esame, in particolare quelle frontali, di esercizi e di laboratorio.

La query è semplice e non necessita di spiegazioni.
*/

SELECT ore_frontali, ore_esercizi, ore_lab
FROM af
WHERE af.id = "<afId>"; 
