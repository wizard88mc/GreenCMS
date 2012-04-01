#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use utf8;

require "GlobalVariables.pl";
require "WorkWithFiles.pl";
require "CreateSecondLevelMenu.cgi";
require "FunctionsDocuments.cgi";

sub printFormDeleteDocument() {
	
	my $message = $_[0];
	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}
	
	my $documentOptions = &getDocumentsOptions();
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Inserimento nuovo Documento</h1>
	$message
	<form method="post" action="DeleteDocument.cgi">
	<fieldset>
	<legend>Selezione Documento</legend>
	<label for="documentID">Documento da eliminare: </label>
	<select id="documentID" name="documentID" t>
	$documentOptions
	</select>
	</fieldset>
	<fieldset>
	<input type="submit" name="submit" value="Elimina" class="button" />
	</fieldset>
	</form>
</div>
CONTENT

	return $content;
}

sub deleteDocument() {
	
	eval {
		my $documentID = $userFormInput{'documentID'};	
		
		my $filename = &cancelDocument($documentID);
		
		my $fileToDelete = $siteForCGI . "documenti/" . $filename;
		
		unlink($fileToDelete);
		
		return 1;
	}
	or do { return 0; }
	
}

$page = new CGI;

$cookie = $page->cookie("CGISESSIONID") || undef;
if (!defined($cookie)) {
	print $page->redirect($siteForCGI . $folderBase . "reservedzone/login.html");
}

$userFormInput{'submit'} = $page->param('submit');

$secondLevel = &createSecondLevelMenu();
$title = "Elimina Documento";
$content = &printFormDeleteDocument();

if ($userFormInput{'submit'} eq "Elimina") {
	
	$userFormInput{'documentID'} = $page->param('documentID');
	
	my $result = &deleteDocument();
	if ($result) {
		$content = &printFormDeleteDocument("Eliminazione Avvenuta");
	}
	else {
		$content = &printFormDeleteDocument("Problemi nell'eliminazione. Riprovare");
	}
		
}

utf8::encode($content);

my $template = &openFile($siteForCGI . "reservedzone/reservedtemplate.html") or die "$!";

$content = $secondLevel . $content;

$template =~ s/<pageContent\/>/$content/g;
$template =~ s/<pageTitle\/>/$title/g;
	
print <<CONTENT;
Content-type:text/html\n\n
$template

CONTENT

