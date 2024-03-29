#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use File::Copy;
use utf8;

require "GlobalVariables.pl";
require "WorkWithFiles.pl"; 
require "CreateSecondLevelMenu.cgi";
require "FunctionsCCS.cgi";

$CGI::POST_MAX = 1024 * 10000000;

#funzione pre creare stringa contenente la form per inserire un nuovo verbale
sub printFormNewCCS() {
	
	my $message = $_[0];
	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}

	my $content = <<CONTENT;
<div id="contents">
	<h1>Inserimento nuovo CCS</h1>
	$message
	<form method="post" action="NewCCS.cgi">
	<fieldset>
	<label for="date">Data Incontro:  (dd/mm/yyyy)</label>
	<input type="text" name="date" id="date" value="$userFormInput{'date'}" />
	<label for="ordineGiorno">Ordine del Giorno: </label>
	<textarea name="ordineGiorno" id="ordineGiorno" cols="20" rows="10" >$userFormInput{'ordineGiorno'}</textarea>
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" class="button" name="submit" value="Inserisci" />
	<input type="reset" class="button" value="Reset" />
	</fieldset>
	</form>
</div>
CONTENT
	
	return $content;
}

#funzione per stampare report del CCS e form per inserimento verbale in pdf
sub printFormReportCCS() {
	
	my $odg = $userFormInput{'ordineGiorno'};
	$odg =~ s/\n/<br \/>/g;
	
	$content = <<CONTENT;
<div id="contents">
	<h1>Riepilogo Inserimento CCS</h1>
	<form method="post" action="NewCCS.cgi" accept-charset="UTF-8"  enctype="multipart/form-data">
		<fieldset>
		<legend>Riepilogo</legend>
		<p><strong>Data CCS: </strong>$userFormInput{'date'}</p>
		<p><strong>Ordine Del Giorno: </strong></p>
		<p>$odg</p>
		</fieldset>
		<fieldset>
		<label for="verbale">Verbale: (.pdf)</label>
		<input type="file" name="verbale" id="verbale" />
		</fieldset>
		<fieldset>
		<legend class="hidden">Bottoni</legend>
		<input type="submit" name="submit" class="button" value="Conferma" />
		<input type="submit" class="button" name="submit" value="Indietro" />
		<input type="hidden" name="date" value="$userFormInput{'date'}" />
		<input type="hidden" name="ordineGiorno" value="$userFormInput{'ordineGiorno'}" />
		</fieldset>
	</form>
</div>
CONTENT

	return $content;

}

#funzione che stampa la conferma di avvenuto inserimento di un verbale
#permette poi di passare l'inserimento degli allegati
sub printThanks() {
	
	my $CCSID = $_[0];

	my $content = <<CONTENT;
<div id="contents">
	<h1>Inserimento Avvenuto</h1>
	<form method="post" action="ManageAttachments.cgi">
	<fieldset>
	<p>Inserimento avvenuto correttamente</p>
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" class="button" name="submit" value="Inserisci Allegati" />
	<input type="hidden" name="CCSID" value="$CCSID" />
    </fieldset>
	</form>
</div>
CONTENT
	
	return $content;

}

#controlla che la data sia in formato gg/mm/aaaa
#e che ci siano almeno 10 caratteri nell'ordine del giorno
sub checkInput() {

	my $errors = "";
	
	if ($userFormInput{'date'} !~ m/^\d{2}\/\d{2}\/\d{4}$/) {
    	$errors .= "Data non corretta<br />";
    }
    
    if (length($userFormInput{'ordineGiorno'}) < 5) {
    	$errors .= "Ordine del giorno troppo corto<br />";
    }	
	
	return $errors;
}

