#!/usr/bin/perl

use utf8;

binmode STDIN, ":utf8";
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";

require "WorkWithFiles.pl";

#parametri
#    $_[0] - booleano che indica se l'header appartiene o meno all'home page
#    $_[1] - discriminante italiano / inglese

sub createHeaderPage() {
	
	my $en = $_[1];
	my $headerPageText = "";
	my $pathSRC = "src=\"../";  #path di default per i link indicati da src
	my $pathHREF = "href=\"../"; #path di default per i link indicati da href 
	$headerPageText = &openFile("../pagesSource/globalDetails/header$en.html");
	
	if ($_[0]) {  #se la pagina è l'home page, devo eliminare dal path di tutti i collegamenti ../, visto che l'home page si trova nella root del sito
		$headerPageText =~ s/$pathSRC/src="/g; 
		$headerPageText =~ s/$pathHREF/href="/g; 
	}
	
	return $headerPageText;
}

1;
