#!/usr/bin/perl

use DBI;
use DBD::mysql;
use utf8;

sub retrieveExamSource() {

	my $DBIConnection = $_[0];
	my $examID = $_[1];
	
	my $sourceQuery = "SELECT Nome, Locazione FROM Risorsa r JOIN joinEventoRisorsa j WHERE r.ID = j.IDRisorsa AND j.IDEvento = $examID;";
	
	my $queryHandle = $DBIConnection->prepare($sourceQuery);
	
	$queryHandle->execute();
	
	return $queryHandle->fetchrow_hashref();


}

1;
