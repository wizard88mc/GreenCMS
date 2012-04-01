#!/usr/bin/perl

use DBI;
use DBD::mysql;
use utf8;
use Time::localtime;

sub retrieveExamsDescription() {

	my $DBIConnection = $_[0];
	
	my $year = localtime->year() + 1900;
	my $month = localtime->mon() + 1;
	my $day = localtime->mday();
	
	if (length($month) == 1) {
		$month = "0$month";
	}
	if (length($day) == 1) {
		$day = "0$day";
	}
	
	my $descriptionQuery = "SELECT DescrizioneEvento FROM Evento WHERE DescrizioneEvento LIKE \"\%[INF]\%\" AND IDTipoEvento <> 27 AND Data >= '$year-$month-$day' GROUP BY DescrizioneEvento ORDER BY DescrizioneEvento ASC";
	
	my $queryHandle = $DBIConnection->prepare($descriptionQuery);
	
	$queryHandle->execute();
	
	return $queryHandle;


}

1;
