#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use utf8;

require "GlobalVariables.pl";
require "WorkWithFiles.pl";
require "CreateSecondLevelMenu.cgi";
require "FunctionsSeminary.cgi";


sub printReport() {
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Riepilogo Nuovo Contatto</h1>
	<form method="post" action="EditContacts.cgi">
		<p><strong>Nome: </strong>$userFormInput{'contactName'}</p>
		<p><strong>Cognome: </strong>$userFormInput{'contactSurname'}</p>
		<p><strong>Email: </strong>$userFormInput{'contactEmail'}</p>
		<fieldset>
		<legend class="hidden>Bottoni</legend>
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

sub printThanks() {

	my $content = <<CONTENT;
<div id="contents">
	<h1>Inserimento Completato</h1>
	<p>L'inserimento è stato eseguito correttamente</p>
</div>
</div>
CONTENT

	utf8::encode($content);

	return $content;
}

sub printFormChooseContact() {

	my $message = $_[0];
	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}
	my $contactsOptions = &getContactsOptions();
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Modifica Contatto</h1>
	$errors
	<form method="post" action="EditContacts.cgi">
	<fieldset>
	<legend>Seleziona Contatto</legend>
	<label for"userModify">Nome Contatto</label>
	<select id="userModify" name="userModify" >
		$contactsOptions
	</select>
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" class="button" name="submit" value="Seleziona" />
	</fieldset>
	</form>
</div>
CONTENT

	return $content;

}

sub printFormModifyContact() {

	my $contactID = $_[0];
	my $message = $_[1];
	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}
	my %informations = &getContactInformations($contactID);
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Informazioni Contatto</h1>
	$message
	<form method="post" action="EditContacts.cgi">
	<fieldset>
	<legend>Informazioni</legend>
	<label for="contactName">Nome: </label>
	<input type="text" name="contactName" id="contactName" value="$informations{'contactName'}" /><br />
	<label for="contactSurname">Cognome: </label>
	<input type="text" name="contactSurname" id="contactSurname" value="$informations{'contactSurname'}" /><br />
	<label for="contactEmail">email: </label>
	<input type="text" name="contactEmail" id="contactEmail" value="$informations{'contactEmail'}" /><br />
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" class="button" name="submit" value="Modifica" />
	<input type="submit" class="button" value="Indietro" />
	</fieldset>
	<input type="hidden" name="idModify" value="$contactID" />
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


$title = "Modifica Contatto";
$secondLevel = &createSecondLevelMenu();
$content = &printFormChooseContact();


if ($userFormInput{'submit'} eq "Seleziona") {

	$title = "Modifica Informazioni";
	$content = &printFormModifyContact($userFormInput{'userModify'});
}

if ($userFormInput{'submit'} eq "Modifica") {

	$userFormInput{'userDelete'} = $page->param('userDelete');
	$userFormInput{'userAssociate'} = $page->param('userAssociate');
	$userFormInput{'mailingAssociate'} = $page->param('mailingAssociate');
	$userFormInput{'userModify'} = $page->param('userModify');
	$userFormInput{'idModify'} = $page->param('idModify');
	
	foreach $userInput (keys %userFormInput) {
		if ($userFormInput{$userInput} eq 0) {
			$userFormInput{$userInput} = "";
		}
		utf8::decode($userFormInput{$userInput});
		$userFormInput{$userInput} =~ s/\&/\&amp\;/g;
		$userFormInput{$userInput} =~ s/</\&lt\;/g;
		$userFormInput{$userInput} =~ s/>/\&gt\;/g;
	}


	my $errors = &checkInputs();
	if ($errors eq "") {
	
		my $result = &modifyContact($userFormInput{'idModify'}, $userFormInput{'contactName'}, $userFormInput{'contactSurname'}, $userFormInput{'contactEmail'});
		if ($result) {
			$content = &printFormChooseContact("Informazioni Aggiornate Correttamente");
		}
		else {
			$content = $printFormModifyContact($userFormInput{'userModify'}, "Problemi nell'aggiornamento del profilo. Riprovare");
		}
	}
	else {
	
		$title = "Modifica Informazioni";
		$content = &printFormModifyContact($userFormInput{'userModify'}, $errors);
	}

}

$template = &openFile($siteForCGI . "reservedzone/reservedtemplate.html") or die "$!";
	
$content = $secondLevel . $content;
	
$template =~ s/<pageContent\/>/$content/g;
$template =~ s/<pageTitle\/>/$title/g;
	
print <<CONTENT;
Content-type:text/html\n\n
$template

CONTENT