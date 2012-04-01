#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use utf8;
use Time::localtime;
use Date::Calc qw(Add_Delta_Days Delta_Days);

require "GlobalVariables.pl";
require "GlobalFunctions.cgi";

#insieme di funzioni per la gestione delle news e del feedRSS

$feedRSS = $fileXML . "rssfeed.xml";
$fileXML .= "ActiveNews.xml";

sub deleteNews() {
	
	#eval {
		#parametro di ingresso: ID della news
		$newsID	= $_[0];
		
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileXML);
		my $root = $document->getDocumentElement;
		
		#recupero nodo news da eliminare e rimuovo
		my $newsNode = $root->find("//TableActiveNews/ActiveNews[ID=$newsID]")->get_node(1);
		
		my $newsTitle = $newsNode->findvalue('Title');
		my $newsActivationDate = $newsNode->findvalue('Date');
		$newsActivationDate = &convertDateFromDBToItalian($newsActivationDate);
		print "$newsActivationDate \n";
		
		my $parent = $newsNode->parentNode;
		$parent->removeChild($newsNode);
		
		open(FILE, ">$fileXML") || die("Non riesco ad aprire il file");
		print FILE $document->toString();
		close(FILE);
		
		my ($currentYear, $currentMonth, $currentDay) = &getCurrentDate();
		my $currentDate = "$currentDay-$currentMonth-$currentYear";
		print "$currentDate \n";
		
		if (&checkDatesCronologicallyCorrect($newsActivationDate, $currentDate) eq true) {
		
            my $documentRSS = $parser->parse_file($feedRSS);
            my $rootRSS = $documentRSS->getDocumentElement;
            
            my $feedNode = $rootRSS->find("//item[title=\"$newsTitle\"]")->get_node(1);
            
            my $parent = $feedNode->parentNode;
            $parent->removeChild($feedNode);
            
            open(FILE, ">$feedRSS") || die("Non riesco ad aprire il file");
            print FILE $documentRSS->toString();
            close(FILE);
		    }
		
		return 1;
	#}
	#or do { return 0; }
	
}

&deleteNews(39);
