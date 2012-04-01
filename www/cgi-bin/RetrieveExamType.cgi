#!/usr/bin/perl

use DBI;
use DBD::mysql;
use utf8;

sub retrieveExamType() {

	my $DBIConnection = $_[0];
	my $examID = $_[1];
	
	my $typeQuery = "SELECT Descrizione FROM TipoEvento t JOIN Evento e WHERE e.ID=$examID AND e.IDTipoEvento = t.ID;";
	
	my $queryHandle = $DBIConnection->prepare($typeQuery);
	
	$queryHandle->execute();
	
	my $informations = $queryHandle->fetchrow_arrayref;

	return $$informations[0];

}

1;
