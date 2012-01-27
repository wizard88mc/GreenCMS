#!/usr/bin/perl

use Time::localtime;
use XML::LibXML;
use utf8;

binmode STDIN, ":utf8";
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";

require "AddYearArchive.pl";
require "ExtractCourses.pl";
require "ArchiveSeminars.pl";
require "WorkWithFiles.pl";


{
	my $year = localtime->year() + 1900;
	my $yearBack = $year - 1;
	
	my $stringAA = "$yearBack/$year";
	
	#aggiungo anno accademico all'archivio
	&addYearArchive($stringAA, "");
	&addYearArchive($stringAA, "en");
	
	#estraggo l'elenco dei corsi
	my @coursesIt = &extractCourses($stringAA, "");
	my @coursesEn = &extractCourses($stringAA, "en");
	
	my @seminars = &archiveSeminars();
	
	my $pageTemplate = &openFile("../pagesSource/archivio/source/yeararchivetemplate.html");
	
	$pageTemplate =~ s/<year\/>/$stringAA/;
	$pageTemplate =~ s/<listCoursesLaurea\/>/$coursesIt[0]/;
	$pageTemplate =~ s/<listCoursesMagistrale\/>/$coursesIt[1]/;
	$pageTemplate =~ s/<listSeminars\/>/$seminars[0]/g;
	
	my $slash = "/";
	$stringAA =~ s/$slash//g;
	
	&createFile("../pagesSource/archivio/source/archivio$stringAA.html", $pageTemplate);
	
	$pageTemplate = &openFile("../pagesSource/archivio/source/yeararchivetemplateen.html");
	
	$pageTemplate =~ s/<year\/>/$stringAA/;
	$pageTemplate =~ s/<listCoursesLaurea\/>/$coursesEn[0]/;
	$pageTemplate =~ s/<listCoursesMagistrale\/>/$coursesEn[1]/;
	$pageTemplate =~ s/<listSeminars\/>/$seminars[1]/g;
	
	my $slash = "/";
	$stringAA =~ s/$slash//g;
	
	&createFile("../pagesSource/archivio/source/archivio$stringAA" . "en.html", $pageTemplate);
	
}
