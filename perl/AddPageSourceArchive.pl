#!/usr/bin/perl

use XML::LibXML;
use utf8;

binmode STDIN, ":utf8";
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";

require "WorkWithFiles.pl";
require "GlobalVariables.pl";

#aggiunge una pagina di un corso al file xmlSource
#parametri: 
#     $_[0] - nome della pagina da inserire in archivio
#     $_[1] - titolo della pagina
#     $_[2] - stringa dell'anno accademico aaaa/aaaa

sub addPageSourceArchive() {
	
	my $pageName = $_[0];
	my $pageTitle = $_[1];
	my $stringAA = $_[2];
	my $en = $_[3];
	
	#nome della pagina iniziale di archivio
	my $targetPageArchive = "archivio$stringAA" . "$en" . ".html";
	$targetPageArchive =~ s/\///g;
	#prima parte dell'anno accademico (il primo anno) che aggiungo in coda alla pagina di archivio
	$stringAAFirst = substr($stringAA, 0, index($stringAA, "/"));
	
	#prendo file xmlSource della sezione archivio
	my $fileXML = "../pagesSource/archivio/source/xmlSource$en.xml";
	
	my $parser = XML::LibXML->new();
	
	my $document = $parser->parse_file($fileXML);
	my $root = $document->getDocumentElement;
	
	#creo nodo
	my $sourceNode;
	if ($en eq "") {
		$sourceNode = 
		"<pageDetails isStatic=\"T\">
		<metaTags>
			<title>Archivio - $pageTitle</title>
			<description>Pagina di archivio $pageTitle</description>
			<keywords>
				<keyword>archivio</keyword>
				<keyword>$stringAA</keyword>
			</keywords>
		</metaTags>
		<pageTitle>$pageTitle</pageTitle>
		<secondLevelMenuNotSelected />
		<otherParent>Archvio $stringAAFirst/$targetPageArchive</otherParent>
		<contentsPageFileName>$pageName</contentsPageFileName></pageDetails>";
	}
	else {
		$sourceNode = 
		"<pageDetails isStatic=\"T\">
		<metaTags>
			<title>Archive - $pageTitle</title>
			<description>Archive page $pageTitle</description>
			<keywords>
				<keyword>archive</keyword>
				<keyword>$stringAA</keyword>
				<keyword>$pageTitle</keyword>
			</keywords>
		</metaTags>
		<pageTitle>$pageTitle</pageTitle>
		<secondLevelMenuNotSelected />
		<otherParent>Archvio $stringAAFirst/$targetPageArchive</otherParent>
		<contentsPageFileName>$pageName</contentsPageFileName></pageDetails>";
	}
	
	#converto nodo e lo aggiungo
	my $newSource = $parser->parse_balanced_chunk($sourceNode);
	my $tableSource = $root->find("//pagesDetails")->get_node(1);
	$tableSource->appendChild($newSource);
	
	open(FILE, ">$fileXML") || die("Non riesco ad aprire il file");
	print FILE $document->toString();
	close(FILE);
	
	
	
}

1;
