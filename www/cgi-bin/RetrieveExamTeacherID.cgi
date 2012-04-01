#!/usr/bin/perl

use DBI;
use DBD::mysql;
use utf8;

sub retrieveExamTeacherID() {

	my $DBIConnection = $_[0];
	my $examID = $_[0];
	
	my $teacherQuery = "SELECT IDPersona FROM Evento WHERE ID=$examID;";
	
	my $queryHandle = $DBIConnection->prepare($teacherQuery);
	
	$queryHandle->execute();
	
	my $array = $queryHandle->fetchrow_arrayref;
	
	return $$array[0];


}

1;
