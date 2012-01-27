#!/usr/bin/perl

use utf8;
use XML::LibXML;

require "CreateHead.pl";
require "CreateHeadEn.pl";
require "CreateHeader.pl";
require "CreateFirstLevelMenu.pl";
require "CreateContent.pl";
require "CreateFooter.pl";
require "CreateBreadcrumb.pl";

#parametri: 
#    $_[0] - nome del link del menu di primo livello che non deve essere selezionato
#    $_[1] - nodo XML contentente tutti i dettagli della pagina che si vuole creare
#    $_[2] - path della cartella dove trovare i sorgenti per la pagina
#    $_[3] - booleano che indica se la pagina da creare è l'home page o meno
#    $_[4] - padre della pagina nel breadcrumb
#    $_[5] - discriminante se la pagina è in italiano o in inglese

sub createSinglePage() {
	
	my $firstMenuNotSelected = $_[0];
	my $xmlNode = $_[1];
	my $sourcePath = $_[2];
	my $isHomePage = $_[3];
	my %parentLinksBreadcrumb = %{$_[4]};
	my $en = $_[5];
	
	my $secondMenuNotSelected = $xmlNode->findvalue('secondLevelMenuNotSelected');  #prendo dal nodo XML il link del menu di secondo livello che non deve essere selezionato
	my $pageFile = $xmlNode->findvalue('contentsPageFileName'); #prendo il nome del file dove si trova il contenuto per quella pagina
	
	my $finalPage = "";
	
	#creo l'head della pagina
	if ($en eq "") {
		$finalPage = &createHead($xmlNode, $isHomePage);
	}
	else {
		$finalPage = &createHeadEn($xmlNode, $isHomePage);
	}
	
	$finalPage .= "<body>";
	
	#creo l'header della pagina
	$finalPage .= &createHeaderPage($isHomePage, $en);
	
	$finalPage .= "<div id=\"main\">";
	
	#creo menu di primo livello
	$finalPage .= &createFirstLevelMenu($firstMenuNotSelected, $isHomePage, $pageFile, $en);
	
	my $otherParent = $xmlNode->findvalue('otherParent');
	my $pageTitle = $xmlNode->findvalue('pageTitle');
	
	my $breadcrumb = &createBreadcrumb(\%parentLinksBreadcrumb, $otherParent, $pageTitle, $en);
	
	#aggiungo il contenuto
	$finalPage .= &createContent($sourcePath, $pageFile, $secondMenuNotSelected, $en);
	
	#concludo con il footer
	$finalPage .= &createFooter($isHomePage, $en);
	
	#chiudo la pagina html
	$finalPage .= "</body>
</html>";

	#sostituisce breadcrumb e titolo pagina
	$finalPage =~ s/<breadcrumb\/>/$breadcrumb/;
	$finalPage =~ s/<pageTitleContent\/>/$pageTitle/g;
	
	my $linksAccessibility = "<a href=\"#beginContent\">Vai ai contenuti</a> ";
	
	if (index($finalPage, "<ul id=\"secondLevel\">") != -1) {
		$linksAccessibility .= " <a href=\"#secondLevel\">Vai al menu di secondo livello</a> ";	
	}
	
	if (index($finalPage, "<div id=\"today\">") != -1) {
		$linksAccessibility .= " <a href=\"#today\">Vai alle news</a>";	
	}
	
	$linksAccessibility = "<span class=\"aural\">$linksAccessibility</span>";
	
	#sostituisce i link per l'accessibilità
	$finalPage =~ s/<linksAccessibility\/>/$linksAccessibility/g;
	
	#restituisco pagina creata (in formato testuale)
	return $finalPage;
	
}

1;
