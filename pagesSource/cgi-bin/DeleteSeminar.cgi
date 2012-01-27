#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use utf8;

require "GlobalVariables.pl";
require "WorkWithFiles.pl";
require "CreateSecondLevelMenu.cgi";
require "FunctionsSeminary.cgi";

sub printFormSeminarDelete() {
	
	my $message = $_[0];
	if ($message ne "") {
		
		$message = "<div id=\"message\">$message</div>";	
	}
	my $optionSeminar = &getSeminarOption();
		
	my $content = <<CONTENT;
<div id="contents">
	<h1>Elimina Seminario</h1>
	$message
	<form method="post" action="DeleteSeminar.cgi">
	<fieldset>
	<legend>Seminario</legend>
	<label for="idSeminar">Seleziona Seminario: </label>
	<select id="idSeminar" name="idSeminar" >
		$optionSeminar
	</select>
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" class="button" value="Elimina" name="submit" />
	</fieldset>
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

$userFormInput{'submit'} = $page->param('submit');

$title = "Elimina Seminario";
$content = &printFormSeminarDelete();
$secondLevel = &createSecondLevelMenu();

if ($userFormInput{'submit'} eq "Elimina") {
	
	$userFormInput{'idSeminar'} = $page->param('idSeminar');
	
	my $result = &deleteSeminar($userFormInput{'idSeminar'});
	
	if ($result) {
		
		$content = &printFormSeminarDelete("Eliminazione Eseguita");
	}
	else {
		
		$content = &printFormSeminarDelete("Problemi nell'eliminazione. Riprovare");
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
