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
#    $_[1] - ID del corso di cui voglio sapere il professore

sub getCourseTeacher() {

	my $DBIConnection = $_[0];
	my $courseID = $_[1];
	
	my $teacherQuery = &openFile("queries/GetTeacher.sql");
	$teacherQuery =~ s/<afId>/$courseID/g;  #sostituisco al tag fittizion afId l'ID del corso
	
	my $queryHandle = $DBIConnection->prepare($teacherQuery);
	$queryHandle->execute();

	my $teacherHASH = $queryHandle->fetchrow_hashref();
	
	my $teacherName = $teacherHASH->{'nome'};  #prendo il nome del professore
	$teacherName =~ s/(\w+)/\u\L$1/g; 
	
	my $teacherSurname = $teacherHASH->{'cognome'};  #prendo cognome professore
	$teacherSurname =~ s/(\w+)/\u\L$1/g; 
	
	return $teacherHASH->{'titolo_id'} . " " . $teacherName . " " . $teacherSurname;

}


1;
