#!/usr/bin/perl

use XML::LibXML;
use utf8;

require "WorkWithFiles.pl";
require "GlobalVariables.pl";
require "ConnectDatabase.pl";
require "RetrieveExamsDescription.cgi";
require "RetrieveExamsIDs.cgi";
require "RetrieveExamInformations.cgi";
require "RetrieveTeacherExam.cgi";
require "RetrieveExamType.cgi";
require "RetrieveExamSource.cgi";

#CGI per la stampa dell'elenco degli esami per la laurea, richiamato quando javascript non è attivo

{

	#prendo file html degli esami
	my $pageExams = &openFile($siteForCGI . "laurea/esamilaurea.html");
	
	#mi connetto al database
	my $DBIConnection = &connectDatabase("booking");

	#recupero le descrizioni degli esami di informatica
	my $descriptionList = &retrieveExamsDescription($DBIConnection);
	
	
	my $completeList = "<p>ATTENZIONE: sono presenti tutti gli esami, sia per la Laurea che per la Laurea Magistrale</p>
	<ul>";
	
	#fintantochè ho una descrizione diversa nell'elenco
	while (my $description = $descriptionList->fetchrow_arrayref()) {
		
		#prendo la descrizione in forma testuale e me la salvo come del file
		my $examName = $$description[0];
		#elimino [INF] presente nella descizione
		$examName =~ s/\[INF\]//g;
		
		#aggiungo elemento al menu
		my $examDefinition = "<li><strong>$examName</strong>";
		
		#recupero gli ID degli eventi degli esami che hanno quella determinata descrizione
		#si suppone per esame uguale stessa descrizione
		my $examsIDList = &retrieveExamsIDs($DBIConnection, $$description[0]);
		
		my $subList = "<ul>";
		
		#fintantochè ho un evento per quella descrizione
		while (my $examIDRow = $examsIDList->fetchrow_arrayref()) {
			
			#recupero ID dell'esame (evento)
			my $examID = $$examIDRow[0];
			
			#recupero informazioni generali (data, ora di inizio, ora di fine)
			my $examInformations = &retrieveExamInformations($DBIConnection, $examID);
			my $date = $examInformations->{'Data'};
			my $bTime = $examInformations->{'OraInizio'};
			my $eTime = $examInformations->{'OraFine'};
			
			#recupero nome del docente titolare dell'evento(esame)
			my $teacher = &retrieveTeacherExam($DBIConnection, $examID);
			
			#recupero descrizione ("necessaria iscrizione...")
			my $description = &retrieveExamType($DBIConnection, $examID);
			
			#recupero nome della risorsa adibita all'esame
			my $sourceHASH = &retrieveExamSource($DBIConnection, $examID);
			my $source = $sourceHASH->{'Nome'};
			
			#costruisco stringa dell'elenco
			my $stringExam = "
		<li>$description - $date, $bTime &rarr; $eTime, <strong>$source</strong> - $teacher</li>";
			
			#concateno <li> all'<ul> di tutti gli eventi per quell'esame 
			$subList .= $stringExam;
		}
		
		#chiudo elenco ed elemento <li>
		$subList .= "</ul></li>";
		
		#concateno alla stringa generale
		$examDefinition .= $subList;
		
		$completeList .= $examDefinition;
	}
	
	$completeList .= "</ul>";
	
	$DBIConnection->disconnect();
	
	utf8::encode($completeList);

	#variabili necessarie per il cambio di indirizzi nella pagina
	my $srcPath = "src=\"../";
	my $hrefPath = "href=\"../";
	my $newSRC = "src=\"/$folderBase";
	my $newHREF = "href=\"/$folderBase";
	my $folder = "laurea/";
	
	my $ulSecond = index($pageExams, "div id=\"contents");
	my $endSecond = index($pageExams, "/ul", $ulSecond);
	my $href = index($pageExams, "href=\"", $ulSecond);
	
	
	while ($href != -1 && $href < $endSecond) {
		
		my $endLink = index($pageExams, "\"", $href + length("href=\""));
		my $link = substr($pageExams, $href, $endLink - $href);
		if (index($link, '.cgi') == -1) {
			substr($pageExams, $href, length("href=\""), "href=\"/$folderBase" . $folder);
		}
		
		$href = index($pageExams, "href=\"", $href + length("href=\"") + 5);
		
	}
	
	$pageExams =~ s/$srcPath/$newSRC/g; 
	$pageExams =~ s/$hrefPath/$newHREF/g;
	
	#sotituisco il tag <noscript> presente nella pagina esamilaurea con l'elenco degli esami appena creato
	substr($pageExams, index($pageExams, "<noscript>"), index($pageExams, "</noscript>") + length("</noscript>") - index($pageExams, "<noscript>"), $completeList);
		
	#elimino immagine preloader
	substr($pageExams, index($pageExams, "<img", index($pageExams, "contentsLong")), index($pageExams, "/>", index($pageExams, "<img")) - index($pageExams, "<img"), "");
	
	$pageExams =~ s/esamilaureaen.html/EsamiLaureaen.cgi/g;
	
#stampo pagina
print "Content-type:text/html\n\n";
print "$pageExams";
	
	

}
