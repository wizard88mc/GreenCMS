#!/usr/bin/perl

use XML::LibXML;
use utf8;
use Date::Calc qw(Delta_Days);

require "GlobalVariables.pl";
require "GlobalFunctions.cgi";
require "WorkWithFiles.pl";

{
	
	my $pageNews = &openFile($siteForCGI . "news/newsen.html");	
	
	my $activeNewsXML = $fileXML . "ActiveNews.xml";
	my $expiredNewsXML =  $fileXML . "ExpiredNews.xml";
	
	my $parser = XML::LibXML->new();
	
	my $document = $parser->parse_file($activeNewsXML);
	my $root = $document->getDocumentElement;
	
	my $activeNewsList = $root->find("//TableActiveNews/ActiveNews");
	
	my $allNews = "";
	
	foreach my $activeNews ($activeNewsList->get_nodelist) {
		
		my $newsID = $activeNews->findvalue('ID');
		my $date = $activeNews->findvalue('Date');
		$date = &convertDateFromDBToItalian($date);
		my $time = $activeNews->findvalue('Time');
		$time = substr($time, 0, 5);
		my $title = $activeNews->find('Title')->get_node(1)->firstChild->toString;
		my $publisher = $activeNews->find('Publisher')->get_node(1)->firstChild->toString;
		my $type = $activeNews->findvalue('Type');
		my $text = $activeNews->findvalue('Text');
		
		if ($type eq "G") {
			$type = "<abbr title=\"General\">G</abbr>";
		}
		if ($type eq "L") {
			$type = "<abbr title=\"Laurea\">L</abbr>";
		}
		if ($type eq "LM") {
			$type = "<abbr title=\"Magistrale\">LM</abbr>";
		}
		
		$text = &convertLinks($text);
		
		my $stringNews = 
		"<h4><strong><span xml:lang=\"it\">$title</span> - $type</strong></h4>
		<p><span xml:lang=\"it\">$publisher</span> - $date $time</p>
		<p xml:lang=\"it\">$text</span></p>
		<p class=\"tornaSu withBorderBottom\"><a href=\"#contentsLong\">Move up &#9650;</a></p>";
		
		$allNews .= $stringNews;
	}
	
	if (index($allNews, "</p>") == -1) {
		$allNews = "<p><em>No active News</em></p>";
	}
	
	utf8::encode($allNews);
		
	$document = $parser->parse_file($expiredNewsXML);
	$root = $document->getDocumentElement;
	
	my $expiredNewsList = $root->find("//TableExpiredNews/ExpiredNews");
		
	my $listExpiredNews = "";
	
	foreach my $expiredNews ($expiredNewsList->get_nodelist) {
		
		my $newsID = $expiredNews->findvalue('ID');
		my $date = $expiredNews->findvalue('Date');
		$date = &convertDateFromDBToItalian($date);
		my ($currentYear, $currentMonth, $currentDay) = &getCurrentDate();
		if (&checkDatesCronologicallyCorrect(
		    $date, "$currentDay-$currentMonth-$currentYear") eq true) {
		
            my $time = $expiredNews->findvalue('Time');
            $time = substr($time, 0, 5);
            my $title = $expiredNews->findvalue('Title');
            my $publisher = $expiredNews->findvalue('Publisher');
            my $type = $expiredNews->findvalue('Type');
            my $text = $expiredNews->findvalue('Text');
            
            if ($type eq "G") {
                $type = "<abbr title=\"General\">G</abbr>";
            }
            if ($type eq "L") {
                $type = "<abbr title=\"Laurea\">L</abbr>";
            }
            if ($type eq "LM") {
                $type = "<abbr title=\"Magistrale\">LM</abbr>";
            }
            
            $text = &convertLinks($text);
            
            my $stringNews = 
            "<h3>$title - $type</h3>
            <p>$publisher - $date $time</p>
            <p class=\"withBorderBottom\">$text</p>";
            
            $listExpiredNews .= $stringNews;
            }
		
	}
		
	if (index($listExpiredNews, "</p>") == -1) {
		$listExpiredNews = "<p><em>No expired News</em></p>";
	}
	
	utf8::encode($listExpiredNews);
		
	my $srcPath = "src=\"../";
	my $hrefPath = "href=\"../";
	my $newSRC = "src=\"/$folderBase";
	my $newHREF = "href=\"/$folderBase";
	my $folder = "news/";
	
	my $ulSecond = index($pageExams, "div id=\"contents");
	my $endSecond = index($pageExams, "/ul", $ulSecond);
	my $href = index($pageExams, "href=\"", $ulSecond);
	
	
	while ($href != -1 && $href < $endSecond) {
		
		my $endLink = index($pageExams, "\"", $href + length("href=\""));
		my $link = substr($pageExams, $href, $endLink - $href);
		if (index($link, '.cgi') == -1) {
			substr($pageExams, $href, length("href=\""), "href=\"/$folderBase" . $folder);
		}
		
		$href = index($pageExams, "href=\"", $href + length("href=\"") + 5);
		
	}
	
	
	$pageNews =~ s/$srcPath/$newSRC/g; 
	$pageNews =~ s/$hrefPath/$newHREF/g;
	$pageNews =~ s/<tableActiveNews\/>/$allNews/g;
	$pageNews =~ s/<tableExpiredNews\/>/$listExpiredNews/g;
	
	$pageNews =~ s/news.html/News.cgi/g;
	$pageNews =~ s/Seminari.cgi/Seminarien.cgi/g;
	
print <<PAGE;
Content-type: text/html\n\n
$pageNews

PAGE
	
}
