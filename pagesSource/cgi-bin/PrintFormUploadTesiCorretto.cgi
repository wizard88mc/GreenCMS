#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use DBI;
use DBD::mysql;
use HTML::Entities;
use utf8;

binmode STDIN, ":utf8";
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";

require "WorkWithFiles.pl";
require "GlobalVariables.pl";
require "FunctionsUploadTesi.cgi";

$CGI::POST_MAX = 1024 * 10000000;

#costruisco la stringa per la form di upload di una tesi
sub formInsertTesi() {
	
	my $formString = 
"<form method=\"post\" action=\"PrintFormUploadTesi.cgi\" enctype=\"multipart/form-data\">
	<fieldset>
	<legend>Dati Personali</legend>
	<div class=\"notes\">
	<h1>Dati Personali</h1>
	<p class=\"last\">Inserisci Nome, Cognome e Numero di Matricola (xxxxxx)</p>
	</div>
	<label for=\"name\">Nome: </label>
	<input type=\"text\" name=\"name\" id=\"name\" value=\"$input{'name'}\" />
	<label for=\"surname\">Cognome: </label>
	<input type=\"text\" name=\"surname\" id=\"surname\" value=\"$input{'surname'}\" />
	<label for=\"matricola\">Matricola: </label>
	<input type=\"text\" name=\"matricola\" id=\"matricola\" value=\"$input{'matricola'}\" />
	</fieldset>
	<fieldset>
	<legend>Informazioni Tesi</legend>
	<div class=\"notes\">
	<h1>Informazioni tesi</h1>
	<p>Titolo della tesi per intero</p>
	<p>File della tesi solo in formato pdf</p>
	<p>Abstract: breve riassunto della tesi proposta</p>
	<p class=\"last\">Specifica se appartieni alla Laurea Magistrale o alla Laurea Specialistica</p>
	</div>
	<label for=\"titleTesi\">Titolo della Tesi: </label>
	<input type=\"text\" name=\"titleTesi\" id=\"titleTesi\" value=\"$input{'titleTesi'}\" />
	<label for=\"fileTesi\">File della Tesi: </label>
	<input type=\"file\" name=\"fileTesi\" id=\"fileTesi\" />
	<label for=\"abstract\">Abstract: </label>
	<textarea name=\"abstract\" id=\"abstract\" cols=\"20\" rows=\"8\" >$input{'abstract'}</textarea>
	<br /><br />
	<input type=\"radio\" name=\"laurea\" id=\"radioLM\" value=\"LM\" checked=\"checked\" />
	<label for=\"radioLM\">Laurea Magistrale</label><br /><br />
	<input type=\"radio\" name=\"laurea\" id=\"radioLS\" value=\"LS\" />
	<label for=\"radioLS\">Laurea Specialistica</label>
	</fieldset>
	<fieldset>
	<legend></legend>
	<input type=\"submit\" name=\"submit\" value=\"Carica\" class=\"button\" />
	<input type=\"reset\" value=\"Reset\" class=\"button\" />
	</fieldset>
</form>";
	
	return $formString;
	
	
}

#stringa per la stampa della form per l'upload della presentazione
sub formUploadPresentation() {
	
	my $formString = 
"<form method=\"post\" action=\"PrintFormUploadTesi.cgi\" enctype=\"multipart/form-data\">
	<fieldset>
	<legend>Dati Personali</legend>
	<div class=\"notes\">
	<h1>Dati Personali</h1>
	<p class=\"last\">Inserisci Nome, Cognome e Numero di Matricola (xxxxxx) che hai inserito al momento del caricamento della tesi.Solo in caso di corrispondenza potrai caricare il file</p>
	</div>
	<label for=\"name\">Nome: </label>
	<input type=\"text\" name=\"name\" id=\"name\" value=\"$input{'name'}\" />
	<label for=\"surname\">Cognome: </label>
	<input type=\"text\" name=\"surname\" id=\"surname\" value=\"$input{'surname'}\" />
	<label for=\"matricola\">Matricola: </label>
	<input type=\"text\" name=\"matricola\" id=\"matricola\" value=\"$input{'matricola'}\" />
	</fieldset>
	<fieldset>
	<legend>Presentazione</legend>
	<label for=\"filePresentation\">File Presentazione: </label>
	<input type=\"file\" name=\"filePresentation\" id=\"filePresentation\" />
	</fieldset>
	<fieldset>
	<legend></legend>
	<input type=\"submit\" name=\"submit\" value=\"Carica\" class=\"button\" />
	</fieldset>
</form>";
	
	
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
	if ($input{'name'} !~ /^\D{3}(\D)*$/ || (&checkBadContent($input{'name'}) ne "")) {
    	$errors .= "Nome inserito non corretto<br />";
    }
    #uguale al nome
    if ($input{'surname'} !~ /^\D{3}(\D)*$/ || (&checkBadContent($input{'surname'}) ne "")) {
    	$errors .= "Cognome inserito non corretto<br />";
    }
    #matricola deve essere di sei numeri e basta
    if ($input{'matricola'} !~  /^\d{6}$/ || (&checkBadContent($input{'matricola'}) ne "")) {
    	$errors .= "Numero matricola errato<br />";
    }
    if (defined($input{'titleTesi'}) && (length($input{'titleTesi'}) < 5 || &checkBadContent($input{'titleTesi'}))) {
    	$errors .= "Titolo della tesi errato<br />";
    }
    if (defined($input{'abstract'}) && (length($input{'abstract'}) < 20 || &checkBadContent($input{'abstract'}))) {
    	$errors .= "Abstract errato<br />";
	}
	
	
	return $errors;
	
}

