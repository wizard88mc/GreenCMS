#!/usr/bin/perl

use DBI;
use DBD::mysql;
use HTML::Entities;
use utf8;

require "ConnectDatabase.pl";
require "WorkWithFiles.pl";
require "GlobalVariables.pl";
require "CreateCourseDetailsPageLaurea.pl";
require "GetCoursesID.pl";
require "GetCourseDescription.pl";
require "GetCourseTeacher.pl";
require "GetCourseCFU.pl";
require "GetCourseTimeInfo.pl";
require "GetCourseHours.pl";
require "GetCourseInformations.pl";

#recupera informazioni per ogni corso, crea la tabella di tutti i corsi della Laurea
sub createPageCoursesLaurea() {

	my @courseNotLink = ("Stage", "Prova finale");

	#creo connessione al database
	my $DBIConnection = &connectDatabase();  

	#parametri per l'esecuzione della query per ottenere gli ID dei corsi della Laurea
	my $descr = "INFORMATICA%";
	my $tipocorso = "L";
	
	#ottengo l'elenco degli ID dei corsi
	my $queryHandle = &getCoursesID($DBIConnection, $tipocorso, $descr);
	
	#inizializzo tabella dei corsi
	my $tableCourses = "
	<table summary=\"Nella tabella vengono presentati i corsi della Laurea, specificando, oltre al nome, 
	il docente titolare del corso ed il periodo di erogazione del corso. Infine per ogni corso e' presente un link alla pagina di dettaglio, con informazioni piu' dettagliate.\">\n";
	$tableCourses .= "<caption>Esami del Corso di Laurea</caption>\n";
	$tableCourses .= 
	"<thead>
		<tr>
		<th id=\"c1\" abbr=\"Corso\" scope=\"col\">Corso</th>
		<th id=\"c2\" abbr=\"Prof\" scope=\"col\">Insegnante</th>
		<th id=\"c3\" abbr=\"Trimestre\" scope=\"col\">Trimestre</th>
		<th id=\"c4\" abbr=\"Anno\" scope=\"col\">Anno</th>
		</tr>
	</thead>
	<tbody>";
	
	my $i = 0;
	
	#per ogni ID di corso che mi viene restituito dalla query
	while (my $course = $queryHandle->fetchrow_hashref()) {   
		
		#prendo l'id del corso che considero
		my $courseID = $course->{'id'};
		
		#hash dove mettero' tutte le informazioni del corso
		my %courseDetails = (); 
		
		#riempio l'hash
		$courseDetails{"teachingName"} = &getCourseDescription($DBIConnection, $courseID);
		$courseDetails{"teacher"} = &getCourseTeacher($DBIConnection, $courseID);
		$courseDetails{"CFU"} = &getCourseCFU($DBIConnection, $courseID);
		$courseDetails{"period"} = &getTimeInfo($DBIConnection, $courseID);
		$courseDetails{"hours"} = &getCourseHours($DBIConnection, $courseID);
		$courseDetails{"informations"} = &getInformationsCourse($DBIConnection, $courseID, 1);
		
		#recupero trimestre e anno del corso
		my %periodInformations = %{$courseDetails{"period"}};
		my $period = $periodInformations{"trimestre"}; 
		my $year = $periodInformations{"anno"};
		
		#creo pagina del corso, mi viene restituito il nome del file a cui far linkare il collegamento
		my $linkFileName = &createCourseDetailsPageLaurea(\%courseDetails); 

		my $notToLink = 0;
		foreach my $course (@courseNotLink) {
			if ($courseDetails{"teachingName"} eq $course) {
				$notToLink = 1;
			}
		}
		
		my $stringEntry;

		#se modulo due di i è != 0 metto classe alternate per alternare barre con sfondo
		if ($i % 2 == 0) {
			$stringEntry = "
			<tr>";
		}
		else {
			$stringEntry = "
			<tr class=\"alternate\">";
		}
		
		#se non ha link scrivo semplice nome, altrimenti aggiungo link
		if ($notToLink) {
			$stringEntry .= "
			<td headers=\"c1\">$courseDetails{'teachingName'}</td>";
		}
		else {
		$stringEntry .= "
			<td headers=\"c1\"><a href=\"$linkFileName\">" . $courseDetails{"teachingName"} . "</a></td>";
		}

		#recupero titolo del professore e aggiungo <abbr>
		my $tytle = substr($courseDetails{"teacher"}, 0, index($courseDetails{"teacher"}, " "));
		if ($tytle eq "Prof.") {
			$tytle = "<abbr title=\"Professor\">$tytle</abbr>";
		}
		if ($tytle eq "Prof.ssa") {
			$tytle = "<abbr title=\"Professoressa\">$tytle</abbr>";
		}
		if ($tytle eq "Dott.") {
			$tytle = "<abbr title=\"Dottor\">$tytle</abbr>";
		}
		if ($tytle eq "Dott.ssa") {
			$tytle = "<abbr title=\"Dottoressa\">$tytle</abbr>";
		}
		my $teacher = $tytle . substr($courseDetails{"teacher"}, index($courseDetails{"teacher"}, " "));

		#aggiungo professore e periodo di svolgimento
		$stringEntry .= "
			<td headers=\"c2\">" . $teacher . "</td>";
		$stringEntry .= "
			<td headers=\"c3\">$period</td><td headers=\"c4\">$year</td>";
		
		$stringEntry .= "
		</tr>\n";
		
		#aggiungo alla tabella in costruzione la nuova riga
		$tableCourses .= $stringEntry;  

		$i = $i + 1; 
		
	}
	
	#chiudo tabella creata
	$tableCourses .= "
	</tbody>
	</table>";
	
	utf8::encode($tableCourses);
	
	#mi disconnetto dal database
	$DBIConnection->disconnect();  
	
	my $pageCoursesLaurea = &openFile($sitePath . "laurea/corsilaurea.html") or die "$!"; 
	#sostituisco, nella pagina corsilaurea.html, il tag <courseTable/> la tabella appena creata
	$pageCoursesLaurea =~ s/<courseTable\/>/$tableCourses/; 
	
	#creo il nuovo file
	&createFile($sitePath . "laurea/corsilaurea.html", $pageCoursesLaurea);  
	

}

1;
