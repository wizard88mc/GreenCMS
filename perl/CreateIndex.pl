#!/usr/bin/perl

use utf8;
use XML::LibXML;

require "ExtractXML.pl";
require "CreateSinglePage.pl";
require "WorkWithFiles.pl";
require "GlobalVariables.pl";

#generazione di tutte le pagine che saranno inserite nella root del sito
sub createIndex() {
	
	#prendo informazioni da xmlSource
	my $xmlFile = &extractXML("../pagesSource/index/source/xmlSource.xml"); #estraggo informazioni riguardo l'home page
	
	my $xmlFileEn = &extractXML("../pagesSource/index/source/xmlSourceen.xml");
	
	my $pageDetailsNodes = $xmlFile->findnodes('pageDetails');
	
	foreach my $pageDetails ($pageDetailsNodes->get_nodelist) {  #pageDetails e' un nodo XML con tutte le informazioni della pagina
		
		#invoco funzione per creare una singola pagina
		my $pageCreated = &createSinglePage("home", $pageDetails, "../pagesSource/index/source", 1);
		
		my $pageName = $pageDetails->findvalue('contentsPageFileName');  #prendo il nome del file che andra' generato
		
		#link alla pagine in inglese
		my $otherPage = "$pageName";
		$otherPage =~ s/.html/en.html/g;
		
		$pageCreated =~ s/<linkOtherLanguage\/>/$otherPage/g;
		
		my $completePath = $sitePath . $pageName;  #creo il path completo per la creazione del file
	
		&createFile($completePath, $pageCreated);
		
		print "Page created: $pageName \n";
		
	}
	
	my $pageDetailsNodeEn = $xmlFileEn->findnodes('pageDetails');
	
	#ripeto le stesse operazioni per la versione inglese
	foreach my $pageDetails ($pageDetailsNodeEn->get_nodelist) {
		
		my $pageCreated = &createSinglePage("home", $pageDetails, "../pagesSource/index/source", 1, "", "en");
		
		$pageName = $pageDetails->findvalue('contentsPageFileName');  #prendo il nome del file che andra' generato
		
		my $otherPage = "$pageName";
		$otherPage =~ s/en.html/.html/g;
		
		$pageCreated =~ s/<linkOtherLanguage\/>/$otherPage/g;
		
		my $completePath = $sitePath . $pageName;  #creo il path completo per la creazione del file
	
		&createFile($completePath, $pageCreated);
		
		print "Page created: $pageName \n";
		
	}
				
}

1;
