#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use CGI::Session;
use CGI::Cookie;
use utf8;

require "GlobalVariables.pl";
require "CreateSecondLevelMenu.cgi";
require "WorkWithFiles.pl";
require "FunctionsPHDStudents.cgi";

sub printFormChooseSupervisor() {

	my $message = $_[0];
	
	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}
	
	my $supervisorList = &getSupervisorList();
	
	my $content = <<CONTENT;
	
<div id="contents">
	<h1>Modifica Supervisore</h1>
	$message
	<form action="EditSupervisor.cgi" method="post">
	<fieldset>
	<legend>Seleziona Supervisore</legend>
	<label for="supervisorID">Supervisore: </label>
	<select name="supervisorID" id="supervisorID">
	$supervisorList
	</select>
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" name="submit" value="Seleziona" class="button" />
	</fieldset>	
	</form>
</div>
CONTENT

	return $content;

}



sub printFormEditSupervisor() {
	
	my $supervisorID = $_[0];
	my $message = $_[0];
	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}
	
	my %informations = &getSupervisorDetails($supervisorID);
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Informazioni Supervisore</h1>
	<form action="EditSupervisor.cgi" method="post">
	<fieldset>
	<legend>Informazioni</legend>
	<label for="name">Nome: </label>
	<input type="text" name="name" id="name" value="$informations{'name'}" /><br />
	<label for="surname">Cognome: </label>
	<input type="text" name="surname" id="surname" value="$informations{'surname'}" /><br />
	<label for="website">Sito internet: </label>
	<input type="text" name="website" id="website" value="$informations{'website'}" /><br />
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" name="submit" value="Modifica" class="button" />
	<input type="submit" name="submit" value="Indietro" class="button" />
	<input type="hidden" name="supervisorID" value="$supervisorID" />
	</fieldset>
	</form>
</div>
CONTENT
}

sub checkInput() {
	
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


$title = "Modifica Supervisore";
$content = &printFormChooseSupervisor();
$secondLevel = &createSecondLevelMenu();

if ($userFormInput{'submit'} ne 0) {
	
	$userFormInput{'name'} = $page->param('name');
	$userFormInput{'surname'} = $page->param('surname');
	$userFormInput{'website'} = $page->param('website');
	$userFormInput{'supervisorID'} = $page->param('supervisorID');
	
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

if ($userFormInput{'submit'} eq "Modifica") {
		
	my $errors = &checkInput();
	
	if ($errors eq "") {
		
		my $result = &editSupervisor(\%userFormInput);
		
		if ($result) {
			
			$content = &printFormChooseSupervisor("Operazione Completata");
		}
		else {
			
			$content = &printFormEditSupervisor($userFormInput{'supervisorID'}, "Aggiornamento non riuscito. Riprovare");
		}
	}
	else {
		
		$content = &printFormEditSupervisor($userFormInput{'supervisorID'}, $errors);
	}
}

if ($userFormInput{'submit'} eq "Seleziona") {
		
	$content = &printFormEditSupervisor($userFormInput{'supervisorID'});
	
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




