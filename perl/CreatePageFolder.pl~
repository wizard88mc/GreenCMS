#!/usr/bin/perl

use utf8;

require "ExtractXML.pl";
require "CreateSinglePage.pl";

#parametri:
#    $_[0] - nome della cartella dove creare le pagine
#    $_[1] - se vogliamo versione inglese o italiana

sub createPagesOfFolder() {
	
	my $folderName = $_[0];
	my $en = $_[1];
	
	#path dove sono collocati i file con il contenuto che andra' inserito nel file html
	my $sourcePath = "../pagesSource/$folderName/source";
	#path della cartella dove verranno creati i file html
	my $outputPath = $sitePath . "$folderName";   
	
	
	#leggo file xml per estrapolare le informazioni delle pagine
	my $xmlFile = &extractXML("$sourcePath/xmlSource$en.xml");
	#prendo il link di primo livello che non deve essere selezionato
	my $menuFirstLevelNotSelected = $xmlFile->findvalue('@firstLevelMenuNotSelected');
	
	
	#recupero il padre inserito nel breadcrumb
	my %parentLinksBreadcrumb = ();
	$parentLinksBreadcrumb{"linkName"} = $xmlFile->findvalue('@parentPathName');
	$parentLinksBreadcrumb{"linkFile"} = $xmlFile->findvalue('@parentPathLink');
	
	foreach my $pageDetails ($xmlFile->findnodes('pageDetails')->get_nodelist) {  #pageDetails e' un nodo XML con tutte le informazioni della pagina
		
		#invoco funzione per creare una singola pagina
		my $pageCreated = &createSinglePage($menuFirstLevelNotSelected, $pageDetails, $sourcePath, 0, \%parentLinksBreadcrumb, $en);
		
		my $pageName = $pageDetails->findvalue('contentsPageFileName');  #prendo il nome del file che andra' generato
		my $completePath = $outputPath . "/" . $pageName;  #creo il path completo per la creazione del file
		
		my $otherPage = $pageName;
		if ($en eq "") {
			$otherPage =~ s/.html/en.html/g;
		}
		else {
			$otherPage =~ s/en.html/.html/g;
		 }
		 $pageCreated =~ s/<linkOtherLanguage\/>/$otherPage/g;
		 
	
		&createFile($completePath, $pageCreated);
		
		print "Page created: $pageName \n";
	} 
	
}

1;
