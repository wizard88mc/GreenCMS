#!/usr/bin/perl

use utf8;

sub insertThesisPageArchive() {
	
	my $italian = $_[0];
	my $english = $_[1];

	my $pageArchiveIt = &openFile($siteForCGI . "laureamagistrale/archiviotesi.html");
	my $pageArchiveEn = &openFile($siteForCGI . "laureamagistrale/archiviotesien.html");
		
	if (index($pageArchiveIt, "<p id=\"notPresent\">") != -1) {
		
		my $startPIt = index($pageArchiveIt, "<p id=\"notPresent\">");
		my $endPIt = index($pageArchiveIt, "</p>", $startPIt);
		
		substr($pageArchiveIt, $startPIt, $endPIt + length("</p>") - $startPIt, $italian); 
		
		my $startPEn = index($pageArchiveEn, "<p id=\"notPresent\">");
		my $endPEn = index($pageArchiveEn, "</p>", $startPEn);
		
		substr($pageArchiveEn, $startPEn, $endPEn + length("</p>") - $startPEn, $english); 
		
	}
	else {
		
		my $endTitleIt = index($pageArchiveIt, "</h2>", index($pageArchiveIt, "<div id=\"contentsLong\">")) + length("</h1>");
		
		substr($pageArchiveIt, $endTitleIt, 0, $italian);
		
		my $endTitleEn = index($pageArchiveEn, "</h2>", index($pageArchiveEn, "<div id=\"contentsLong\">")) + length("</h1>");
		
		substr($pageArchiveEn, $endTitleEn, 0, $english);

	}
	
	utf8::encode($pageArchiveIt);
	utf8::encode($pageArchiveEn);

	&createFile($siteForCGI . "laureamagistrale/archiviotesi.html", $pageArchiveIt);
	&createFile($siteForCGI . "laureamagistrale/archiviotesien.html", $pageArchiveEn);

}

1;
