#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use HTML::Entities;
use XML::LibXML;
use utf8;

require "GlobalVariables.pl";
require "GlobalFunctions.cgi";
require "WorkWithFiles.pl";

{
	$page = new CGI;
	$newsID = $page->param('newsID');

	my $parser = XML::LibXML->new();
	
	my $activeNewsXML = $fileXML . "ActiveNews.xml";
	my $expiredNewsXML = $fileXML . "ExpiredNews.xml";
	
	my $document = $parser->parse_file($activeNewsXML);
	my $root = $document->getDocumentElement;
	my $newsFound = 0;
	my %informations;
	
	if ($newsID ne "") {
	
		my $title = $root->findvalue("//TableActiveNews/ActiveNews[ID=$newsID]/Title");
		
		if ($title ne "") {
			$newsFound = 1;
			$informations{'title'} = $title;
			my $newsNode = $root->find("//TableActiveNews/ActiveNews[ID=$newsID]")->get_node(1);
			
			my $date = $newsNode->findvalue('Date');
			$date = &convertDateFromDBToItalian($date);
			my $time = $newsNode->findvalue('Time');
			$time = substr($time, 0, 5);
			my $publisher = $newsNode->findvalue('Publisher');
			my $text = $newsNode->findvalue('Text');
			$text = &convertLinks($text);
			
			$informations{'date'} = $date;
			$informations{'time'} = $time;
			$informations{'publisher'} = $publisher;
			$informations{'text'} = $text;
		
		}
		
		if ($newsFound == 0) {
			
			$document = $parser->parse_file($expiredNewsXML);
			$root = $document->getDocumentElement;
		
			$title = $root->findvalue("//TableExpiredNews/ExpiredNews[ID=$newsID]/Title");
			
			if ($title ne "") {
				
				$newsFound = 1;
				
				$newsNode = $root->find("//TableExpiredNews/ExpiredNews[ID=$newsID]")->get_node(1);
				
				$informations{'title'} = $title;
				my $date = $newsNode->findvalue('Date');
				$date = &convertDateFromDBToItalian($date);
				my $time = $newsNode->findvalue('Time');
				$time = substr($time, 0, 5);
				my $publisher = $newsNode->findvalue('Publisher');
				my $text = $newsNode->findvalue('Text');
				$text = &convertLinks($text);

				$informations{'date'} = $date;
				$informations{'time'} = $time;
				$informations{'publisher'} = $publisher;
				$informations{'text'} = $text;
			}
		
		}
	}
	
	my $newsHeader;
	
	if ($newsFound == 0) {
		
		$informations{'title'} = "Errore";
		$informations{'date'} = "";
		$informations{'time'} = "";
		$informations{'publisher'} = "";
		$informations{'text'} = "ID News non trovato";
		$newsHeader = "";
	}
	else {
		$newsHeader = "Scritto da $informations{'publisher'} il giorno $informations{'date'} alle ore $informations{'time'}";
	}
	
	utf8::encode($informations{'title'});
	utf8::encode($newsHeader);
	utf8::encode($informations{'text'});
	
	my $newsPage = &openFile($siteForCGI . "news/readnews.html");
	
	my $srcPath = "src=\"../";
	my $hrefPath = "href=\"../";
	my $newSRC = "src=\"/$folderBase";
	my $newHREF = "href=\"/$folderBase";
	
	$newsPage =~ s/$srcPath/$newSRC/g; 
	$newsPage =~ s/$hrefPath/$newHREF/g;
	
	$newsPage =~ s/"nomeNews"/$informations{'title'}/g;
	$newsPage =~ s/<newsHeader\/>/$newsHeader/g;
	$newsPage =~ s/<textNews\/>/$informations{'text'}/g;
	
print <<PAGE;
Content-type: text/html\n\n
$newsPage

PAGE
	
}
