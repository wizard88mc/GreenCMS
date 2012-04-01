#!/usr/bin/perl

use XML::LibXML;
use utf8;

require "GlobalVariables.pl";
require "WorkWithFiles.pl";

{

	#prendo file html dei seminari
	my $pageSeminars = &openFile($siteForCGI . "news/seminari.html"); 
	
	#prendo file XML contenente i seminari
	my $seminarsXML = $fileXML . "EventMailingListContact.xml";

	my $parser = XML::LibXML->new();
	
	my $document = $parser->parse_file($seminarsXML);
	my $root = $document->getDocumentElement;

	my $seminarsList = $root->find("//TableEvents/Event");

	my $stringSeminars =  "";

	#per ogni seminario presente
	foreach my $seminar ($seminarsList->get_nodelist)  {

		#recupero informazioni
		my $language = $seminar->findvalue('@language');
		my $title = $seminar->find('Title')->get_node(1)->firstChild->toString;
		my $date = $seminar->findvalue('Date');
		$date = substr($date, 8, 2) . "/" . substr($date, 5, 2) . "/" . substr($date, 0, 4);
		my $time = $seminar->findvalue('Time');
		$time = substr($time, 0, 5);
		my $place = $seminar->find('Place')->get_node(1)->firstChild->toString;
		my $speaker = $seminar->find('Speaker')->get_node(1)->firstChild->toString;
		my $from = "";
		if ($seminar->findvalue('From') ne "") {
			$from = $seminar->find('From')->get_node(1)->firstChild->toString;
		}
		my $speakerCV = " - - - ";
		if ($seminar->findvalue('SpeakerCV') ne "") {
			$speakerCV = $seminar->find('SpeakerCV')->get_node(1)->firstChild->toString;
		}
		my $abstract = " - - - ";
		if ($seminar->findvalue('Abstract') ne "") {
			$abstract = $seminar->find('Abstract')->get_node(1)->firstChild->toString;
		}
		
		#verifico se all'interno dell'abstract è stato inserito un link
		my $positionLink = index($abstract, "http://");
		
		while ($positionLink != -1) {
		
			my $endLink = index($abstract, " ", $positionLink);

			my $link = substr($abstract, $positionLink, $endLink - $positionLink);
			
			$link = "<a href=\"$link\">$link</a>";
			my $lengthLink = length($link);
		
			substr($abstract, $positionLink, $endLink - $positionLink, $link);
			
			$positionLink = index($abstract, "http://", $positionLink + $lengthLink);
			
		}

		#se la lingua specificata Ã¨ l'inglese, aggiungo xml:lang ai tag testuali
		if ($language eq "en") {
			$title = "<h3 xml:lang=\"en\">$title</h3>";
			$abstract = "<span xml:lang=\"en\">$abstract</span>";
			$speakerCV = "<span xml:lang=\"en\">$speakerCV</span>";
		}
		else {
			$title = "<h3>$title</h3>";
		}
		
		#se c'Ã¨ affiliazione del relatore la aggiungo
		if ($from ne "") {
			$from = "<strong>($from)</strong>";
		}
		
		#creo stringa del seminario
		my $seminarString =
		"$title
		<p><strong>Dove / Data e Ora: </strong> $place, il giorno $date alle ore $time</p>
		<p><strong>Relatore: </strong>$speaker  $from</p>
		<p><strong xml:lang=\"en\">Abstract: </strong>$abstract</p>
		<p><strong> CV Relatore: </strong>$speakerCV</p>
		<p class=\"tornaSu withBorderBottom\"><a href=\"#contentsLong\">Torna su &#9650;</a></p>";
		
		$stringSeminars .= $seminarString;
	
	}
	
	if (index($stringSeminars, "</h3>") == -1) {
		$stringSeminars = "<p><em>Nessun seminario inserito</em></p>";
	}
	
	utf8::encode($stringSeminars);
	
	#link da sostituire
	my $srcPath = "src=\"../";
	my $hrefPath = "href=\"../";
	my $newSRC = "src=\"/$folderBase";
	my $newHREF = "href=\"/$folderBase";
	my $folder = "news/";
	
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
	
	
	$pageSeminars =~ s/$srcPath/$newSRC/g; 
	$pageSeminars =~ s/$hrefPath/$newHREF/g;
	$pageSeminars =~ s/<seminarsList\/>/$stringSeminars/g;
	
	$pageSeminars =~ s/seminarien.html/Seminarien.cgi/g;
	
print <<PAGE;
Content-type: text/html\n\n
$pageSeminars

PAGE
}
