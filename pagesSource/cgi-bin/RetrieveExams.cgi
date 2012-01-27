#!/usr/bin/perl

use DBI;
use DBD::mysql;
use utf8;

sub retrieveExamsID() {

	my $DBIConnection = $_[0];

	my $examsQuery = "SELECT ID From Evento WHERE Descizione Evento LIKE \"[INF]\%\" AND IDTipoEvento <> 27";
	
	my $queryHandle = $DBIConnection->prepare($examsQuery);
	
	$queryHandle->execute();
	
	return $queryHandle;


}

1;
