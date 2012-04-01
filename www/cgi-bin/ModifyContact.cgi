#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use utf8;

require "GlobalVariables.pl";
require "WorkWithFiles.pl";
require "CreateSecondLevelMenu.cgi";
require "FunctionsSeminary.cgi";

sub printFormChooseContact() {

	my $message = $_[0];
	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}
	my $contactsOptions = &getContactsOptions();
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Modifica Contatto</h1>
	$message
	<form method="post" action="ModifyContact.cgi">
	<fieldset>
	<legend>Seleziona Contatto</legend>
	<label for"idModify">Nome Contatto</label>
	<select id="idModify" name="idModify" >
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
	<form method="post" action="ModifyContact.cgi">
	<fieldset>
	<legend>Informazioni</legend>
	<label for="contactName">Nome: </label>
	<input type="text" name="contactName" id="contactName" value="$informations{'name'}" /><br />
	<label for="contactSurname">Cognome: </label>
	<input type="text" name="contactSurname" id="contactSurname" value="$informations{'surname'}" /><br />
	<label for="contactEmail">email: </label>
	<input type="text" name="contactEmail" id="contactEmail" value="$informations{'email'}" /><br />
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" class="button" name="submit" value="Modifica" />
	<input type="reset" class="button" value="Reset" />
	</fieldset>
	<input type="hidden" name="idModify" value="$contactID" />
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
	
	
}

$title = "Modifica Contatto";
$content = &printFormChooseContact();
$secondLevel = &createSecondLevelMenu();

if ($userFormInput{'submit'} eq "Modifica") {
	

	my $errors = &checkInputs();
	if ($errors eq "") {
	
		my $result = &modifyContact($userFormInput{'idModify'}, $userFormInput{'contactName'}, $userFormInput{'contactSurname'}, $userFormInput{'contactEmail'});
		
		if ($result) {
			
			$content = &printFormChooseContact("Informazioni Aggiornate");
		}
		else {
			
			$content = &printFormModifyContact($userFormInput{'idModify'}, "Problemi nell'aggiornamento. Riprovare");
		}
	
	}
	else {
		
		$title = "Modifica Informazioni";
		$content = &printFormModifyContact($userFormInput{'idModify'}, $errors);
	}
}

if ($userFormInput{'submit'} eq "Seleziona") {

		$title = "Modifica Informazioni";
		$content = &printFormModifyContact($userFormInput{'idModify'});
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


