#!/usr/bin/perl

#recupera gli esami, invocato tramite metodo ajax

print "Content-typ:text/html\n\n";

use DBI;
use DBD::mysql;
use utf8;

binmode STDIN, ":utf8";
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";

require "ConnectDatabase.pl";
require "RetrieveExamsDescription.cgi";
require "RetrieveExamsIDs.cgi";
require "RetrieveExamInformations.cgi";
require "RetrieveTeacherExam.cgi";
require "RetrieveExamType.cgi";
require "RetrieveExamSource.cgi";

eval {
#collego al database bookin
my $DBIConnection = &connectDatabase("booking");

#recupero le descrizioni degli esami di informatica
my $descriptionList = &retrieveExamsDescription($DBIConnection);

my $completeList = "";

#per ogni descrizione presente
while (my $description = $descriptionList->fetchrow_arrayref()) {
	
	#prendo descrizione ed elimino [INF] per avere nome
	my $examName = $$description[0];
	$examName =~ s/\[INF\]//g;
	
	#aggiungo <li> per quell'esame
	my $examDefinition = "<li><strong>$examName</strong>";
	
	#recupero gli ID degli eventi associati a quegli esami
	my $examsIDList = &retrieveExamsIDs($DBIConnection, $$description[0]);
	
	#elenco di secondo livello per 
	my $subList = "<ul>";
	
	while (my $examIDRow = $examsIDList->fetchrow_arrayref()) {
		
		my $examID = $$examIDRow[0];
		
		my $examInformations = &retrieveExamInformations($DBIConnection, $examID);
		my $date = $examInformations->{'Data'};
		my $bTime = $examInformations->{'OraInizio'};
		my $eTime = $examInformations->{'OraFine'};
		
		my $teacher = &retrieveTeacherExam($DBIConnection, $examID);
		
		my $description = &retrieveExamType($DBIConnection, $examID);
		
		my $sourceHASH = &retrieveExamSource($DBIConnection, $examID);
		my $source = $sourceHASH->{'Nome'};
		
		my $stringExam = "
	<li>$description - $date, $bTime &rarr; $eTime, <strong>$source</strong> - $teacher</li>";
		
		$subList .= $stringExam;
	}
	
	$subList .= "</ul></li>";
	
	$examDefinition .= $subList;
	
	$completeList .= $examDefinition;
}

$DBIConnection->disconnect();

print "$completeList";
}
or do {
	$completeList = "<ul><li>DB non raggiungibile. Problemi Tecnici. Ci scusiamo per il disagio. </li></ul>";
	
	print "$completeList";
}

