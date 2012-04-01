#!/usr/bin/perl

use utf8;

binmode STDIN, ":utf8";
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";

require "WorkWithFiles.pl";
require "GlobalVariables.pl";
require "CreatePageArchiveCourse.pl";
require "AddPageSourceArchive.pl";

sub extractCourses() {
	
	my $stringAA = $_[0];
	my $en = $_[1];
	
	#recupero i corsi per la laurea
	my $coursePage = &openFile($sitePath . "laurea/corsilaurea$en.html");
	
	my $listLaurea = "<ul>";
	
	my $offset = index($coursePage, "<tbody>");
	
	#recupero posizione della prima riga contenente un corso
	my $trPosition = index($coursePage, "<tr", $offset);
	
	#fino a quando non finiscono le righe che contengono un corso
	while ($trPosition != -1) {
		
		#recupero l'indice dove finisce la riga che contiene il corso
		my $endTr = index($coursePage, "</tr>", $trPosition);
		
		#prendo la riga selezionata come sottostringa
		my $substringRow = substr($coursePage, $trPosition, $endTr - $trPosition);
		
		#recupero il link che contiene la pagina del corso ed il suo nome
		my $stringInformations = substr($substringRow, index($substringRow, "<a"), index($substringRow, "</a>") - index($substringRow, "<a"));
		
		#recupero il nome del corso, compreso tra "> e </a>
		my $courseName = substr($stringInformations, index($stringInformations, "\">") + 2);
		
		if ($courseName ne "") {
			
			#recupero nome della pagina che contiene le informazioni del corso (posizione di ef=" + 4 (arrivo all'inizio del nome) -> posizione di "> (fine link)
			my $pageLinkStart = index($stringInformations, "ef=\"") + 4;
			
			my $pageName = substr($stringInformations, $pageLinkStart, index($stringInformations, ".html\"") + 5 - $pageLinkStart);
			
			print "$pageName\n";
			my $startCellName = index($substringRow, "<td>", index($substringRow, "<td>" + 2));
			
			my $startName = index($substringRow, "<abbr", $startCellName);
			
			my $stringTeacherName = substr($substringRow, $startName, index($substringRow, "</td>", $startName) - $startName);
			
			my $finalPageName = &createPageArchiveCourse($pageName, $stringAA, "laurea", $en);
			
			&addPageSourceArchive($finalPageName, $courseName . " - $stringAA", $stringAA, $en);
			
			my $link = "<li><a href=\"$finalPageName\">$courseName</a> - $stringTeacherName</li>";
			
			$listLaurea .= $link;
		}
		$trPosition = index($coursePage, "<tr", $trPosition + 5);
	}
	
	$listLaurea .= "</ul>";
	
	#comincio con i corsi della magistrale, e applico stesso principio di prima
	$coursePage = &openFile($sitePath . "laureamagistrale/corsimagistrale$en.html");
	my $listMagistrale = "<ul>";
	
	$offset = index($coursePage, "<tbody>");
	
	#recupero posizione della prima riga contenente un corso
	$trPosition = index($coursePage, "<tr", $offset);
	
	#fino a quando non finiscono le righe che contengono un corso
	while ($trPosition != -1) {
		
		#recupero l'indice dove finisce la riga che contiene il corso
		my $endTr = index($coursePage, "</tr>", $trPosition);
		
		#prendo la riga selezionata come sottostringa
		my $substringRow = substr($coursePage, $trPosition, $endTr - $trPosition);

		#recupero il link che contiene la pagina del corso ed il suo nome
		my $stringInformations = substr($substringRow, index($substringRow, "<a"), index($substringRow, "</a>") - index($substringRow, "<a"));
		
		#recupero il nome del corso, compreso tra "> e </a>
		my $courseName = substr($stringInformations, index($stringInformations, "\">") + 2);
		
		if ($courseName ne "") {
			
			#recupero nome della pagina che contiene le informazioni del corso (posizione di ef=" + 4 (arrivo all'inizio del nome) -> posizione di "> (fine link)
			my $pageLinkStart = index($stringInformations, "ef=\"") + 4;
			
			my $pageName = substr($stringInformations, $pageLinkStart, index($stringInformations, ".html\"") + 5 - $pageLinkStart);
			print "$pageName\n";
			my $startCellName = index($substringRow, "<td>", index($substringRow, "<td>" + 2));
			
			my $startName = index($substringRow, "<abbr", $startCellName);
			
			my $stringTeacherName = substr($substringRow, $startName, index($substringRow, "</td>", $startName) - $startName);
			
			my $finalPageName = &createPageArchiveCourse($pageName, $stringAA, "laureamagistrale", $en);
			
			&addPageSourceArchive($finalPageName, $courseName . " - $stringAA", $stringAA, $en);
			
			my $link = "<li><a href=\"$finalPageName\">$courseName</a> - $stringTeacherName</li>";
			
			$listMagistrale .= $link;
		}
		$trPosition = index($coursePage, "<tr", $trPosition + 5);
	}
	
	$listMagistrale .= "</ul>";
	
	my @results = ($listLaurea, $listMagistrale);
	
	return @results;
	
}

1;