#carica il file della tesi
sub uploadFile() {
	
	my $safe_filename_characters = "a-zA-Z0-9_.-";
	my ( $name, $path, $extension ) = fileparse($input{'fileTesi'}, '\..*' );  
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
	
	#do nome al file come matricola e cognome
	$filename = $input{'matricola'} . $input{'surname'} . $extension;
	
	#upload del file
	my $upload_filehandle = $page->upload("fileTesi"); 
	
	$input{'fileTesi'} = $filename;
	
	my $upload_dir = "../private/tesimagistrale/";
 
	#scrivo file nella directory corretta
	open ( UPLOADFILE, ">$upload_dir/$filename" ) or die "$!";  
	binmode UPLOADFILE;  
 
	while ( my $bites_read = read($upload_filehandle, my $buffer, 1024) ) {  
		print UPLOADFILE $buffer;  
	}  
	
	close UPLOADFILE; 
	
	chmod(0664, "$upload_dir/$filename");
	
	return "";
}

#carico presentazione
sub uploadPresentation() {
	
	my $safe_filename_characters = "a-zA-Z0-9_.-";
	my ( $name, $path, $extension ) = fileparse($input{'filePresentation'}, '\..*' );  
	my $filename = $name . $extension; 
	if ($filename eq "") {
		return "File non inserito";
	} 
	#controllo che l'estensione sia quella corretta
	if (index($extension, ".ppt") == -1 && index($extension, ".pptx") == -1 && index($extension, ".odp") && index($extension, ".otp") && index($extension, ".pps") && index($extension, ".ppsx")) {
		return "Formato file non corretto"; 
	}

	#stesso lavoro delle tesi
	$filename = $input{'matricola'} . $input{'surname'} . $extension;
	
	my $upload_filehandle = $page->upload("filePresentation"); 
	
	my $upload_dir = "../private/presentazionimagistrale/";
 
	open ( UPLOADFILE, ">$upload_dir/$filename" ) or die "$!";  
	binmode UPLOADFILE;  
 
	while ( <$upload_filehandle> ) {  
		print UPLOADFILE;  
	}  
	
	close UPLOADFILE; 
	
	chmod(0664, "$upload_dir/$filename");
	
	return "";	
	
	
}


