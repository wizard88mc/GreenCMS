#!/usr/bin/perl

use utf8;

binmode STDIN, ":utf8";
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";

#parametri
#    $_[0] - percordo del file da aprire

sub openFile() {

	my $inputFileName = $_[0];
	
	open (MYFILE, '<', $inputFileName); #apro file
	
	my $fileText = "";
	
	while (<MYFILE>) { #fintanto che c'è da leggere qualcosa all'interno del file leggo e aggiungo alla stringa
		chomp;
		$fileText .= "$_\n";
	}
	
	return $fileText;
	
}

#parametri
#    $_[0] - percorso del file da creare
#    $_[1] - testo da scrivere nel file

sub createFile() {

	my $filePosition = $_[0];
	my $fileText = $_[1];
	
	open (MYFILE, '>', $filePosition);
	print MYFILE "$fileText";
	close (MYFILE);
	
	chmod(0775, $filePosition);
}
