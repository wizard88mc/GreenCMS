#!/usr/bin/perl

use utf8

binmode STDIN, ":utf8";
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";

#funzione per creare il breadcrumb di una pagina
sub createBreadcrumb() {
	
	#HASH contenente il padre della pagina in questione, oltre alla home page
	my %parentLinksBreadcrumb = %{$_[0]};
	#eventuale padre in più
	my $otherParent = $_[1];
	my $pageName = $_[2];
	my $en = "";
	if ($_[3]) { $en = $_[3]; }
	
	#stringa di base del breadcrumb
	my $stringBreadcrumb = "<span id=\"path\"><a href=\"../index$en.html\" xml:lang=\"en\">Home</a> &#187; ";
	
	#nome della pagina padre
	my $parentPathName = "";
	if ($parentLinksBreadcrumb{'linkName'}) {
	    $parentPathName = $parentLinksBreadcrumb{'linkName'};
	}
	#link alla pagina padre
	my $parentPathLink = "";
	if ($parentLinksBreadcrumb{'linkFile'}) {
	    $parentPathLink = $parentLinksBreadcrumb{"linkFile"};
	}
	
	#se la pagina padre è diversa da quella che sto creando aggiungo il link
	if ($pageName ne $parentPathName && $parentPathName ne "") {
		$stringBreadcrumb .= "<a href=\"$parentPathLink\">$parentPathName</a> &#187; ";
	}
	
	#aggiungo l'eventuale padre ulteriore
	if ($otherParent ne "") {
		my $slashPosition = index($otherParent, "/");
		my $otherParentName = substr($otherParent, 0, $slashPosition);
		my $pageLink = substr($otherParent, $slashPosition + 1);
		
		$stringBreadcrumb .= "<a href=\"$pageLink\">$otherParentName</a> &#187; ";
	}
	
	#aggiungo la pagina attual al breadcrumb
	$stringBreadcrumb .= "<span id=\"pathSelected\">$pageName</span></span>";

	utf8::encode($stringBreadcrumb);
	return $stringBreadcrumb;

}


1;
