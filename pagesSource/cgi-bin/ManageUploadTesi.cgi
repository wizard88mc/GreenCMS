#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use CGI::Session;
use CGI::Cookie;
use utf8;

require "GlobalVariables.pl";
require "CreateSecondLevelMenu.cgi";
require "WorkWithFiles.pl";


sub updateState() {
	
	eval {
		my $change = $_[0];

		my $pageTemplateThesis = &openFile($siteForCGI . "laureamagistrale/uploadtesi.html");
		my $pageTemplatePresentation = &openFile($siteForCGI . "laureamagistrale/uploadpresentazioni.html");

		if ($change eq "12") {
			
			$pageTemplateThesis =~ s/<formNonAttiva\/>/<formUploadTesi\/>/g;
		}
		if ($change eq "13") {
			
			$pageTemplatePresentation =~ s/<formNonAttiva\/>/<formUploadPresentation\/>/g;
		}
		
		if ($change eq "1") {
			
			$pageTemplateThesis =~ s/<formUploadTesi\/>/<formNonAttiva\/>/g;
			$pageTemplatePresentation =~ s/<formUploadPresentation\/>/<formNonAttiva\/>/g;
		}
		
		my $pageThesis = $siteForCGI . "laureamagistrale/uploadtesi.html";
		my $pagePresentation = $siteForCGI . "laureamagistrale/uploadpresentazioni.html";
		
		open FILE, ">$pageThesis" or die "$!";
		print FILE "$pageTemplateThesis";
		close (FILE);
		
		open FILE, ">$pagePresentation" or die "$!";
		print FILE "$pageTemplatePresentation";
		close (FILE);
		
		return 1;
	}
	or do { return 0; }
		
}

sub printFormUploadState() {

	my $message = $_[0];
	
	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Gestione Upload Tesi</h1>
	$message
	<form method="post" action="ManageUploadTesi.cgi">
	<fieldset>
	<legend>Operazione</legend>
	<label for="operation">Seleziona operazione: </label>
	<select id="operation" name="operation" >
		<option value="1">Chiudi qualsiasi upload</option>
		<option value="12">Abilita Upload Tesi</option>
		<option value="13">Abilita Upload Presentazioni</option>
	</select>
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" name="submit" value="Aggiorna" class="button" />
	<input type="reset" name="reset" value="Reset" class="button" />
	</form>
</div>
CONTENT

	return $content;
}

$page = new CGI;

$cookie = $page->cookie("CGISESSIONID") || undef;
if (!defined($cookie)) {
	print $page->redirect($siteForCGI . $folderBase . "reservedzone/login.html");
}

$input{'submit'} = $page->param('submit');
$input{'operation'} = $page->param('operation');

$title = "Gestione Upload Tesi";
$content = &printFormUploadState();
$secondLevel = &createSecondLevelMenu();


if ($input{'submit'} eq "Aggiorna") {
	
	my $result = &updateState($input{'operation'});
	if ($result) {
		$content = &printFormUploadState("Aggiornamento Avvenuto");
	}
	else {
		$content = &printFormUploadState("Aggiornamento non riuscito. Riprovare");
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

	
	
