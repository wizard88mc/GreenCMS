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
#    $_[1] - ID del corso di cui voglio sapere il numero di crediti

sub getCourseCFU() {

	my $DBIConnection = $_[0];
	my $courseID = $_[1];
	
	my $CFUQuery = &openFile("queries/GetCfu.sql");
	$CFUQuery =~ s/<afId>/$courseID/g;   #sostituisco ad <afId> nella query l'ID del corso
	
	my $queryHandle = $DBIConnection->prepare($CFUQuery);
	$queryHandle->execute();

	my $CFU = $queryHandle->fetchrow_hashref();  #prendo i risultati e li metto in un hash
	
	return $CFU->{'cfu'};
	

}


1;
