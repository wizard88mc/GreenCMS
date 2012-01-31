#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use HTML::Entities;
use XML::LibXML;
use utf8;

require "WorkWithFiles.pl";
require "GlobalVariables.pl";

{
	$page = new CGI;
	$newsID = $page->param('newsID');

	my $parser = XML::LibXML->new();
	
	my $activeNewsXML = $fileXML . "ActiveNews.xml";
	my $espiredNewsXML = $fileXML . "ExpiredNews.xml";
	
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
			$date = substr($date, 8, 2) . "/" . substr($date, 5, 2) . "/" . substr($date, 0, 4);
			my $time = $newsNode->findvalue('Time');
			$time = substr($time, 0, 5);
			my $publisher = $newsNode->findvalue('Publisher');
			my $text = $newsNode->findvalue('Text');
			
			$informations{'date'} = $date;
			$informations{'time'} = $time;
			$informations{'publisher'} = $publisher;
			$informations{'text'} = $text;
		
		}
		
		if (!$newsFound) {
			
			$document = $parser->parse_file($espiredNewsXML);
			$root = $document->getDocumentElement;
		
			$title = $root->findvalue("TableExpiredNews/ExpiredNews[ID=$newsID]");
			
			if ($title ne "") {
				
				$newsFound = 1;
				
				$newsNode = $root->find("//TableExpiredNews/ExpiredNews[ID=$newID]")->get_node(1);
				
				$informations{'title'} = $title;
				my $date = $newsNode->findvalue('Date');
				$date = substr($date, 8, 2) . "/" . substr($date, 5, 2) . "/" . substr($date, 0, 4);
				my $time = $newsNode->findvalue('Time');
				$time = substr($time, 0, 5);
				my $publisher = $newsNode->findvalue('Publisher');
				my $text = $newsNode->findvalue('Text');

				$informations{'date'} = $date;
				$informations{'time'} = $time;
				$informations{'publisher'} = $publisher;
				$informations{'text'} = $text;
			}
		
		}
	}
	
	my $newsHeader;
	
	if (!$newsFound) {
		
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
	
	my $openTagLink = '[link]';
    my $closeTagLink = '[/link]';
    
    my $positionLink = index($informations{'text'}, $openTagLink);
    
    while ($positionLink != -1) {
        
        #posizione di fine del link
        my $endLink = index($informations{'text'}, $closeTagLink, $positionLink);
        
        my $link = substr($informations{'text'}, $positionLink + length($openTagLink), $endLink - $positionLink - length($openTagLink));
        $link =~ s/ //g;
        $link = "<a href=\"$link\">$link</a>";
        substr($informations{'text'}, $positionLink, $endLink + length($closeTagLink) - $positionLink, $link);

        $positionLink = index($informations{'text'}, $openTagLink, $positionLink + length($link));
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
