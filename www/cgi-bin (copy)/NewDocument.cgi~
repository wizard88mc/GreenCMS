#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use CGI::Session;
use CGI::Cookie;
use utf8;

require "GlobalVariables.pl";
require "WorkWithFiles.pl";
require "CreateSecondLevelMenu.cgi";
require "FunctionsDocuments.cgi";

$CGI::POST_MAX = 1024 * 10000000;

sub printFormAddDocument() {
	
	my $message = $_[0];
	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Inserimento Nuovo Documento</h1>
	$message
	<form method="post" action="NewDocument.cgi" enctype="multipart/form-data" accept-charset="UTF-8">
	<fieldset>
	<legend>Inserimento Documento</legend>
	<span><strong>Attenzione: Form non funzionante con accenti e IE</strong></span>
	<label for="textFile">Descrizione File</label>
	<input type="text" name="textFile" id="textFile" value="$userFormInput{'textFile'}" />
	<label for="fileUpload">Seleziona File</label>
	<input type="file" name="fileUpload" id="fileUpload" />
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" value="Inserisci" name="submit" class="button" />
	</fieldset>
	</form>
	
</div>
CONTENT

	return $content;
}

sub loadDocument() {
	
	eval {
		if (length($userFormInput{'textFile'}) < 5) {
			return "Descrizione del file non valida";
		}
		
		my $safe_filename_characters = "a-zA-Z0-9_.-";
		my ( $name, $path, $extension ) = fileparse($userFormInput{'fileUpload'}, '\..*' );  
		my $filename = $name . $extension;
		
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
		
		my $upload_dir = $siteForCGI . "documenti";
		
		my $upload_filehandle = $page->upload("fileUpload");
		
		open ( UPLOADFILE, ">$upload_dir/$filename" ) or die "$!";  
		binmode UPLOADFILE;
		
		while ( my $bytesread = read($upload_filehandle, my $buffer, 1024)) {  
			print UPLOADFILE $buffer;  
		}  
		
		close UPLOADFILE;  
		
		chmod(0665, "$upload_dir/$filename");
		
		my $result = &insertDocument($filename, $userFormInput{'textFile'});
		
		if ($result) {
			$userFormInput{'textFile'} = "";
			return "Inserimento Avvenuto";
		}
		else {
			return "Problemi nel caricamento. Riprovare";
		}
	}
	or do { return "Problemi nel caricamento. Riprovare"; }
	
	
}

$page = new CGI;

$cookie = $page->cookie("CGISESSIONID") || undef;
if (!defined($cookie)) {
	print $page->redirect($siteForCGI . $folderBase . "reservedzone/login.html");
}

$userFormInput{'submit'} = $page->param('submit');


$title = "Carica Documento";
$content = &printFormAddDocument();
$secondLevel = &createSecondLevelMenu();

if ($userFormInput{'submit'} eq "Inserisci") {

	$userFormInput{'textFile'} = $page->param('textFile');
	$userFormInput{'fileUpload'} = $page->param('fileUpload');
	foreach $userInput (keys %userFormInput) {
		if ($userFormInput{$userInput} eq 0) {
			$userFormInput{$userInput} = "";
		}
		utf8::decode($userFormInput{$userInput});
		$userFormInput{$userInput} =~ s/\&/\&amp\;/g;
		$userFormInput{$userInput} =~ s/</\&lt\;/g;
		$userFormInput{$userInput} =~ s/>/\&gt\;/g;
		
	}
	
	my $result = &loadDocument();
	$content = &printFormAddDocument($result);
	
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


