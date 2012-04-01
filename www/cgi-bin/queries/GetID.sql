/*
	IDTipoPersona: - 2 = decenti
		       - 4 = dottorandi
		       -12 = rappresentanti studenti

        Gruppo:        -121 = ccl informatica
		       -147 = dottorandi informatica 
*/




SELECT Persona.ID 
FROM Persona, Gruppo, joinPersonaGruppo
WHERE Persona.ID = joinPersonaGruppo.IDPersona
AND joinPersonaGruppo.IDGruppo = Gruppo.ID
AND Persona.IDTipoPersona = '<idTP>'
AND Gruppo.ID = '<idTG>'
ORDER BY Persona.VARCHAR02;