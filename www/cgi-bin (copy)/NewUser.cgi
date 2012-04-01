#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use utf8;

require "GlobalVariables.pl";
require "WorkWithFiles.pl";
require "CreateSecondLevelMenu.cgi";
require "FunctionsAdmin.cgi";

sub printFormNewUser() {
	
	my $message = $_[0];
	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}
	
	my $content = <<CONTENT;
<div id="contents">	
	<h1>Inserimento nuovo <span xml:lang="en">User</span></h1>
	$message
	<form method="post" action="NewUser.cgi">
	<fieldset>
	<legend>Dettagli Utente</legend>
	<label for="name">Nome: </label>
	<input type="text" name="name" id="name" value="$userFormInput{'name'}" />
	<label for="surname">Cognome: </label>
	<input type="text" name="surname" id="surname" value="$userFormInput{'surname'}" />
	<label for="userID">Nome Utente: </label>
	<input type="text" name="userID" id="userID" value="$userFormInput{'userID'}" />
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" name="submit" value="Inserisci" class="button" />
	<input type="reset" name="reset" value="Reset" class="button" />
	</fieldset>
	</form>
</div>
CONTENT

	return $content;

}

sub printReport() {
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Riepilogo Informazioni</h1>
	<form method="post" action="NewUser.cgi">
	<fieldset>
	<legend>Riepilogo</legend>
	<p><strong>Nome: </strong> $userFormInput{'name'} </p>
	<p><strong>Cognome: </strong> $userFormInput{'surname'} </p>
	<p><strong>Username: </strong>$userFormInput{'userID'} </p>
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" name="submit" value="Conferma" class="button" />
	<input type="submit" name="submit" value="Indietro" class="button" />
	<input type="hidden" name="name" value="$userFormInput{'name'}" />
	<input type="hidden" name="surname" value="$userFormInput{'surname'}" />
	<input type="hidden" name="userID" value="$userFormInput{'userID'}" />
	</form>
</div>
CONTENT

	return $content;
}

sub printThanks() {

	my $content = <<CONTENT;	
<div id="contents">	
	<h1>Operazione Completata</h1>
	<p>Operazione eseguita correttamente</p>
</div>
CONTENT

	return $content;
}

sub checkErrors() {
	
	my $errors = "";
	if ($userFormInput{'name'} !~ /^\D{3}(\D)*$/) {
    	$errors .= "Nome inserito non corretto<br />";
    }
    if ($userFormInput{'surname'} !~ /^\D{3}(\D)*$/) {
    	$errors .= "Cognome inserito non corretto<br />";
    }
    
    if (length($userFormInput{'userID'}) < 3) {
    	$errors .= "Nome utente non corretto";
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
	$userFormInput{'userID'} = $page->param('userID');
	
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

$title = "Nuovo User";
$content = &printFormNewUser();
$secondLevel = &createSecondLevelMenu();

if ($userFormInput{'submit'} eq "Conferma") {
	
	my $result = &insertNewUser(\%userFormInput);
	if ($result) {
		
		$content = &printThanks();
	}
	else {
		
		$content = $content = &printFormNewUser("Impossibile eseguire operazione. Riprovare");
	}
	
}
if ($userFormInput{'submit'} eq "Inserisci") {
	
	$errors = &checkErrors();
	
	if ($errors eq "") {
		
		$title = "Riepilogo Informazioni";
		$content = &printReport();			
	}
	else {
		
		$content = &printFormNewUser($errors);
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
