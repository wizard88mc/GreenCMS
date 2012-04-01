#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use CGI::Session;
use CGI::Cookie;
use utf8;

require "GlobalVariables.pl";
require "WorkWithFiles.pl";
require "CreateSecondLevelMenu.cgi";
require "FunctionsPHDStudents.cgi";

sub printFormChoosePHDStudent() {
	
	my $message = $_[0];
	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}
	
	my $phdOptions = &getPHDList();
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Modifica Dottorando</h1>
	$message
	<form method="post" action="EditPHDStudent.cgi">
	<fieldset>
	<legend>Selezione Dottorando</legend>
	<label for="idStudent">Seleziona Dottorando da modificare: </label>
	<select name="idStudent" id="idStudent">
	$phdOptions
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

sub printFormEditStudentDetails() {
	
	my $studentID = $_[0];
	my $message = $_[1];
	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}
	
	my %studentInformations = &getUserDetails($studentID);
	my %supervisorHash = &getSupervisorHash();
	my %cycleHash = &getCycleHash();
	
	my $stringSupervisor = "";
	
	while (my ($id, $name)=each(%supervisorHash)) {
		
		if ($id eq $studentInformations{'supervisor'}) {
			$stringSupervisor .= "<option value=\"$id\" selected=\"selected\">$name</option>";
		}
		else {
			$stringSupervisor .= "<option value=\"$id\">$name</option>";
		}
	}
	
	my $stringCycle = "";
	while (my ($id, $name)=each(%cycleHash)) {
		
		if ($id eq $studentInformations{'cycle'}) {
			$stringCycle .= "<option value=\"$id\" selected=\"selected\">$name</option>";
		}
		else {
			$stringCycle .= "<option value=\"$id\">$name</option>";
		}
	}
	
	my $english = "";
	if ($studentInformations{'lang'} eq "en") {
		$english = "<input type=\"checkbox\" name=\"lang\" id=\"lang\" value=\"en\" checked=\"checked\" />";
	}
	else {
		$english = "<input type=\"checkbox\" name=\"lang\" id=\"lang\" value=\"en\" />";
	}
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Modifica Informazioni</h1>
	<form method="post" action="EditPHDStudent.cgi" >
	$message
	<fieldset>
	<legend>Informazioni Generali</legend>
	<label for="name">Nome: </label>
	<input type="text" name="name" id="name" value="$studentInformations{'name'}" />
	<label for="surname">Cognome: </label>
	<input type="text" name="surname" id="surname" value="$studentInformations{'surname'}" />
	<label for="website">Sito web: </label>
	<input type="text" name="website" id="website" value="$studentInformations{'website'}" />	
	</fieldset>
	<fieldset>
	<legend>Informazioni Dettagliate</legend>
	<label for="researchArea">Area di Ricerca</label>
	<textarea id="researchArea" name="researchArea" cols="20" rows="8" >$studentInformations{'researchArea'}</textarea><br />
	$english
	<label for="lang">Lingua area ricerca: Inglese</label>
	<br /><br />
	<label for="supervisor">Supervisore</label>
	<select name="supervisor" id="supervisor" >
	<option value=""> - - - </option>
	$stringSupervisor
	</select><br /><br />
	<label for="cycle">Ciclo: </label>
	<select name="cycle" id="cycle" >
	<option value=""> - - - </option>
	$stringCycle
	</select><br /><br />
	<input type="hidden" name="idStudent" value="$studentID" />
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" class="button" name="submit" value="Modifica" />
	<input type="submit" class="button" name="submit" value="Annulla" />
	</fieldset>

	</form>
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
	
    if (length($userFormInput{'researchArea'}) < 5) {
    	$errors .= "Area di ricerca non inserita";
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
	$userFormInput{'researchArea'} = $page->param('researchArea');
	$userFormInput{'lang'} = $page->param('lang');
	$userFormInput{'idStudent'} = $page->param('idStudent');
	$userFormInput{'supervisor'} = $page->param('supervisor');
	$userFormInput{'cycle'} = $page->param('cycle');
	
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

$title = "Modifica Dottorando";
$content = &printFormChoosePHDStudent();
$secondLevel = &createSecondLevelMenu();


if ($userFormInput{'submit'} eq "Modifica") {
	
	my $errors = &checkErrors();
	if ($errors eq "") {
		
		my $result = &modifyPHDStudent(\%userFormInput);
		
		if ($result) {
			
			$content = &printFormChoosePHDStudent("Operazione Completata");
		}
		else {
			
			$content = &printFormEditStudentDetails($userFormInput{'idStudent'}, "Problema nell'aggiornamento. Riprovare");
		}
	}
	else {
		
		$content = &printFormEditStudentDetails($userFormInput{'idStudent'}, $errors);
	}
}
	
if ($userFormInput{'submit'} eq "Seleziona") {
		
	$content = &printFormEditStudentDetails($userFormInput{'idStudent'});

}

utf8::decode($content);

$template = &openFile($siteForCGI . "reservedzone/reservedtemplate.html") or die "$!";
	
$content = $secondLevel . $content;
	
$template =~ s/<pageContent\/>/$content/g;
$template =~ s/<pageTitle\/>/$title/g;
	
print <<CONTENT;
Content-type:text/html\n\n
$template

CONTENT











