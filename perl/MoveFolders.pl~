#!/usr/bin/perl

use utf8;
use File::Copy::Recursive qw(fcopy rcopy dircopy fmove rmove dirmove);

require "GlobalVariables.pl";
require "MoveXMLFiles.pl";

#funziona che sposta le cartelle insieme al loro contenuto, dove cioè non abbiamo pagine da generare
sub moveFolders() {

	#elenco cartelle
	my @foldersMove = (
		"img", 
		"style", "js", 
		"cgi-bin", 
		"documenti"
		);
		
	&moveXMLFiles();
	
	foreach $folder (@foldersMove) {

		my $firstDirectory = "../pagesSource/$folder";
		my $endDirectory = $sitePath . "$folder";
		
		#elimino quella precedente
		#unlink($endDirectory);
		
		#copio cartella insieme ai file
		my $num_of_files_and_dirs = dircopy($firstDirectory,$endDirectory);
		
		#cambio gruppo per la cartella
		my @commands = ("chgrp", "www-data", "$endDirectory");
		system(@commands);
		
		#imposto permessi per i file
		my $cmd = "chmod 664 $endDirectory/*.*";
		system $cmd;
	}
	
	my $private = $sitePath . "private";
	if (!(-d $private)) {
		mkdir($private);
		my $cmd = "chmod 775 $private";
		system($cmd);
		my @commands = ("chgrp", "www-data", "$private");
		system(@commands);
		mkdir($private . "/archivio");
		$cmd = "chmod 775 $private";
		system($cmd);
		@commands = ("chgrp", "www-data", "$private/archivio");
		system(@commands);
		mkdir($private . "/tesimagistrale");
		$cmd = "chmod 775 $private";
		system($cmd);
		@commands = ("chgrp", "www-data", "$private/tesimagistrale");
		system(@commands);
		mkdir($private . "/presentazionimagistrale");
		$cmd = "chmod 775 $private";
		system($cmd);
		@commands = ("chgrp", "www-data", "$private/presentazionimagistrale");
		system(@commands);
	
	}
	
	my $document = $sitePath . "documenti";
	if (!(-d $document)) {
		mkdir($document);
		my $cmd = "chmod 775 $document";
		system($cmd);
	}
	
	#imposto permessi e cambio gruppo per i file xml
	my $cmd = "chmod 775 $sitePath" . "xml_files/*.*";
	system($cmd);

	$cmd = "chgrp www-data $sitePath" . "xml_files/*.*";
	system($cmd);
	
	$cmd = "chmod 755 $sitePath" . "cgi-bin/*.*";
	system($cmd);

}

1;
