#!/usr/bin/perl

use XML::LibXML;
use HTML::Entities;
use utf8;

binmode STDIN, ":utf8";
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";

require "ExtractXML.pl";

sub getCourseSiteLaurea() {
	
	my $courseName = $_[0];
	
	my $fileXMLSites =  "coursesSite/CoursesWebsitesLaurea.xml";
	
	my $root = &extractXML($fileXMLSites);
	
	my $coursesWebsites = $root->find("//CoursesWebsites")->get_node(1);
	
	my $sitePresent = $coursesWebsites->exists("//CourseWebsite[Course=\"$courseName\"]");
	
	if ($sitePresent) {
		my $linksList = $coursesWebsites->findnodes("//CourseWebsite[Course=\"$courseName\"]/LinkDescription");
		
		my $completeString = "";
		
		foreach my $couple ($linksList->get_nodelist) {
		
			my $link = $couple->findvalue('Link');
			my $description = "";
			if ($couple->findvalue('Description') ne "") {
				$description = $couple->find('Description')->get_node(1)->firstChild->toString;
				encode_entities($description);
			}
			
			my $string = "";
			
			if ($description eq "") {

				$string = "<p><a href=\"$link\">Link al sito del corso</a></p>";	
			}
			else {
				$string = "<p><a href=\"$link\">$description</a></p>";
			}
			
			$completeString .= $string;
			
		}
		
		return $completeString;
	}
	else {
		return "";
	}
	
}

sub getCourseSiteMagistrale() {
	
	my $courseName = $_[0];

	my $fileXMLSites =  "coursesSite/CoursesWebsitesMagistrale.xml";
	
	my $root = &extractXML($fileXMLSites);
	
	my $coursesWebsites = $root->find("//CoursesWebsites")->get_node(1);
	
	my $sitePresent = $coursesWebsites->exists("//CourseWebsite[Course=\"$courseName\"]");
	
	if ($sitePresent) {
		my $linksList = $coursesWebsites->find("//CourseWebsite[Course=\"$courseName\"]/LinkDescription");
		
		my $completeString = "";
		
		foreach my $couple ($linksList->get_nodelist) {
		
			my $link = $couple->findvalue('Link');
			my $description = "";
			if ($couple->findvalue('Description') ne "") {
				$description = $couple->find('Description')->get_node(1)->firstChild->toString;
				encode_entities($description);
			}
			
			my $string = "";
			
			if ($description eq "") {

				$string = "<p><a href=\"$link\">Link al sito del corso</a></p>";	
			}
			else {
				$string = "<p><a href=\"$link\">$description</a></p>";
			}
			
			$completeString .= $string;
			
		}
		
		return $completeString;
	}
	else {
		return "";
	}
}