#upload del file del verbale sul server
sub uploadReport() {
	
	my $safe_filename_characters = "a-zA-Z0-9_.-";
	my ( $name, $path, $extension ) = fileparse($userFormInput{'verbale'}, '\..*' );  
	my $filename = $name . $extension; 
	$extension = substr($extension, rindex($extension, '.'));
	
	if ($extension ne ".pdf") {
		return "Estensione file non valida";
	}
	
	if ($filename eq "") {
		return "File non inserito";
	}
	$filename =~ tr/ /_/;  
	$filename =~ s/[^$safe_filename_characters]//g;  
	
	if ( $filename =~ /^([$safe_filename_characters]+)$/ ) {  
		$filename = $1;  
	}  
	else {  
		return "File mal rinominato";  
	}
	
	$userFormInput{'filename'} = $filename;
	
	#costruisco nome directory come aaaammgg
	my $directory = substr($userFormInput{'date'}, 6) . substr($userFormInput{'date'}, 3, 2) . substr($userFormInput{'date'}, 0, 2);
	
	my $upload_dir = $siteForCGI . "documenti/verbaliccs/" . $directory;
		
	my $upload_filehandle = $page->upload("verbale");
	
	#creo nuova cartella
	mkdir($upload_dir) or die "$!";
	chmod(0775, $upload_dir);
	
	#cambio gruppo
	my $cmd = "chgrp www-data $upload_dir";
	system($cmd);
	
	#carico il file
	open ( UPLOADFILE, ">$upload_dir/$filename" ) or die "$!";    
	binmode UPLOADFILE;
	
	while ( my $bytesread = read($upload_filehandle, my $buffer, 1024) ) {  
		print UPLOADFILE $buffer;  
	}  
	
	close UPLOADFILE;  
	
	chmod(0775, "$upload_dir/$filename");
		
	$cmd = "chgrp www-data $upload_dir/$filename";
	system $cmd;
	
	copy($sourcePath . "perl/htaccess/.htaccess", "$upload_dir/.htaccess") or die "$!";
	
	return "";
}


$page = new CGI;

#se non è autentico rimando utente a pagina di login
$cookie = $page->cookie("CGISESSIONID") || undef;
if (!defined($cookie)) {
	print $page->redirect($siteForCGI . $folderBase . "reservedzone/login.html");
}

$userFormInput{'submit'} = $page->param('submit');



if ($userFormInput{'submit'} ne 0) {
	
	#recupero data, ordine del giorno e verbale
	$userFormInput{'date'} = $page->param('date');
	$userFormInput{'ordineGiorno'} = $page->param('ordineGiorno');
	$userFormInput{'verbale'} = $page->param('verbale');
	
	
	foreach $userInput (keys %userFormInput) {
	if ($userFormInput{$userInput} eq 0) {
		$userFormInput{$userInput} = "";
	}
	utf8::decode($userFormInput{$userInput});
	$userFormInput{$userInput} =~ s/\&/\&amp\;/g;
	$userFormInput{$userInput} =~ s/</\&lt\;/g;
	$userFormInput{$userInput} =~ s/>/\&gt\;/g;
	
	}
}

#inizio a costruire pagina con titolo, contenuto di default e menu di secondo livello
$title = "Inserimento Verbale CCS";
$content = &printFormNewCCS();
$secondLevel = &createSecondLevelMenu();
	
if ($userFormInput{'submit'} eq "Conferma") {
	
	
	#provo a fare upload del file, nel caso vada a buon fine passo all'inserimento del CCS nel file XML
	my $uploadOK = &uploadReport(); 
	if ($uploadOK eq "") {
	
		my $CCSID = &insertNewCCS($userFormInput{'date'}, $userFormInput{'ordineGiorno'}, $userFormInput{'filename'});
		if ($CCSID) {
			$title = "Inserimento Avvenuto";
			$content = &printThanks($CCSID);
		}
		else {
			
			my $directory = substr($userFormInput{'date'}, 6) . substr($userFormInput{'date'}, 3, 2) . substr($userFormInput{'date'}, 0, 2);
			my $upload_dir = $siteForCGI . "documenti/verbaliccs/" . $directory;
			unlink($upload_dir);
			
			$content = &printFormNewCCS("Problemi nell'inserimento nel file XML del Verbale");
		}

	}
	else {
		
		$content = &printFormNewCCS($uploadOK);
	}
	
}
	#sono nella situazione in cui è stata compilata la prima form
if ($userFormInput{'submit'} eq "Inserisci") {
	
	my $errors = &checkInput();
	if ($errors eq "") {
		
		$content = &printFormReportCCS();			
	}
	else {
		
		$content = &printFormNewCCS($errors);			
	}
}


utf8::encode($content);

$template = &openFile($siteForCGI . "reservedzone/reservedtemplate.html") or die "$!";
	
$content = $secondLevel . $content;
	
$template =~ s/<pageContent\/>/$content/g;
$template =~ s/<pageTitle\/>/$title/g;
	
print <<CONTENT;
Content-type:text/html\n\n
$template

CONTENT

