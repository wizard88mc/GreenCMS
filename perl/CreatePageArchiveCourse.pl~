#!/usr/bin/perl

use utf8;

binmode STDIN, ":utf8";
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";

require "WorkWithFiles.pl";
require "GlobalVariables.pl";

#prendo la parte di una pagina di un corso che mi interessa, da content-right alla fine
sub createPageArchiveCourse() {
	
	my $inputPageName = $_[0];
	my $stringAA = $_[1];
	my $folder = $_[2];
	my $en = $_[3];
	my $slash = "/";
	
	#apro pagina contenente il dettaglio dei corsi 
	my $inputPage = &openFile($sitePath . "$folder/$inputPageName");
	
	#recupero l'indice dove inizia il contenuto, e cioè dove inizia div id="contents-right
	my $indexContents = index($inputPage, "<div id=\"contents-right\">");
	
	#recupero l'indice dove si conclude il contenuto (lo trovo basandomi sul div contatore
	my $endDiv = index($inputPage, "\"contatore\"") - 8;
	
	#prendo il contenuto della pagina
	my $piecePage = substr($inputPage, $indexContents , $endDiv - $indexContents);
	
	#sostituisco al titolo della pagina il titolo con aggiunto alla fine l'anno accademico di rfierimento
	substr($piecePage, index($piecePage, "</h2>"), 5, " - A.A. $stringAA</h2>");
	
	#prendo l'attuale menu di secondo livello e lo sostituisco con il tag <secondLevelMenu/> così da aggiungere quello
	#vero alla generazione della pagina
	my $startSecondLevel = index($piecePage, "<ul id=\"secondLevel\">");
	my $endSecondLevel = index($piecePage, "</ul>", $startSecondLevel) + 5;
	
	substr($piecePage, $startSecondLevel, $endSecondLevel - $startSecondLevel, '<secondLevelMenu/>');
	
	#faccio la stessa cosa con il breadcrumb (elimino quello attuale ed inseriscoil tag per poter inserire quello corretto successivamente
	my $startBreadcrumb = index($piecePage, "<span id=\"path\">");
	my $endBreadcrumb = index($piecePage, "<h1>", $startBreadcrumb) - 1;
	
	substr($piecePage, $startBreadcrumb, $endBreadcrumb - $startBreadcrumb, '<breadcrumb/>');
	
	$stringAA =~ s/$slash//g;
	
	#creo il nome della pagina finale: pagina iniziale + anno accademico di riferimento
	
	my $finalPageName = substr($inputPageName, 0, rindex($inputPageName, ".")) . "$stringAA" . ".html";
	
	if ($en ne "") {
		$finalPageName = substr($inputPageName, 0, rindex($inputPageName, "en.")) . "$stringAA" . "en.html";
	}
	
	&createFile("../pagesSource/archivio/source/$finalPageName", $piecePage);
	
	return $finalPageName;
	
}

1;
