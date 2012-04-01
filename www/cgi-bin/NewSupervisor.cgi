#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use utf8;

require "GlobalVariables.pl";
require "WorkWithFiles.pl";
require "CreateSecondLevelMenu.cgi";
require "FunctionsPHDStudents.cgi";

sub printFormNewSupervisor() {
	
	my $message = $_[0];
	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}

	my $content = <<CONTENT;
<div id="contents">
	<h1>Inserisci Nuovo Supervisore</h1>
	$message
	<form method="post" action="NewSupervisor.cgi">
	<fieldset>
	<legend>Informazioni</legend>
	<label for="name">Nome: </label>
	<input type="text" name="name" id="name" value="$userFormInput{'name'}" />
	<label for="surname">Cognome: </label>
	<input type="text" name="surname" id="surname" value="$userFormInput{'surname'}" />
	<label for="website">Sito web: </label>
	<input type="text" name="website" id="website" value="$userFormInput{'website'}" />	
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" class="button" name="submit" value="Inserisci" />
	<input type="reset" class="button" value="Annulla" />
	</fieldset>
	</form>
CONTENT

	return $content;

}

sub printReport() {
	
	my $supervisor = &getSupervisorName($userFormInput{'supervisor'});
	my $cycle = &getCycle($userFormInput{'cycle'});
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Controlla informazioni</h1>
	<form method="post" action="NewSupervisor.cgi">
	<fieldset>
	<legend>Report</legend>
	<p><strong>Nome: </strong>$userFormInput{'name'}</p>
	<p><strong>Cognome: </strong>$userFormInput{'surname'}</p>
	<p><strong>Sito web: </strong>$userFormInput{'website'}</p>
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" value="Conferma" name="submit" class="button" />
	<input type="submit" value="Indietro" name="submit" class="button" />
	<input type="hidden" name="name" value="$userFormInput{'name'}" />
	<input type="hidden" name="surname" value="$userFormInput{'surname'}" />
	<input type="hidden" name="website" value="$userFormInput{'website'}" />
	</fieldset>
	</form>
</div>
CONTENT

	return $content;
}

sub printThanks() {
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Operazione completata</h1>
	<p>Inserimento avvenuto completamente</p>
</div>
CONTENT

	return $content;
}

sub checkError() {
	
	my $errors = "";
	if ($userFormInput{'name'} !~ /^\D{3}(\D)*$/) {
    	$errors .= "Nome inserito non corretto<br />";
    }
    if ($userFormInput{'surname'} !~ /^\D{3}(\D)*$/) {
    	$errors .= "Cognome inserito non corretto<br />";
    }
	
	return $errors;
	
}


$page = new CGI;

$cookie = $page->cookie("CGISESSIONID") || undef;
if (!defined($cookie)) {
	print $page->redirect($siteForCGI . $folderBase . "reservedzone/login.html");
}


$userFormInput{'submit'} = $page->param('submit');

if ($userFormInput{'submit'} ne 0) {

	$userFormInput{'name'} = $page->param('name');
	$userFormInput{'surname'} = $page->param('surname');
	$userFormInput{'website'} = $page->param('website');

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


$title = "Inserisci Nuovo Supervisore";
$content = &printFormNewSupervisor();
$secondLevel = &createSecondLevelMenu();

if ($userFormInput{'submit'} eq "Conferma") {

	my $result = &insertNewSupervisor(\%userFormInput);
	
	if ($result) {
		$title = "Inserimento Avvenuto";
		$content = &printThanks();
	}
	else {
		$title = "Errore";
		$content = &printFormNewSupervisor("Problemi nell'inserimento. Riprovare");
	}	
}

if ($userFormInput{'submit'} eq "Inserisci") {
		
	my $error = &checkError();
	if ($error eq "") {
		
		$title = "Verifica Informazioni";
		$content = &printReport();
		
	}
	else {
	
		$content = &printFormNewSupervisor($error);
	}
	
}

utf8::encode($content);

$template = &openFile($siteForCGI . "reservedzone/reservedtemplate.html") or die "$!";
	
$content = $secondLevel . $content;
	
$template =~ s/<pageContent\/>/$content/g;
$template =~ s/<pageTitle\/>/Area Riservata/g;
	
print <<CONTENT;
Content-type:text/html\n\n
$template

CONTENT


