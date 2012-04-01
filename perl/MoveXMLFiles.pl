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

	my $joinsFile = $sitePath . "xml_files/EventMailingListContact.xml";

	my $parser = XML::LibXML->new();
	my $document = $parser->parse_file($joinsFile);
	
	#estraggo la radice del file XML
	my $root = $document->getDocumentElement;
	
	#recupero l'insieme degli eventi e li elimino
	my $joinList = $root->findnodes("Event");
	
	foreach $join ($joinList->get_nodelist) {
		my $parent = $join->parentNode;
		$parent->removeChild($join);
	}
	
	open(FILE, ">$joinsFile") || die("Non riesco ad aprire il file");
	print FILE $document->toString();
	close(FILE);

	# devo ora eliminare anche le associazioni tra seminari e mailing list / email
	# presenti nell'altro file
	my $fileAssociazioni = $sitePath . 'xml_files/MailingListsContactsJoins.xml';
	
	my $documentAssociazioni = $parser->parse_file($fileAssociazioni);
	my $rootAssociazioni = $documentAssociazioni->getDocumentElement;
	
	my $associazioni = $rootAssociazioni->findnodes('TableJoinEventsMailingLists/JoinEventMailingList');
	
	foreach $associazione ($associazioni->get_nodelist) {
	    my $parent = $associazione->parentNode;
	    $parent->removeChild($associazione);
	}
	
	open(FILE, ">$fileAssociazioni") || die("Non riesco ad aprire il file");
	print FILE $documentAssociazioni->toString();
	close(FILE);

}

sub moveXMLFiles() {

	my $folderStart = "../pagesSource/xml_files";
	my $folderEnd = $sitePath . "xml_files";
	
	if (-d $folderEnd) {
		
		print "Copy part\n";
		my @toCopy = ("EventMailingListContact.xml", "ActiveNews.xml", "ExpiredNews.xml", "rssfeed.xml");
		
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