#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use utf8;

binmode STDERR, ":utf8";

require "GlobalVariables.pl";
require "WorkWithFiles.pl";
require "FunctionsUploadTesi.cgi";

my $upload_dir = $siteForCGI . "private/presentazionimagistrale";

$CGI::POST_MAX = 1024 * 10000000;


#stringa per la stampa della form per l'upload della presentazione
sub formUploadPresentation() {
	
	my $formString = <<CONTENT;
<form method="post" action="UploadPresentation.cgi" enctype="multipart/form-data">
	<fieldset>
	<legend>Dati Personali</legend>
	<div class="notes">
	<h1>Dati Personali</h1>
	<p class="last">Inserisci Nome, Cognome e Numero di Matricola (xxxxxx) che hai inserito al momento del caricamento della tesi.Solo in caso di corrispondenza potrai caricare la presentazione</p>
	</div>
	<label for="name">Nome: </label>
	<input type="text" name="name" id="name" value="$userFormInput{'name'}" />
	<label for="surname">Cognome: </label>
	<input type="text" name="surname" id="surname" value="$userFormInput{'surname'}" />
	<label for="matricola">Matricola: </label>
	<input type="text" name="matricola" id="matricola" value="$userFormInput{'matricola'}" />
	</fieldset>
	<fieldset>
	<legend>Presentazione</legend>
	<label for="filePresentation">File Presentazione: </label>
	<input type="file" name="filePresentation" id="filePresentation" />
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" name="submit" value="Carica" class="button" />
	</fieldset>
</form>
CONTENT
	
	return $formString;
	
}


sub checkInputs() {
	
	my $errors = "";
	
	#nome deve avere almeno tre caratteri ed essere solo caratteri, no numeri
	if ($userFormInput{'name'} !~ /^\D{3}(\D)*$/ || (&checkBadContent($userFormInput{'name'}) ne "")) {
    	$errors .= "Nome inserito non corretto<br />";
    }
    #uguale al nome
    if ($userFormInput{'surname'} !~ /^\D{3}(\D)*$/ || (&checkBadContent($userFormInput{'surname'}) ne "")) {
    	$errors .= "Cognome inserito non corretto<br />";
    }
    #matricola deve essere di sei numeri e basta
    if ($userFormInput{'matricola'} !~  /^\d{6}$/ || (&checkBadContent($userFormInput{'matricola'}) ne "")) {
    	$errors .= "Numero matricola errato<br />";
    }
    
    return $errors;
    
}

sub checkBadContent() {
	
	my $string = $_[0];

	if (index($string, "<?") != -1 || index($string, "?>") != -1 || index($string, "<\%") != -1 || index($string, "\%>") != -1
		|| index($string, "<script") != -1 || index($string, "</script") != -1) {
		return "bad";
		}

}

#carico presentazione
sub uploadPresentation() {
	
	my $safe_filename_characters = "a-zA-Z0-9_.-";
	my ( $name, $path, $extension ) = fileparse($userFormInput{'filePresentation'}, '\..*' );
	
	$extension = substr($extension, rindex($extension, '.'));
	my $filename = $name . $extension; 
	if ($filename eq "") {
		return "File non inserito";
	} 
	#controllo che l'estensione sia quella corretta
	if (index($extension, ".pdf") == -1 && index($extension, ".ppt") == -1 && index($extension, ".pptx") == -1 && index($extension, ".odp") && index($extension, ".otp") && index($extension, ".pps") && index($extension, ".ppsx")) {
		return "Formato file non corretto"; 
	}

	#stesso lavoro delle tesi
	$filename = $userFormInput{'matricola'} . $userFormInput{'surname'} . $extension;
	
	my $upload_filehandle = $page->upload("filePresentation"); 
 
	open ( UPLOADFILE, ">$upload_dir/$filename" ) or die "$!";  
	binmode UPLOADFILE; 
 
	while ( my $bytes_read = read($upload_filehandle, my $buffer, 1024) ) {  
		print UPLOADFILE $buffer;
	}  
	
	close UPLOADFILE; 
	
	chmod(0664, "$upload_dir/$filename");
	
	my $cmd = "chgrp www-data $upload_dir/$filename";
	system($cmd);
	
	return "";	
	
	
}


