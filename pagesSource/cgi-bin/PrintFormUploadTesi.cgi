#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use utf8;

binmode STDERR, ":utf8";

require "GlobalVariables.pl";
require "WorkWithFiles.pl";
require "FunctionsUploadTesi.cgi";

my $upload_dir = $siteForCGI . "private/tesimagistrale";

$CGI::POST_MAX = 1024 * 10000000;

#costruisco la stringa per la form di upload di una tesi
sub formInsertTesi() {
    
    my $optionsRelatore = &getOptionsRelatore();
	
	my $formString = <<CONTENT;
<form method="post" action="PrintFormUploadTesi.cgi" enctype="multipart/form-data">
	<fieldset>
	<legend>Dati Personali</legend>
	<div class="notes">
	<h1>Dati Personali</h1>
	<p class="last">Inserisci Nome, Cognome e Numero di Matricola (xxxxxx)</p>
	</div>
	<label for="name">Nome: </label>
	<input type="text" name="name" id="name" value="$userFormInput{'name'}" />
	<label for="surname">Cognome: </label>
	<input type="text" name="surname" id="surname" value="$userFormInput{'surname'}" />
	<label for="matricola">Matricola: </label>
	<input type="text" name="matricola" id="matricola" value="$userFormInput{'matricola'}" /><br />
	</fieldset>
	<fieldset>
	<legend>Informazioni Tesi</legend>
	<div class="notes">
	<h1>Informazioni tesi</h1>
	<p>Titolo della tesi per intero</p>
	<p>File della tesi solo in formato pdf</p>
	<p>Abstract: breve riassunto della tesi proposta</p>
	<p class="last">Specifica se appartieni alla Laurea Magistrale o alla Laurea Specialistica</p>
	</div>
	<label for="relatore">Relatore: </label>
	<select name="relatore" id="relatore">
	    $optionsRelatore
	</select>
	<label for="titleTesi">Titolo della Tesi: </label>
	<input type="text" name="titleTesi" id="titleTesi" value="$userFormInput{'titleTesi'}" />
	<label for="fileTesi">File della Tesi: </label>
	<input type="file" name="fileTesi" id="fileTesi" />
	<label for="abstract">Abstract: </label>
	<textarea name="abstract" id="abstract" cols="20" rows="8" >$userFormInput{'abstract'}</textarea>
	<br /><br />
	<input type="checkbox" name="lang" value="en" id="lang" />
	<label for="lang">Tesi in inglese</label>
	<input type="radio" name="laurea" id="radioLM" value="LM" checked="checked" />
	<label for="radioLM">Laurea Magistrale</label><br /><br />
	<input type="radio" name="laurea" id="radioLS" value="LS" />
	<label for="radioLS">Laurea Specialistica</label>
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" name="submit" value="Carica" class="button" />
	<input type="reset" value="Reset" class="button" />
	</fieldset>
</form>
CONTENT

	return $formString;
	
	
}


#controlla che il contenuto degli input di tipo testo non abbia qualcosa che non va bene
sub checkBadContent() {
	
	my $string = $_[0];

	if (index($string, "<?") != -1 || index($string, "?>") != -1 || index($string, "<\%") != -1 || index($string, "\%>") != -1
		|| index($string, "<script") != -1 || index($string, "</script") != -1) {
		return "bad";
		}

}

#funziona che controlla che gli input inseriti siano corretti rispetto a determinate specifiche
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
    if (($userFormInput{'matricola'} !~  /^\d{6}$/ && $userFormInput{'matricola'} !~  /^\d{7}$/) || (&checkBadContent($userFormInput{'matricola'}) ne "")) {
    	$errors .= "Numero matricola errato<br />";
    }
    if (defined($userFormInput{'titleTesi'}) && (length($userFormInput{'titleTesi'}) < 5 || &checkBadContent($userFormInput{'titleTesi'}))) {
    	$errors .= "Titolo della tesi errato<br />";
    }
    if (defined($userFormInput{'abstract'}) && (length($userFormInput{'abstract'}) < 20 || &checkBadContent($userFormInput{'abstract'}))) {
    	$errors .= "Abstract errato<br />";
	}
	
	
	return $errors;
	
}

