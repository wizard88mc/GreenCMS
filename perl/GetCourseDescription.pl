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
#    $_[1] - ID del corso di cui voglio avere la descrizione

sub getCourseDescription() {

	my $DBIConnection = $_[0];
	my $courseID = $_[1];
	
	my $descriptionQuery = &openFile("queries/GetDescription.sql");
	$descriptionQuery =~ s/<afId>/$courseID/g;  #sostituisco al tag fittizio <afId> l'ID del corso
	
	my $queryHandle = $DBIConnection->prepare($descriptionQuery);
	$queryHandle->execute();
	
	my $teachingName = $queryHandle->fetchrow_hashref();  #metto i risultati in un hash
	return $teachingName->{'descr_ita'};

}


1;