{
	
	$page = new CGI;
	#apro il file di template per la pagina di upload
	my $pageTemplateUpload = &openFile($siteForCGI . "laureamagistrale/uploadpresentazioni.html");
	
	#modifico i link per farlo corrispondere al path corretto
	my $srcPath = "src=\"../";
	my $hrefPath = "href=\"../";
	my $newSRC = "src=\"/$folderBase";
	my $newHREF = "href=\"/$folderBase";
	my $folder = "laureamagistrale/";
	
	my $ulSecond = index($pageTemplateUpload, "div id=\"contents");
	my $endSecond = index($pageTemplateUpload, "/ul", $ulSecond);
	my $href = index($pageTemplateUpload, "href=\"", $ulSecond);
	
	
	while ($href != -1 && $href < $endSecond) {
		
		my $endLink = index($pageTemplateUpload, "\"", $href + length("href=\""));
		my $link = substr($pageTemplateUpload, $href, $endLink - $href);
		if (index($link, '.cgi') == -1) {
			substr($pageTemplateUpload, $href, length("href=\""), "href=\"/$folderBase" . $folder);
		}
		
		$href = index($pageTemplateUpload, "href=\"", $href + length("href=\"") + 5);
		
	}
	
	$pageTemplateUpload =~ s/$srcPath/$newSRC/g; 
	$pageTemplateUpload =~ s/$hrefPath/$newHREF/g; 


	if (index($pageTemplateUpload, "<formUploadPresentation/>") != -1) {
			
		$userFormInput{'submit'} = $page->param('submit');
		
		my $form = "<h3>Caricamento Presentazione</h3>";
		
		#utente ha cliccato su bottone di caricamento
		if ($userFormInput{'submit'} eq "Carica") {
			
			$userFormInput{'name'} = $page->param('name');
			$userFormInput{'surname'} = $page->param('surname');
			$userFormInput{'matricola'} = $page->param('matricola');
			$userFormInput{'filePresentation'} = $page->param('filePresentation');
			
			foreach my $userInput (keys %input) {
				if ($input{$userInput} eq 0) {
					$input{$userInput} = "";
				}
				utf8::decode($input{$userInput});
				$input{$userInput} =~ s/\&/\&amp;/g;
				$input{$userInput} =~ s/</\&lt\;/g;
				$input{$userInput} =~ s/>/\&gt\;/g;
			}
			
			$form = $form . &formUploadPresentation();
			#verifico errori nell'input
			my $errors = &checkInputs();	
			
			if ($errors eq "") {
			
				#controllo che a dati inseriti corrisponda una tesi inserita
				my $checkMatricola = &checkMatricola($userFormInput{'matricola'}, $userFormInput{'name'}, $userFormInput{'surname'});
				
				if ($checkMatricola eq "") {
					
					my $tryUpload = &uploadPresentation();
					if ($tryUpload eq "") {
						$form = "<p>Inserimento avvenuto correttamente</p>";
					}
					else {
						$form = "<div id=\"message\">$tryUpload</div>$form";
					}
				}
				else {
					$form = "<div id=\"message\">$checkMatricola</div>$form";
				}
			}
			else {
				$form = "<div id=\"message\">$errors</div>$form";
			}
		}
		else {
		    $form = $form . &formUploadPresentation();
		}
		
		utf8::encode($form);
		
		$pageTemplateUpload =~ s/<formUploadPresentation\/>/$form/;
	}
	else {	
		#nessuna form attiva
		my $textNotActive = "<p>La form per l'inserimento della presentazione per gli appelli di laurea non è al momento disponibile</p>";
		
		utf8::encode($textNotActive);
		
		$pageTemplateUpload =~ s/<formNonAttiva\/>/$textNotActive/g; 			
		
	}


print <<CONTENT;
Content-type:text/html\n\n
$pageTemplateUpload

CONTENT



}


