#!/usr/bin/perl

use DBI;
use DBD::mysql;
use utf8;

#parametri:
#    $_[0] - connessione al database
#    $_[1] - id del docente

sub getTeacherInformations() {

	my $DBIConnection = $_[0];
	my $teacherID = $_[1];
	
	my $coursesQuery = &openFile("queries/GetInformations.sql");
	$coursesQuery =~ s/<PersonaID>/$teacherID/g;   #sostituisco al tag <tipocorso> il tipo del corso (o L o LM)
	
	my $queryHandle = $DBIConnection->prepare($coursesQuery);
	$queryHandle->execute();
	
	return $queryHandle->fetchrow_hashref();

}

1;