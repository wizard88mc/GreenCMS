#!C:/usr/bin/perl.exe
#!C:/usr/bin/perl
#!/usr/bin/perl.exe
#!/usr/bin/perl

use utf8;

binmode STDIN, ":utf8";
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";

require "GlobalVariables.pl";
require "CreateSinglePage.pl";
require "WorkWithFiles.pl";

{

	my $pagesToUpdate = $#ARGV;
	
	foreach $pageNumber (0 .. $pagesToUpdate) {
	
		my $page = $ARGV[$pageNumber];
		my $folderName = substr($page, 0, index($page, "/"));
		my $pageDirectory = "../pagesSource/" . $folderName;
		
		my $pageName = substr($page, index($page, "/") + 1);
	
		my $sourcePath = $pageDirectory . "/source";
		my $outputPath = $folderHTMLPath . "/$folderName";  #path della cartella dove verranno creati i file html 
		
		my $xmlFile = &extractXML("$sourcePath/xmlSource.xml");
		my $menuFirstLevelNotSelected = $xmlFile->{firstLevelMenuNotSelected};  #prendo il link di primo livello che non deve essere selezionato
		my %parentLinksBreadcrumb = ();
		$parentLinksBreadcrumb{"linkName"} = $xmlFile->{parentPathName};
		$parentLinksBreadcrumb{"linkFile"} = $xmlFile->{parentPathLink};
		
		if ($pageName ne "index.html") {
			foreach my $pageDetails (@{$xmlFile->{pageDetails}}) {  #pageDetails è un nodo XML con tutte le informazioni della pagina
				
				if ($pageDetails->{contentsPageFileName} eq $pageName) {
					
					my $completePath;
					my $pageCreated;
					if ($pageName eq "index.html") {
					
						my $indexCreated = &createSinglePage("", $indexDetails, "../pageSources/index/source", 1);
						$completePath = $folderHTMLPath . "/index.html";
					}
					else {
						$pageCreated = &createSinglePage($menuFirstLevelNotSelected, $pageDetails, $sourcePath, 0, \%parentLinksBreadcrumb);
						$completePath = $outputPath . "/" . $pageName;  #creo il path completo per la creazione del file
					}
					
					print $completePath;
					&createFile($completePath, $pageCreated);
					
					print "Page Updated: $pageName \n";
				}
			} 
		}

	}
	
}