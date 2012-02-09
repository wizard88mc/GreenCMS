/*Query che ritorna le informazioni relative ad una persona dato il suo id*/

SELECT Persona.VARCHAR02 as Cognome, Persona.VARCHAR03 as Nome
FROM Persona
WHERE Persona.ID = "<PersonaID>"; 
