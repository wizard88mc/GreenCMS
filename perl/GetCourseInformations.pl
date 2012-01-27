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
#    $_[1] - ID del corso di cui voglio sapere le informazioni

sub getInformationsCourse() {


	my $DBIConnection = $_[0];
	my $courseID = $_[1];
	my $langID = $_[2];
	
	my $informationsQuery = &openFile("queries/GetInformation.sql");
	$informationsQuery =~ s/<afId>/$courseID/g;  #sostituisco al tag fittizion afId l'ID del corso
	$informationsQuery =~ s/<langId>/$langID/g;
	
	my $queryHandle = $DBIConnection->prepare($informationsQuery);
	$queryHandle->execute() or die "$informationsQuery";
	
	return $queryHandle->fetchrow_hashref();  #restituisco l'hash dei risultati ottenuti


}


1;
