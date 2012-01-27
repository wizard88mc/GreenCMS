#!/usr/bin/perl

use XML::LibXML;
use Data::Dumper;

use utf8;


#parametri input:
#    $_[0] - percorso dove si trova il file XML da estrarre

sub extractXML() {
	
	my $fileXML = $_[0];
	
	my $parser = XML::LibXML->new();
	my $document = $parser->parse_file($fileXML);
	
	#estraggo la radice del file XML
	my $root = $document->getDocumentElement;
	
	return $root; 
	
}

1;
