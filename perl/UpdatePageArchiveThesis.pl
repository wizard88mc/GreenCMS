#!/usr/bin/perl

use XML::LibXML;
use utf8;

require "ExtractXML.pl";

sub updatePageArchiveThesis() {

	my $fileXML = $sitePath . "xml_files/ArchiveThesis.xml";
	
	my $root = &extractXML($fileXML);

	my @monthIt = ("Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre");
	my @monthEn = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December");

	my $periodList = $root->find("//TableArchiveThesis/ArchiveThesis");
	
	my $stringIt = "";
	my $stringEn = "";
	
	foreach my $period ($periodList->get_nodelist) {
	
		my $month = $period->findvalue('@MonthSession');
		my $year = $period->findvalue('@Year');
		
		my $thesisList = $period->find('Thesis');
		
		$stringIt .= "<h3>$monthIt[$month - 1] $year</h3>";
		$stringEn .= "<h3>$monthEn[$month - 1] $year</h3>";
		
		foreach my $thesis ($thesisList->get_nodelist) {
			my $name = $thesis->find('Name')->get_node(1)->firstChild->toString;
			my $surname = $thesis->find('Surname')->get_node(1)->firstChild->toString;
			my $abstract = $thesis->find('Abstract')->get_node(1)->firstChild->toString;
			my $title = $thesis->find('Title')->get_node(1)->firstChild->toString;
			my $relatore = $thesis->findvalue('Relatore');
			my $matricola = $thesis->findvalue('Matricola');
			my $lang = $thesis->findvalue('@lang');
			
			if ($lang eq "it") {
			
				$stringIt .= "<h4>$title - $name $surname - $matricola - Relatore: $relatore</h4><p class=\"withBorderBottom\">$abstract</p>";
				$stringEn .= "<h4 xml:lang=\"it\">$title - $name $surname - $matricola - Relatore: $relatore</h4><p class=\"withBorderBottom\" xml:lang=\"it\">$abstract</p>";
			}
			else {
				$stringIt .= "<h4><span xml:lang=\"en\">$title</span> - $name $surname - $matricola - Relatore: $relatore</h4><p class=\"withBorderBottom\" xml:lang=\"en\">$abstract</p>";
				$stringEn .= "<h4>$title - <span xml:lang=\"it\">$name $surname - $matricola</span> - Supervisor: $relatore</h4><p class=\"withBorderBottom\">$abstract</p>";
			}
		}
	
	}
	
	utf8::encode($stringIt);
	utf8::encode($stringEn);
	
	if (index($stringIt, '<h3>') != -1) {

		my $pageArchiveIt = &openFile($sitePath . "laureamagistrale/archiviotesi.html");
		my $pageArchiveEn = &openFile($sitePath . "laureamagistrale/archiviotesien.html");
		
		
		my $startPIt = index($pageArchiveIt, "<p id=\"notPresent\">");
		my $endPIt = index($pageArchiveIt, "</p>", $startPIt);
		
		substr($pageArchiveIt, $startPIt, $endPIt + length("</p>") - $startPIt, $stringIt); 
		
		my $startPEn = index($pageArchiveEn, "<p id=\"notPresent\">");
		my $endPEn = index($pageArchiveEn, "</p>", $startPEn);
		
		substr($pageArchiveEn, $startPEn, $endPEn + length("</p>") - $startPEn, $stringEn); 
		
		&createFile($sitePath . "laureamagistrale/archiviotesi.html", $pageArchiveIt);
		&createFile($sitePath . "laureamagistrale/archiviotesien.html", $pageArchiveEn);

	}

}

1;