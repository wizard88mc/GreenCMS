#!/usr/bin/perl

use utf8;
use XML::LibXML;

binmode STDIN, ":utf8";
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";

require "GlobalVariables.pl";
require "CreateSinglePage.pl";
require "CreateIndex.pl";
require "WorkWithFiles.pl";
require "UpdatePHDStudent.pl";
require "UpdatePHDStudentEn.pl";
require "UpdatePageArchiveThesis.pl";
require "CreateReservedTemplate.pl";

{
	&createIndex();
	
	foreach $folder (@folders) {
	
		#path dove sono collocati i file con il contenuto che andra' inserito nel file html
		my $sourcePath = "../pagesSource/$folder/source"; 
		#path della cartella dove verranno creati i file html
		my $outputPath = $sitePath . "$folder";   
		
		#leggo file xml per estrapolare le informazioni delle pagine
		my $xmlFile = &extractXML("$sourcePath/xmlSource.xml");
		
		#prendo il link di primo livello che non deve essere selezionato
		my $menuFirstLevelNotSelected = $xmlFile->findvalue('@firstLevelMenuNotSelected');  
		my %parentLinksBreadcrumb = ();
		$parentLinksBreadcrumb{"linkName"} = $xmlFile->findvalue('@parentPathName');
		$parentLinksBreadcrumb{"linkFile"} = $xmlFile->findvalue('@parentPathLink');
		
		#pageDetails e' un nodo XML con tutte le informazioni della pagina
		foreach my $pageDetails ($xmlFile->findnodes('pageDetails')->get_nodelist) {  
			
			if ($pageDetails->findvalue('@isStatic') eq "T") {
				#invoco funzione per creare una singola pagina
				my $pageCreated = &createSinglePage($menuFirstLevelNotSelected, $pageDetails, $sourcePath, 0, \%parentLinksBreadcrumb);
				
				#prendo il nome del file che andra' generato
				my $pageName = $pageDetails->findvalue('contentsPageFileName');
				#creo il path completo per la creazione del file
				my $completePath = $outputPath . "/" . $pageName;  
				
				my $otherPage = $pageName;
				$otherPage =~ s/.html/en.html/g;
				
				$pageCreated =~ s/<linkOtherLanguage\/>/$otherPage/g;
			
				&createFile($completePath, $pageCreated);
				
				print "Page Updated: $pageName \n";
			}
			
		}

		my $xmlFileEn = &extractXML("$sourcePath/xmlSourceen.xml");	
		$menuFirstLevelNotSelected = $xmlFileEn->findvalue('@firstLevelMenuNotSelected');  
		%parentLinksBreadcrumb = ();
		$parentLinksBreadcrumb{"linkName"} = $xmlFileEn->findvalue('@parentPathName');
		$parentLinksBreadcrumb{"linkFile"} = $xmlFileEn->findvalue('@parentPathLink');

		foreach my $pageDetails ($xmlFileEn->findnodes('pageDetails')->get_nodelist) {  
			
			if ($pageDetails->findvalue('@isStatic') eq "T") {
				#invoco funzione per creare una singola pagina
				my $pageCreated = &createSinglePage($menuFirstLevelNotSelected, $pageDetails, $sourcePath, 0, \%parentLinksBreadcrumb, "en");
				
				#prendo il nome del file che andra' generato
				my $pageName = $pageDetails->findvalue('contentsPageFileName');
				#creo il path completo per la creazione del file
				my $completePath = $outputPath . "/" . $pageName; 
				
				my $otherPage = $pageName;
				$otherPage =~ s/en.html/.html/g;
				
				$pageCreated =~ s/<linkOtherLanguage\/>/$otherPage/g;
			
				&createFile($completePath, $pageCreated);
				
				print "Page Updated English: $pageName \n";
			}
			
		}
	}
	
	my @commands = ("chgrp", "www-data", "$sitePath" . "laureamagistrale/uploadtesi.html");
	system(@commands);
	
	my @commands = ("chgrp", "www-data", "$sitePath" . "laureamagistrale/uploadpresentazioni.html");
	system(@commands);
	
	my @commands = ("chgrp", "www-data", "$sitePath" . "dottorato/index.html");
	system(@commands);

	my @commands = ("chgrp", "www-data", "$sitePath" . "dottorato/indexen.html");
	system(@commands);
	
	my @commands = ("chgrp", "www-data", "$sitePath" . "laureamagistrale/archiviotesi.html");
	system(@commands);
	
	my @commands = ("chgrp", "www-data", "$sitePath" . "laureamagistrale/archiviotesien.html");
	system(@commands);
	
	&updatePHDStudent();
	&updatePHDStudentEn();
	
	&updatePageArchiveThesis();
	
	&createReservedTemplate();
	
}