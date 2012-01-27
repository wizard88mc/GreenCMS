#!/usr/bin/perl

use DBI;
use DBD::mysql;
use utf8;

#funzione che recupera il docente dell'esame (Per gli eventi)
#parametri: connessione, ID dell'esame

sub retrieveTeacherExam() {

	my $DBIConnection = $_[0];
	my $examID = $_[1];
	
	#costruisco query
	my $teacherQuery = "SELECT p.VARCHAR02 As Cognome, p.VARCHAR03 As Nome FROM Persona p, Evento e WHERE e.ID=$examID AND p.ID = e.IDPersona;";
	
	#preparo query
	my $queryHandle = $DBIConnection->prepare($teacherQuery);
	
	#esegup
	$queryHandle->execute();

	my $informations = $queryHandle->fetchrow_hashref();

	#restituisco Cognome Nome	
	return $informations->{'Cognome'} . " " . $informations->{'Nome'};

}

1;
