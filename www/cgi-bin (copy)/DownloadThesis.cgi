#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use CGI::Session;
use CGI::Cookie;
use XML::LibXML;
use utf8;

require "GlobalVariables.pl";
require "CreateSecondLevelMenu.cgi";
require "WorkWithFiles.pl";

#funziona per stampare la l'elenco per il download delle tesi
sub printFormDownloadThesis() {
	
	#seleziono file delle tesi
	$fileXML .= "Thesis.xml";
	
	my $parser = XML::LibXML->new();
	
	my $document = $parser->parse_file($fileXML) or die "$!";
	my $root = $document->getDocumentElement;
	
	my $thesisList = $root->find("//Thesis");
	
	my $stringThesis;
	
	#per ogni tesi presente
	foreach $thesis ($thesisList->get_nodelist) {
		
		#recupero informazioni
		my $name = $thesis->find('Name')->get_node(1)->firstChild->toString;
		my $surname = $thesis->find('Surname')->get_node(1)->firstChild->toString;
		my $matricola = $thesis->findvalue('Matricola');
		my $title = $thesis->find('Title')->get_node(1)->firstChild->toString;
		my $abstract = $thesis->find('Abstract')->get_node(1)->firstChild->toString;
		my $filename = $thesis->findvalue('FileName');
		my $type = $thesis->findvalue('TipoLaurea');
		
		#costruisco stringa per una tesi e la concateno a quella generale
		my $string = 
		"<h2><a href=\"/" . $folderBase . "private/tesimagistrale/$filename\">$name $surname - $matricola</a></h2>
		<h3>$title</h3>
		<p class=\"withBorderBottom\"><strong>Abstract: </strong>$abstract</p>";
	
		$stringThesis .= $string; 
	}
	
	if (index($stringThesis, "<h2>") == -1) {
		$stringThesis = "<p>Nessuna tesi è stata ancora inserita</p>";
	}
	
	
#stampo parte del contenuto
	my $content = <<CONTENT;
<div id="contents">
	<h1>Download Tesi</h1>
	$stringThesis
</div>
CONTENT

	return $content;
}

$page = new CGI;

$cookie = $page->cookie("CGISESSIONID") || undef;
if (!defined($cookie)) {
	print $page->redirect($siteForCGI . $folderBase . "reservedzone/login.html");
}



my $template = &openFile($siteForCGI . "reservedzone/reservedtemplate.html") or die "$!";

$content = &printFormDownloadThesis();
$secondLevel = &createSecondLevelMenu();

utf8::encode($content);

$content = $secondLevel . $content;
	
$template =~ s/<pageContent\/>/$content/g;
$template =~ s/<pageTitle\/>/Download Tesi/g;
	
print <<CONTENT;
Content-type:text/html\n\n
$template

CONTENT