{
	#apro il file di template per la pagina di upload
	my $pageTemplateUpload = &openFile("../laureamagistrale/uploadtesi.html");	
	
	#modifico i link per farlo corrispondere al path corretto
	my $srcPath = "src=\"../";
	my $hrefPath = "href=\"../";
	my $newSRC = "src=\"$sitePath";
	my $newHREF = "href=\"$sitePath";
	
	#modifico link del menu di secondo livello
	my $linkOrario = $sitePath . "laureamagistrale/orario.html";
	my $linkIndirizzi = $sitePath . "laureamagistrale/indirizzimagistrale.html";
	my $linkCorsi = $sitePath . "laureamagistrale/corsimagistrale.html";
	my $linkPianoStudi = $sitePath . "laureamagistrale/pianostudimagistrale.html";
	my $linkTesi = $sitePath . "laureamagistrale/tesimagistrale.html";
	my $linkAppelliLaurea = $sitePath . "laureamagistrale/appellilaureamagistrale.html";
	my $linkReferenti = $sitePath . "laureamagistrale/referentimagistrale.html";
	my $linkEsami = $sitePath . "laureamagistrale/esamimagistrale.html";
	my $oldIndex = "href=\"index.html\"";
	my $newIndex = "href=\"/testing/laureamagistrale/index.html\"";
	
	$pageTemplateUpload =~ s/$oldIndex/$newIndex/g;
	$pageTemplateUpload =~ s/orariomagistrale.html/$linkOrario/g;
	$pageTemplateUpload =~ s/indirizzimagistrale.html/$linkIndirizzi/g;
	$pageTemplateUpload =~ s/corsimagistrale.html/$linkCorsi/g;
	$pageTemplateUpload =~ s/esamimagistrale.html/$linkEsami/g;
	$pageTemplateUpload =~ s/pianostudimagistrale.html/$linkPianoStudi/g;
	$pageTemplateUpload =~ s/tesimagistrale.html/$linkTesi/g;
	$pageTemplateUpload =~ s/appellilaureamagistrale.html/$linkAppelliLaurea/g;
	$pageTemplateUpload =~ s/referentimagistrale.html/$linkReferenti/g;
	
	$pageTemplateUpload =~ s/$srcPath/$newSRC/g; 
	$pageTemplateUpload =~ s/$hrefPath/$newHREF/g; 
	
	#devo stampare form per upload delle tesi
	if (index($pageTemplateUpload, "<formUploadTesi/>") != -1) {

		$page = new CGI;
		$input{'name'} = $page->param('name');
		$input{'surname'} = $page->param('surname');
		$input{'matricola'} = $page->param('matricola');
		$input{'titleTesi'} = $page->param('titleTesi');
		$input{'fileTesi'} = $page->param('fileTesi');
		$input{'abstract'} = $page->param('abstract');
		$input{'laurea'} = $page->param('laurea');
		$input{'submit'} = $page->param('submit');
		
		my $form = &formInsertTesi();
		
		#utente ha cliccato sul bottone submit
		if ($input{'submit'} eq "Carica") {
			#verifico eventuali errori nell'input
			my $errors = &checkInputs();
			
			if ($errors eq "") {
				
				#provo ad uploadare il file
				my $tryUpload = &uploadFile();
				
				#non ci sono errori
				if ($tryUpload eq "") {
					
					#inserisco tesi in file xml
					&insertNewTesi(\%input);
					$form = "<p>Inserimento avvenuto correttamente</p>";
				}
				else {
					$form = "<div id=\"message\">$tryUpload</div>$form";
				}
			}
			else {
				
				$form = "<div id=\"message\">$errors</div>$form";
			}
		}
		
		$pageTemplateUpload =~ s/<formUploadTesi\/>/$form/;
		
	}
	else {
		
		#stampo form per upload presentazioni
		if (index($pageTemplateUpload, "<formUploadPresentation/>") != -1) {
			
			$page = new CGI;
			$input{'name'} = $page->param('name');
			$input{'surname'} = $page->param('surname');
			$input{'matricola'} = $page->param('matricola');
			$input{'filePresentation'} = $page->param('filePresentation');
			$input{'submit'} = $page->param('submit');
			
			my $form = "<h3>Caricamento Presentazione</h3>" . &formUploadPresentation();
			
			#utente ha cliccato su bottone di caricamento
			if ($input{'submit'} eq "Carica") {
				
				#verifico errori nell'input
				my $errors = &checkInputs();	
				
				if ($errors eq "") {
				
					#controllo che a dati inseriti corrisponda una tesi inserita
					my $checkMatricola = &checkMatricola($input{'matricola'}, $input{'name'}, $input{'surname'});
					
					if ($checkMatricola eq "") {
						
						#provo a caricare file
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
			
			$pageTemplateUpload =~ s/<formUploadPresentation\/>/$form/;
			
		}
		else {
		
			#nessuna form attiva
			my $textNotActive = "<p>La form per l'inserimento degli abstract per gli appelli di laurea non &egrave; al momento disponibile</p>";
		
			$pageTemplateUpload =~ s/<formNonAttiva\/>/$textNotActive/g; 			
	
		}
		
	}
			
print <<PAGE;
Content-type: text/html\n\n
$pageTemplateUpload

PAGE
	
}