#carica il file della tesi
sub uploadFile {
	
	my $safe_filename_characters = "a-zA-Z0-9_.-";
	my ($name, $path, $extension ) = fileparse($page->param('fileTesi'), '\..*' );  
	$extension = substr($extension, rindex($extension, '.'));
	$name = $page->param('matricola') . $page->param('surname');
	my $filename = $name . $extension; 
	
	#controlla che il file sia stato inserito
	if ($filename eq "") {
		return "File non inserito";
	} 
	
	#controllo che l'estensione sia pdf
	if (index($extension, ".pdf") == -1) {
		return "Formato file non corretto"; 
	}
	
	#controllo che il file non abbia caratteri strani
	$filename =~ tr/ /_/;  
	$filename =~ s/[^$safe_filename_characters]//g;  
	
	if ( $filename =~ /^([$safe_filename_characters]+)$/ ) {  
		$filename = $1;  
	}  
	else {  
		return "File mal rinominato";  
	}
		
	#upload del file
	my $upload_filehandle = $page->upload('fileTesi'); 
	
	$userFormInput{'fileTesi'} = $filename;
 
	my $outfile = $upload_dir . "/" . $filename;
	
	#scrivo file nella directory corretta
	open ( UPLOADFILE, ">$outfile" ) or die "$!";  
        binmode UPLOADFILE;

	while ( my $bytes_read = read($upload_filehandle, my $buffer, 1024 )) {
		print UPLOADFILE $buffer;  
	}  
	
	close UPLOADFILE; 
	
	chmod(0664, "$upload_dir/$filename");
	rename($outfile, "$upload_dir/$filename");
	
	my $cmd = "chgrp www-data $upload_dir/$filename";
	system($cmd);
	
	return "";
}


{

    $page = new CGI;
	#apro il file di template per la pagina di upload
	my $pageTemplateUpload = &openFile($siteForCGI . "laureamagistrale/uploadtesi.html");
	
	#modifico i link per farli corrispondere al path corretto
	my $srcPath = "src=\"../";
	my $hrefPath = "href=\"../";
	my $newSRC = "src=\"/$folderBase";
	my $newHREF = "href=\"/$folderBase";
	my $folder = "laureamagistrale/";
	
	my $ulSecond = index($pageTemplateUpload, "div id=\"contents");
	my $endSecond = index($pageTemplateUpload, "</ul>", $ulSecond);
	my $href = index($pageTemplateUpload, "href=\"", $ulSecond);
	
	
	while ($href != -1 && $href < $endSecond) {
		
		my $endLink = index($pageTemplateUpload, "\"", $href + length("href=\""));
		my $link = substr($pageTemplateUpload, $href, $endLink - $href);
		if (index($link, '.cgi') == -1) {
			substr($pageTemplateUpload, $href, length("href=\""), "href=\"/$folderBase" . $folder);
		}
		
		$href = index($pageTemplateUpload, "href=\"", $href + 1);
		
	}
	
	$pageTemplateUpload =~ s/$srcPath/$newSRC/g; 
	$pageTemplateUpload =~ s/$hrefPath/$newHREF/g; 
	
	#devo stampare form per upload delle tesi
	if (index($pageTemplateUpload, "<formUploadTesi/>") != -1) {

		$userFormInput{'submit'} = $page->param('submit');
		
		my $form = &formInsertTesi();
		
		#utente ha cliccato sul bottone submit
		if ($userFormInput{'submit'} eq "Carica") {
			
			$userFormInput{'name'} = $page->param('name');
			$userFormInput{'surname'} = $page->param('surname');
			$userFormInput{'matricola'} = $page->param('matricola');
			$userFormInput{'relatore'} = $page->param('relatore');
			$userFormInput{'titleTesi'} = $page->param('titleTesi');
			$userFormInput{'fileTesi'} = $page->param('fileTesi');
			$userFormInput{'abstract'} = $page->param('abstract');
			$userFormInput{'laurea'} = $page->param('laurea');
			$userFormInput{'lang'} = $page->param('lang');
				
			foreach my $userInput (keys %userFormInput) {
				if ($userFormInput{$userInput} eq 0) {
					$userFormInput{$userInput} = "";
				}
				utf8::decode($userFormInput{$userInput});
				$userFormInput{$userInput} =~ s/\"/''/g;
				$userFormInput{$userInput} =~ s/\&/\&amp;/g;
				$userFormInput{$userInput} =~ s/</\&lt\;/g;
				$userFormInput{$userInput} =~ s/>/\&gt\;/g;
			}
			
			#verifico eventuali errori nell'input
			my $errors = &checkInputs();
			
			if ($errors eq "") {
				
				#provo ad uploadare il file
				my $tryUpload = &uploadFile();
				
				#non ci sono errori
				if ($tryUpload eq "") {
					
					#inserisco tesi in file xml
					&insertNewTesi(\%userFormInput);
					$form = "<p>Inserimento avvenuto correttamente</p>";
				}
				else {
				    $form = &formInsertTesi();
					$form = "<div id=\"message\">$tryUpload</div>$form";
				}
			}
			else {
			    $form = &formInsertTesi();
				$form = "<div id=\"message\">$errors</div>$form";
			}
		}
		
		utf8::encode($form);
		
		$pageTemplateUpload =~ s/<formUploadTesi\/>/$form/;
		
	}
	else {	
		#nessuna form attiva
		my $textNotActive = "<p>La form per l'inserimento degli abstract per gli appelli di laurea non è al momento disponibile</p>";
		
		utf8::encode($textNotActive);
		
		$pageTemplateUpload =~ s/<formNonAttiva\/>/$textNotActive/g; 			
		
	}
	
	

print <<CONTENT;
Content-type:text/html\n\n
$pageTemplateUpload

CONTENT

}
