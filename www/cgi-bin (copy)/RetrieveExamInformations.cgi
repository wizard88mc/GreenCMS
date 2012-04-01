#!/usr/bin/perl

use DBI;
use DBD::mysql;
use utf8;

sub retrieveExamInformations() {

	my $DBIConnection = $_[0];
	my $examID = $_[1];
	
	my $informationsQuery = "SELECT DATE_FORMAT(Data, '\%d/\%m/\%Y') AS Data, DATE_FORMAT(OraInizio, '\%H:\%i') AS OraInizio, DATE_FORMAT(OraFine, '\%H:\%i') AS OraFine, DescrizioneEvento FROM Evento WHERE ID=$examID;";
	
	my $queryHandle = $DBIConnection->prepare($informationsQuery);
	
	$queryHandle->execute();
	
	return $queryHandle->fetchrow_hashref();



}

1;
