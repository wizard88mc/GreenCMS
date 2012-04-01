#!/usr/bin/perl

use XML::LibXML;
use utf8;

require "GlobalVariables.pl";
require "WorkWithFiles.pl";

{
	
	my $pageDocuments = &openFile($siteForCGI . "documenti/documenti.html");	
	
	my $parser = XML::LibXML->new();
	
	my $documentXML = $fileXML . "Document.xml";
	
	my $document = $parser->parse_file($documentXML);
	my $root = $document->getDocumentElement;
	
	my $documentsList = $root->find("//TableDocument/Document");
	
	my $documentHTML = "<ol>";
	
	foreach my $document ($documentsList->get_nodelist) {
		
		my $documentName = $document->findvalue('Name');
		my $fileName = $document->findvalue('FileName');
		
		$documentHTML .= "<li><a href=\"/" . $folderBase . "documenti/$fileName\">$documentName</a></li>";
		
	}
	
	$documentHTML .= "</ol>";
	
	if (index($documentHTML, "<li>") == -1) {
		$documentHTML = "<p><em>Nessun documento ancora inserito</em></p>";
	}
	
	utf8::encode($documentHTML);
	
	my $srcPath = "src=\"../";
	my $hrefPath = "href=\"../";
	my $newSRC = "src=\"/$folderBase";
	my $newHREF = "href=\"/$folderBase";
	
	$pageDocuments =~ s/$srcPath/$newSRC/g; 
	$pageDocuments =~ s/$hrefPath/$newHREF/g;
	
	$pageDocuments =~ s/<listDocuments\/>/$documentHTML/g;
	
	$pageDocuments =~ s/documentien.html/Documentien.cgi/g;
	
print <<PAGE;
Content-type: text/html\n\n
$pageDocuments

PAGE
}
