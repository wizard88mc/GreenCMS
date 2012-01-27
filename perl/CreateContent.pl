#!/usr/bin/perl

use utf8;

binmode STDIN, ":utf8";
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";

require "WorkWithFiles.pl";
require "CreateSecondLevelMenu.pl";

#parametri:
#    $_[0] - path dove trovare il file con il contenuto da aggiungere alla pagina  nomeCartella/source
#    $_[1] - nome del file dove trovare i contenuti
#    $_[2] - nome del link del menu di secondo livello non selezionato
#    $_[3] - discriminante italiano - inglese

sub createContent() {
	
	my $pageFile = $_[0] . "/" . $_[1];
	my $secondMenuNotSelected = $_[2];
	my $en = $_[3];
	
	#apro pagina con i contenuti
	my $pageContent = &openFile($pageFile);
	
	#creo menu di secondo livello
	my $secondLevelMenu = &createSecondLevelMenu($_[0], $secondMenuNotSelected, $en);
	
	#sostituisco, nella parte dei contenuti, il tag fittizio da me inserito <secondLevelMenu/> il testo del menu di secondo livello appena creato
	$pageContent =~ s/<secondLevelMenu\/>/$secondLevelMenu/;  
	
	return $pageContent;
	
}

1;
