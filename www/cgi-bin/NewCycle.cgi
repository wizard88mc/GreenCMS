#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use utf8;

require "GlobalVariables.pl";
require "WorkWithFiles.pl";
require "CreateSecondLevelMenu.cgi";
require "FunctionsPHDStudents.cgi";

sub printFormNewCycle() {
	
	my $message = $_[0];
	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Nuovo Ciclo</h1>
	$message
	<form method="post" action="NewCycle.cgi" >
	<fieldset>
	<legend>Informazioni</legend>
	<label for="name">Nome Ciclo: </label>
	<input type="text" id="name" name="name" value="$userFormInput{'name'}" />
	<label for="byear">Anno inizio: </label>
	<input type="text" name="byear" id="byear" value="$userFormInput{'byear'}" />
	<label for="eyear">Anno fine: </label>
	<input type="text" name="eyear" id="eyear" value="$userFormInput{'eyear'}"/>
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" name="submit" value="Inserisci" class="button"  />
	</fieldset>
	</form>
</div>
CONTENT
	
	return $content;
}

sub checkInput() {
	
	my $errors = "";

	if (length($userFormInput{'name'}) < 3) {
		$errors .= "Nome ciclo non corretto (meno di 3 caratteri)<br />";
	}
	if ($userFormInput{'byear'} !~ /\d{4}/) {
		$errors .= "Anno di inizio errato<br />";
	}
	if ($userFormInput{'eyear'} !~ /\d{4}/) {
		$errors .= "Anno di fine errato<br />";
	}
	if ($userFormInput{'byear'} >= $userFormInput{'eyear'}) {
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

$title = "Inserisci nuovo ciclo";
$content = &printFormNewCycle();
$secondLevel = &createSecondLevelMenu();

if ($userFormInput{'submit'} eq "Inserisci") {
	
	$userFormInput{'name'} = $page->param('name');
	$userFormInput{'byear'} = $page->param('byear');
	$userFormInput{'eyear'} = $page->param('eyear');
	
	foreach $userInput (keys %userFormInput) {
		if ($userFormInput{$userInput} eq 0) {
			$userFormInput{$userInput} = "";
		}
		utf8::decode($userFormInput{$userInput});
		$userFormInput{$userInput} =~ s/\&/\&amp\;/g;
		$userFormInput{$userInput} =~ s/</\&lt\;/g;
		$userFormInput{$userInput} =~ s/>/\&gt\;/g;
		
	}

	my $errors = &checkInput();
	if ($errors eq "") {
		
		my $result = &insertNewCycle(\%userFormInput);
		if ($result) {
			$content = &printFormNewCycle("Inserimento Avvenuto");
		}
		else {
			$content = &printFormNewCycle("Problemi nell'inserimento. Riprovare");
		}
		
	}
	else {
		
		$content = &printFormNewCycle($errors);
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


