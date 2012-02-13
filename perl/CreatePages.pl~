#!/usr/bin/perl

use utf8;

require "CreatePageFolder.pl";
require "CreateIndex.pl";

#funzione invocata per creare tutte le pagine
#parametri:
#    $_[0] - indica se le pagine da generare sono quelle in inglese o in italiano

sub createPages() { 
	
	#invoco funzione per la creazione dell'index
	&createIndex();

	foreach $folder(@folders) {
		#cancello cartella che voglio creare
		unlink($sitePath . "$folder");
		mkdir($sitePath . "$folder");  #creo la cartella
		#imposto permessi
		chmod(0775, $sitePath . "$folder");
		
		#assegno gruppo
		my @commands = ("chgrp", "www-data", "$sitePath" . "$folder");
		system(@commands);
		
		print "FOLDER: $folder \n";
		&createPagesOfFolder($folder);  #invoco metodo per creare tutte le pagine apparteneneti a quella cartella
		&createPagesOfFolder($folder, "en");
	}
	
	my @commands = ("chgrp", "www-data", "$sitePath" . "laureamagistrale/uploadtesi.html");
	system(@commands);
	
	my @commands = ("chgrp", "www-data", "$sitePath" . "laureamagistrale/uploadpresentazioni.html");
	system(@commands);
	
	my @commands = ("chgrp", "www-data", "$sitePath" . "dottorato/index.html");
	system(@commands);

	my @commands = ("chgrp", "www-data", "$sitePath" . "dottorato/indexen.html");
	system(@commands);
	
	my @commands = ("chgrp", "www-data", "$sitePath" . "laureamagistrale/archiviotesi.html");
	system(@commands);
	
	my @commands = ("chgrp", "www-data", "$sitePath" . "laureamagistrale/archiviotesien.html");
	system(@commands);
	
	print "Pages Created";

}

1;
