#!/usr/bin/perl

#use CGI qw(:standart);
use CGI::Carp qw(fatalsToBrowser);
use utf8;

binmode STDIN, ":utf8";
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";

require "GlobalVariables.pl";
require "WorkWithFiles.pl";

sub createHeader() {

	my $headerPageText = "";
	my $pathSRC = "src=\"../";  #path di default per i link indicati da src
	my $pathHREF = "href=\"../"; #path di default per i link indicati da href
	
	#recupero head generale e sostituisco link
	$headerPageText = &openFile($sourcePath . "/pagesSource/globalDetails/header.html");
	
	$headerPageText =~ s/$pathSRC/src="$sitePath/g; 
	$headerPageText =~ s/$pathHREF/href="$sitePath/g; 
	
print <<HEADER;
$headerPageText
<div id="main">
HEADER
}	

1;
