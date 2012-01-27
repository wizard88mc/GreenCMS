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

sub printFormChooseCycle() {
	
	my $message = $_[0];

	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}
	
	my $cycleList = &getCyclesList();
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Modifica Ciclo Dottorato</h1>
	$message
	<form action="EditCycle.cgi" method="post">
	<fieldset>
	<legend>Seleziona Ciclo</legend>
	<label for="cycleID">Ciclo Da Modificare</label>
	<select name="cycleID" id="cycleID">
	$cycleList
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


sub printFormEditCycle() {
	
	my $cycleID = $_[0];
	my $message = $_[1];
	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}
	
	my %informations = &getCycleDetails($cycleID);
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Informazioni Ciclo</h1>
	$message
	<form method="post" action="EditCycle.cgi">
	<fieldset>
	<legend>Informazioni</legend>
	<label for="name">Nome Ciclo: </label>
	<input type="text" name="name" id="name" value="$informations{'name'}" /><br />
	<label for="bYear">Anno Inizio: </label>
	<input type="text" name="bYear" id="bYear" value="$informations{'bYear'}" /><br />
	<label for="eYear">Anno Fine: </label>
	<input type="text" name="eYear" id="eYear" value="$informations{'eYear'}" /><br />
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" name="submit" value="Modifica" class="button" />
	<input type="submit" name="submit" value="Indietro" class="button" />
	<input type="hidden" name="cycleID" value="$cycleID" />
	</legend>
	</form>
</div>
CONTENT
	
	
}

sub checkInput() {
	
	my $errors = "";

	if (length($userFormInput{'name'}) < 3) {
		$errors .= "Nome ciclo non corretto (almeno 3 caratteri)<br />";
	}
	if ($userFormInput{'bYear'} !~ /\d{4}/) {
		$errors .= "Anno di inizio errato<br />";
	}
	if ($userFormInput{'eYear'} !~ /\d{4}/) {
		$errors .= "Anno di fine errato<br />";
	}
	if ($userFormInput{'bYear'} >= $userFormInput{'eYear'}) {
		$errors .= "Anno di inizio maggiore di quello di fine<br />";
	}
	return $errors;
	
}


$page = new CGI;

$cookie = $page->cookie("CGISESSIONID") || undef;
if (!defined($cookie)) {
	print $page->redirect($siteForCGI . $folderBase . "reservedzone/login.html");
}

$userFormInput{'submit'} = $page->param('submit');


$title = "Modifica Ciclo Dottorato";
$content = &printFormChooseCycle();
$secondLevel = &createSecondLevelMenu();

if ($userFormInput{'submit'} ne 0) {
	
	$userFormInput{'cycleID'}  = $page->param('cycleID');
	$userFormInput{'name'} = $page->param('name');
	$userFormInput{'bYear'} = $page->param('bYear');
	$userFormInput{'eYear'} = $page->param('eYear');
	
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
		my $result = &editCycle(\%userFormInput);
		
		if ($result) {
			$content = &printFormChooseCycle("Operazione completata.");
		}
		else {
			
			$content = &printFormEditCycle($userFormInput{'cycleID'}, "Operazione non completata. Riprovare");
		}
	}
	else {
		
		$content = &printFormEditCycle($userFormInput{'cycleID'}, $errors);
	}
}

if ($userFormInput{'submit'} eq "Seleziona") {
	
	$content = &printFormEditCycle($userFormInput{'cycleID'});

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




