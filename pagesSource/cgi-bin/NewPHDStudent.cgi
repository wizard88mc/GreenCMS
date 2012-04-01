#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use utf8;

#binmode STDIN, ":utf8";
#binmode STDOUT, ":utf8";
#binmode STDERR, ":utf8";

require "GlobalVariables.pl";
require "WorkWithFiles.pl";
require "CreateSecondLevelMenu.cgi";
require "FunctionsPHDStudents.cgi";

sub printFormNewPHDStudent() {
	
	my $message = $_[0];
	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}
	
	my $supervisorList = &getSupervisorList();
	my $cycleList = &getCyclesList();
	
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Inserisci nuovo Dottorando</h1>
	$message
	<form method="post" action="NewPHDStudent.cgi">
	<fieldset>
	<legend>Informazioni Generali</legend>
	<label for="name">Nome: </label>
	<input type="text" name="name" id="name" value="$userFormInput{'name'}" />
	<label for="surname">Cognome: </label>
	<input type="text" name="surname" id="surname" value="$userFormInput{'surname'}" />
	<label for="website">Sito web: </label>
	<input type="text" name="website" id="website" value="$userFormInput{'website'}" />	
	</fieldset>
	<fieldset>
	<legend>Informazioni Dettagliate</legend>
	<label for="researchArea">Area di Ricerca</label>
	<textarea id="researchArea" name="researchArea" cols="20" rows="8" >$userFormInput{'researchArea'}</textarea><br />
	<input type="checkbox" name="lang" value="en" id="lang" />
	<label for="lang">Lingua area ricerca: Inglese</label>
	<br /><br />
	<label for="supervisor">Supervisore</label>
	<select name="supervisor" id="supervisor" >
	<option value=""> - - - </option>
	$supervisorList
	</select><br /><br />
	<label for="cycle">Ciclo: </label>
	<select name="cycle" id="cycle" >
	<option value=""> - - - </option>
	$cycleList
	</select><br /><br />
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" class="button" name="submit" value="Inserisci" />
	<input type="reset" class="button" value="Annulla" />
	</fieldset>
	</form>
</div>
CONTENT

	return $content;
}

sub printReport() {
	
	my $supervisor = &getSupervisorName($userFormInput{'supervisor'});
	my $cycle = &getCycle($userFormInput{'cycle'});
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Controlla informazioni</h1>
	<form method="post" action="NewPHDStudent.cgi">
	<fieldset>
	<legend>Report</legend>
	<p><strong>Nome: </strong>$userFormInput{'name'}</p>
	<p><strong>Cognome: </strong>$userFormInput{'surname'}</p>
	<p><strong>Sito web: </strong>$userFormInput{'website'}</p>
	<p><strong>Area di ricerca: </strong>$userFormInput{'researchArea'}</p>
	<p><strong>Supervisore: </strong>$supervisor</p>
	<p><strong>Ciclo: </strong>$cycle</p>
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" value="Conferma" name="submit" class="button" />
	<input type="submit" value="Indietro" name="submit" class="button" />
	<input type="hidden" name="name" value="$userFormInput{'name'}" />
	<input type="hidden" name="surname" value="$userFormInput{'surname'}" />
	<input type="hidden" name="website" value="$userFormInput{'website'}" />
	<input type="hidden" name="researchArea" value="$userFormInput{'researchArea'}" />
	<input type="hidden" name="supervisor" value="$userFormInput{'supervisor'}" />
	<input type="hidden" name="cycle" value="$userFormInput{'cycle'}" />
	<input type="hidden" name="lang" value="$userFormInput{'lang'}" />
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


$title = "Inserisci Nuovo Dottorando";
$content = &printFormNewPHDStudent();
$secondLevel = &createSecondLevelMenu();


if ($userFormInput{'submit'} eq "Conferma") {
	
	$userFormInput{'name'} = $page->param('name');
	$userFormInput{'surname'} = $page->param('surname');
	$userFormInput{'website'} = $page->param('website');
	$userFormInput{'researchArea'} = $page->param('researchArea');
	$userFormInput{'supervisor'} = $page->param('supervisor');
	$userFormInput{'cycle'} = $page->param('cycle');
	$userFormInput{'lang'} = $page->param('lang');

	foreach $userInput (keys %userFormInput) {
		if ($userFormInput{$userInput} eq 0) {
			$userFormInput{$userInput} = "";
		}
		utf8::decode($userFormInput{$userInput});
		$userFormInput{$userInput} =~ s/\&/\&amp\;/g;
		$userFormInput{$userInput} =~ s/</\&lt\;/g;
		$userFormInput{$userInput} =~ s/>/\&gt\;/g;
		
	}

	
	my $result = &insertNewPHDStudent(\%userFormInput);
	if ($result) {
		$title = "Inserimento Avvenuto";
		$content = &printThanks();
	}
	else {
		$title = "Errore";
		$content = &printFormNewPHDStudent("Errore nell'inserimento. Riprovare");
	}
	
}
if ($userFormInput{'submit'} eq "Inserisci") {
		
	$userFormInput{'name'} = $page->param('name');
	$userFormInput{'surname'} = $page->param('surname');
	$userFormInput{'website'} = $page->param('website');
	$userFormInput{'researchArea'} = $page->param('researchArea');
	$userFormInput{'supervisor'} = $page->param('supervisor');
	$userFormInput{'cycle'} = $page->param('cycle');
	$userFormInput{'lang'} = $page->param('lang');
		
	foreach $userInput (keys %userFormInput) {
		if ($userFormInput{$userInput} eq 0) {
			$userFormInput{$userInput} = "";
		}
		utf8::decode($userFormInput{$userInput});
		$userFormInput{$userInput} =~ s/\&/\&amp\;/g;
		$userFormInput{$userInput} =~ s/</\&lt\;/g;
		$userFormInput{$userInput} =~ s/>/\&gt\;/g;
		
	}


	my $error = &checkError();
	if ($error eq "") {
		$title = "Verifica Informazioni";
		$content = &printReport();
		
	}
	else {
	
		$content = &printFormNewPHDStudent($error);
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







