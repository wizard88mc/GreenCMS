#!/usr/bin/perl

use Time::localtime;
use XML::LibXML;
use utf8;

require "GlobalVariables.pl";
require "ExtractXML.pl";
require "GlobalFunctions.pl";

#recupera i seminari svolti in un anno accademico
sub archiveSeminars() {
	
	#file xml contenente i seminari
	my $seminarsXML = $sitePath . "xml_files/EventMailingListContact.xml";
	
	my $root = &extractXML($seminarsXML);
	
	my $seminarsList = $root->find("//TableEvents/Event");
	
	#una stringa per la versione italiana e una per l'inglese
	my $stringSeminars = "<ul>";
	my $stringSeminarsEn = "<ul>";
	
	foreach $seminar ($seminarsList->get_nodelist) {
		
		#recupero la lingua delle informazioni inserite
		my $language = $seminar->findvalue('@language');
		my $title = $seminar->find('Title')->get_node(1)->firstChild->toString;
		my $date = $seminar->findvalue('Date');
		my $dateIt = &convertDateFromDBToItalian($date);
		my $speaker = $seminar->find('Speaker')->get_node(1)->firstChild->toString;
		my $from = "";
		#se affiliazione è stata inserita allora recupero anche affiliazione
		if ($seminar->findvalue('From') ne "") {
			$from = $seminar->find('From')->get_node(1)->firstChild->toString;
		}
		my $abstract = $seminar->find('Abstract')->get_node(1)->firstChild->toString;
		
		#sostituisco eventuali link inseriti nell'abstract in link veri e propri, con tag <a>
		
		$abstract = &convertLinks($abstract);
		
		my $titleIT = "<strong>$title</strong>";
		my $abstractIT = $abstract;
		
		if ($language eq "en") {
			$titleIT = "<strong xml:lang=\"en\">$title</strong>";
			$abstractIT = "<span xml:lang=\"en\">$abstract</span>";
		}
		
		#se c'è affiliazione del relatore la aggiungo
		if ($from ne "") {
			$from = "<strong>($from)</strong>";
		}
		
		#creo stringa del seminario
		my $stringSeminar ="<li>$titleIT - il giorno $dateIt - $speaker  $from	<p><strong xml:lang=\"en\">Abstract: </strong>$abstractIT</p></li>";
		
		if ($language eq "it") {
			$title = "<strong xml:lang=\"it\">$title</strong>";
			$abstract = "<span xml:lang=\"it\">$abstract</span>";
		}
		
		my $stringSeminarEn = "<li>$title - $date - $speaker  $from	<p><strong xml:lang=\"en\">Abstract: </strong>$abstract</p></li>";
		
		$stringSeminars .= $stringSeminar;
		
		$stringSeminarsEn .= $stringSeminarEn;
		
	}
	
	$stringSeminars .= "</ul>";
	$stringSeminarsEn .= "</ul>";
	
	if (index($stringSeminars, "<li>") == -1) {
		$stringSeminars = "<em>Non sono stati tenuti seminari per questo A.A.</em>";
		$stringSeminarsEn = "<em>No seminars inserted for this year</em>";
	}
	
	utf8::encode($stringSeminars);
	utf8::encode($stringSeminarsEn);
	
	return ($stringSeminars, $stringSeminarsEn);
	
	
}
