#!/usr/bin/perl

use DBI;
use DBD::mysql;
use utf8;

#parametri:
#    $_[0] - connessione al database
#    $_[1] - id che identifica il tipo di professore (2 o 10 per Docenti, 12 per Rapp. Studenti, 4 per Dottorandi)
#    $_[2] - id che identifica il tipo del gruppo (121 Docenti e Rappresentanti Studenti, 147 Dottorandi)

sub getTeachersID() {

	my $DBIConnection = $_[0];
	my $tipocorso = $_[1];
	my $descr = $_[2];

	my $coursesQuery = &openFile("queries/GetID.sql");
	$coursesQuery =~ s/<idTP>/$tipocorso/g;   #sostituisco al tag <tipocorso> il tipo del corso (o L o LM)
	$coursesQuery =~ s/<idTG>/$descr/g;   #sostituisco  al tag <descrizione> la descrizione del corso di cui voglio avere l'ID dei corsi
	
	my $queryHandle = $DBIConnection->prepare($coursesQuery);
	$queryHandle->execute();
	
	return $queryHandle;  #restituisco il risultato ottenuto

}

1;