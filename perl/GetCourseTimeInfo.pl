#!/usr/bin/perl

use DBI;
use DBD::mysql;
use utf8;

binmode STDIN, ":utf8";
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";

require "WorkWithFiles.pl";

#parametri: 
#    $_[0] - connessione al database
#    $_[1] - ID del corso di cui voglio sapere il periodo di svolgimento

sub getTimeInfo() {

	my $DBIConnection = $_[0];
	my $courseID = $_[1];

	my $periodQuery = &openFile("queries/GetTimeInfo.sql");
	$periodQuery =~ s/<afId>/$courseID/g;   #sostituisco al tag fittizion afId l'ID del corso
	
	my $queryHandle = $DBIConnection->prepare($periodQuery);
	$queryHandle->execute();
	
	#ottento anno, trimestre, giorno inizio, giorno fine

	return $queryHandle->fetchrow_hashref();   #restituisco hash risultati

}


1;
