#!/usr/bin/perl

use XML::LibXML;
use utf8;
use File::Copy;

binmode STDIN, ":utf8";
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";

require "GlobalVariables.pl";
require "ExtractXML.pl";

sub deleteEvents() {

	my $eventsFile = $sitePath . "xml_files/EventMailingListContact.xml";

	my $parser = XML::LibXML->new();
	my $document = $parser->parse_file($eventsFile);
	
	#estraggo la radice del file XML
	my $root = $document->getDocumentElement;
	
	#recupero l'insieme degli eventi e li elimino
	my $seminarList = $root->findnodes("//TableEvent/Event");
	
	foreach $seminar ($seminarList->get_nodelist) {
		my $parent = $seminar->parentNode;
		$parent->removeChild($seminar);
	}
	
	open(FILE, ">$eventsFile") || die("Non riesco ad aprire il file");
	print FILE $document->toString();
	close(FILE);


}

sub moveXMLFiles() {

	my $folderStart = "../pagesSource/xml_files";
	my $folderEnd = $sitePath . "xml_files";
	
	if (-d $folderEnd) {
		
		print "Copy part\n";
		my @toCopy = ("ActiveNews.xml", "ExpiredNews.xml", "rssfeed.xml");
		
		foreach $file (@toCopy) {
			copy($folderStart . "/$file", $folderEnd . "/$file");
		}
		
		&deleteEvents();
	
	}
	else {
	
		print "Copy all\n";
		my $num_of_files_and_dirs = dircopy($folderStart,$folderEnd);
		
		#cambio gruppo per la cartella
		my @commands = ("chgrp", "www-data", "$folderEnd");
		system(@commands);
		
		#imposto permessi per i file
		my $cmd = "chmod 664 $folderEnd/*.*";
		system $cmd;
	
	
	}

}