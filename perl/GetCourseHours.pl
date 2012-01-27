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
#    $_[1] - ID del corso di cui voglio sapere le ore

sub getCourseHours() {

	my $DBIConnection = $_[0];
	my $courseID = $_[1];
	
	my $hoursQuery = &openFile("queries/GetHours.sql");
	$hoursQuery =~ s/<afId>/$courseID/g;  #sostituisco al tag fittizion afId l'ID del corso
	
	my $queryHandle = $DBIConnection->prepare($hoursQuery);
	$queryHandle->execute();
	
	return $queryHandle->fetchrow_hashref(); #restituisco l'hash dei risultati
	
}


1;
