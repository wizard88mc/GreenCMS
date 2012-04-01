#!/usr/bin/perl

use DBI;
use DBD::mysql;
use utf8;

sub retrieveExamsIDs() {

	my $DBIConnection = $_[0];
	my $eventDescription = $_[1];
	
	my $year = localtime->year() + 1900;
	my $month = localtime->mon() + 1;
	my $day = localtime->mday();
	
	if (length($month) == 1) {
		$month = "0$month";
	}
	if (length($day) == 1) {
		$day = "0$day";
	}

	my $examsQuery = "SELECT ID FROM Evento WHERE DescrizioneEvento = \"$eventDescription\" AND Data >= '$year-$month-$day' ORDER BY Data ASC;";
	
	my $queryHandle = $DBIConnection->prepare($examsQuery);
	
	$queryHandle->execute();
	
	#restituisce il risultato che è l'elenco degli ID degli eventi che hanno come DescrizioneEvento quel particolare esame
	return $queryHandle;


}

1;
