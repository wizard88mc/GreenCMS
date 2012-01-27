#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use utf8;

require "GlobalVariables.pl";
require "WorkWithFiles.pl";
require "CreateSecondLevelMenu.cgi";
require "FunctionsSeminary.cgi";


sub printFormContactDetails() {

	my $message = $_[0];
	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}

	my $content = <<CONTENT;
<div id="contents">
	<h1>Informazioni Contatto</h1>
	$message
	<form method="post" action="NewContact.cgi">
	<fieldset>
	<legend>Informazioni</legend>
	<label for="contactName">Nome: </label>
	<input type="text" name="contactName" id="contactName" value="$userFormInput{'contactName'}" /><br />
	<label for="contactSurname">Cognome: </label>
	<input type="text" name="contactSurname" id="contactSurname" value="$userFormInput{'contactSurname'}" /><br />
	<label for="contactEmail">email: </label>
	<input type="text" name="contactEmail" id="contactEmail" value="$userFormInput{'contactEmail'}" /><br />
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

sub printReport() {
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Riepilogo Nuovo Contatto</h1>
	<form method="post" action="NewContact.cgi">
		<fieldset>
		<legend>Report</legend>
		<p><strong>Nome: </strong>$userFormInput{'contactName'}</p>
		<p><strong>Cognome: </strong>$userFormInput{'contactSurname'}</p>
		<p><strong>Email: </strong>$userFormInput{'contactEmail'}</p>
		</fieldset>
		<fieldset>
		<legend class="hidden">Bottoni</legend>
		<input type="submit" name="submit" class="button" value="Conferma" />
		<input type="submit" class="button" name="submit" value="Indietro" />
		</fieldset>
		<input type="hidden" name="contactName" value="$userFormInput{'contactName'}" />
		<input type="hidden" name="contactSurname" value="$userFormInput{'contactSurname'}" />
		<input type="hidden" name="contactEmail" value="$userFormInput{'contactEmail'}" />
	</form>
</div>
CONTENT

	return $content;
}

sub printThanks() {

	my $content = <<CONTENT;
<div id="contents">
	<h1>Inserimento Completato</h1>
	<p>L'inserimento è stato eseguito correttamente</p>
</div>
CONTENT

	return $content;
}

sub checkInputs() {

	my $errors = "";
	if ($userFormInput{'contactName'} !~ /^\D{3}(\D)*$/) {
    	$errors .= "Nome inserito non corretto<br />";
    }
    if ($userFormInput{'contactSurname'} !~ /^\D{3}(\D)*$/) {
    	$errors .= "Cognome inserito non corretto<br />";
    }
	if ($userFormInput{'contactEmail'} !~ /^([\w\-\+\.]+)([\w]+)\@([\w]+)([\w\-\+\.]+)\.([\w\-\+\.]+)$/) {
    	$errors .= "Email inserita non corretta<br />";
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
	
	$userFormInput{'contactName'} = $page->param('contactName');
	$userFormInput{'contactSurname'} = $page->param('contactSurname');
	$userFormInput{'contactEmail'} = $page->param('contactEmail');
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


$title = "Inserisci Nuovo Contatto";
$content = &printFormContactDetails();
$secondLevel = &createSecondLevelMenu();

if($userFormInput{'submit'} eq "Conferma") { 
	
	my $result = &insertNewContact($userFormInput{'contactName'}, $userFormInput{'contactSurname'}, $userFormInput{'contactEmail'});
	if ($result) {
		$content = &printThanks();
	}
	else {
		$content = &printFormContactDetails("Problemi nell'inserimento del contatto. Riprovare");
	}
	
}

if($userFormInput{'submit'} eq "Inserisci") {
		
	my $errors = &checkInputs();
	if ($errors eq "") {
		$title = "Rivedi Informazioni";
		$content = &printReport();
	
	}
	else {
		$content = &printFormContactDetails($errors);
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


