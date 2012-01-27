#!/usr/bin/perl

use XML::LibXML;
use utf8;

binmode STDIN, ":utf8";
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";

#aggiunge un nuovo anno all'archivio, al momento della generazione del sito per il nuovo AA
sub addYearArchive() {
	
	#stringa dell'anno, inteso come aaaa/aaaa
	my $stringAA = $_[0];
	#discriminante italiano-inglese
	my $en = $_[1];
	
	#file con il menu di secondo livello
	my $secondLevelXML = "../pagesSource/archivio/source/secondLevelMenu$en.xml";
	
	#file xmlSource
	my $xmlSource = "../pagesSource/archivio/source/xmlSource$en.xml";
	
	my $parser = XML::LibXML->new();
	
	my $documentSecondLevel = $parser->parse_file($secondLevelXML);
	my $rootSecondLevel = $documentSecondLevel->getDocumentElement;
	
	my $documentSource = $parser->parse_file($xmlSource);
	my $rootSource = $documentSource->getDocumentElement;
	
	#nome della pagina iniziale di archivio, a cui poi elimino /
	my $pageName = "archivio$stringAA" . $en . ".html";
	$pageName =~ s/\///g;
	
	#nodo per il menu di secondo livello
	my $secondLevelNode = 
	"<secondLevelMenuEntry>
	<linkMenuEntryText>$stringAA</linkMenuEntryText>
	<linkMenuEntryName>$stringAA</linkMenuEntryName>
	<linkMenuEntryPageTarget>$pageName</linkMenuEntryPageTarget>
	<linkMenuEntryAlt>$stringAA</linkMenuEntryAlt></secondLevelMenuEntry>";
	
	#aggiungo il nuovo nodo in testa al file
	my $newNode = $parser->parse_balanced_chunk($secondLevelNode);
	my $tableSecond = $rootSecondLevel->find("//secondLevelMenu")->get_node(1);
	my $firstNode = $tableSecond->find("secondLevelMenuEntry[1]")->get_node(1);
	
	$tableSecond->insertBefore($newNode, $firstNode);
	
	open(FILE, ">$secondLevelXML") || die("Non riesco ad aprire il file");
	print FILE $documentSecondLevel->toString();
	close(FILE);
	
	my $sourceNode;
	
	#nodo per il file xmlSource
	if ($en eq "") {
		$sourceNode = 
		"<pageDetails isStatic=\"T\">
		<metaTags>
			<title>Archivio $stringAA</title>
			<description>Pagina iniziale archivio $stringAA</description>
			<keywords>
				<keyword>archivio</keyword>
				<keyword>$stringAA</keyword>
			</keywords>
		</metaTags>
		<pageTitle>Archivio $stringAA</pageTitle>
		<secondLevelMenuNotSelected>$stringAA</secondLevelMenuNotSelected>
		<contentsPageFileName>$pageName</contentsPageFileName></pageDetails>";
	}
	else {
		$sourceNode = 
		"<pageDetails isStatic=\"T\">
		<metaTags>
			<title>Archive $stringAA</title>
			<description>Initial page archive $stringAA</description>
			<keywords>
				<keyword>archive</keyword>
				<keyword>$stringAA</keyword>
			</keywords>
		</metaTags>
		<pageTitle>archive $stringAA</pageTitle>
		<secondLevelMenuNotSelected>$stringAA</secondLevelMenuNotSelected>
		<contentsPageFileName>$pageName</contentsPageFileName></pageDetails>";
		
	}
	#converto ed inserisco nel file
	my $newSource = $parser->parse_balanced_chunk($sourceNode);
	my $tableSource = $rootSource->find("//pagesDetails")->get_node(1);
	$tableSource->appendChild($newSource);
	
	
	open(FILE, ">$xmlSource") || die("Non riesco ad aprire il file");
	print FILE $documentSource->toString();
	close(FILE);
	
	
}

1;
