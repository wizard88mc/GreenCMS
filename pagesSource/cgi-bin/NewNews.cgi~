#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use CGI::Session;
use CGI::Cookie;
use utf8;

require "GlobalVariables.pl";
require "WorkWithFiles.pl";
require "CreateSecondLevelMenu.cgi";
require "FunctionsNews.cgi";

sub printFormInsert() {
	
	my $message = $_[0];
	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}
	my $validDate = $_[1];
	my $expirationDate = $_[2];
	
	my $daysOptionsValid;
	my $monthsOptionsValid;
	my $yearsOptionsValid;
	
	if ($_[1]) {
	    my ($day, $month, $year) = &getDateComponentsFromItalianDate($_[1]);
	    $daysOptionsValid = &getDaysOptions($day);
	    $monthsOptionsValid = &getMonthsOptions($month);
	    $yearsOptionsValid = &getYearsOptions($year);
	}
	else {
	    $daysOptionsValid = &getDaysOptions();
	    $monthsOptionsValid = &getMonthsOptions();
	    $yearsOptionsValid = &getYearsOptions();
	}
	
	my $daysOptionsExpired;
	my $monthsOptionsExpired;
	my $yearsOptionsExpired;
	
	if ($expirationDate) {
	    my ($day, $month, $year) = &getDateComponentsFromItalianDate($expirationDate);
	    $daysOptionsExpired = &getDaysOptions($day);
	    $monthsOptionsExpired = &getMonthsOptions($month);
	    $yearsOptionsExpired = &getYearsOptions($year);
	}
	else {
	    $daysOptionsExpired = &getDaysOptions();
	    $monthsOptionsExpired = &getMonthsOptions();
	    $yearsOptionsExpired = &getYearsOptions();
	}
	
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Inserisci Nuova News</h1>
	$message
	<form method="post" action="NewNews.cgi">
	<fieldset>
	<legend>Informazioni Generali</legend>
	<label for="title">Titolo: </label>
	<input type="text" name="title" id="title" value="$userFormInput{'title'}" /><br />
	<label for="author">Autore: </label>
	<input type="text" name="author" id="author" value="$userFormInput{'author'}" /><br />
	</fieldset>
	<fieldset>
	<legend>Dettagli News</legend>
	<label for="textNews">Testo News: </label>
	<textarea name="textNews" id="textNews" rows="8" cols="20" >$userFormInput{'textNews'}</textarea>
	<br /><br />
	<label for="type">Tipo News: </label>
	<select name="type" id="type" >
		<option value="G">Generale</option>
		<option value="L">Laurea</option>
		<option value="LM">Laurea Magistrale</option>
	</select><br /><br />
	<div>
	<label for="archiveYes">Archivia</label>
	<input type="radio" name="archive" id="archiveYes" value="T" /><br /><br />
	<label for="archiveNo"><strong>Non</strong> Archiviare</label>
	<input type="radio" checked="checked" name="archive" id="archiveNo" value="F" /></div>
	<br /><br />
	<label for="validityDay">News a partire da:</label>
	<select name="validDay" id="validDay">$daysOptionsValid</select>
	<select name="validMonth" id="validMonth">$monthsOptionsValid</select>
	<select name="validYear" id="validYear">$yearsOptionsValid</select><br />
	<label for="expirationDay">Scadenza News: </label>
	<select name="expirationDay" id="expirationDay">$daysOptionsExpired</select>
	<select name="expirationMonth" id="expirationMonth">$monthsOptionsExpired</select>
	<select name="expirationYear" id="expirationYear">$yearsOptionsExpired</select>
	
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
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Riepilogo News</h1>
	<form method="post" action="NewNews.cgi">
		<fieldset>
		<legend>Riepilogo</legend>
		<p><strong>Titolo: </strong>$userFormInput{'title'}</p>
		<p><strong>Autore: </strong>$userFormInput{'author'}</p>
		<p><strong>Tipo News: </strong>$userFormInput{'type'}</p>
		<p><strong>Da Archiviare: </strong>$userFormInput{'archive'}</p>
		<p><strong>Valida a partire dal: </strong>$userFormInput{'validFrom'}</p>
		<p><strong>Fino al: </strong>$userFormInput{'expirationDay'}</p>
		<p><strong>Testo News: </strong>$userFormInput{'textNews'}</p>
		</fieldset>
		<fieldset>
		<legend class="hidden">Bottoni</legend>
		<input type="submit" name="submit" class="button" value="Conferma" />
		<input type="submit" class="button" name="submit" value="Indietro" />
		<input type="hidden" name="title" value="$userFormInput{'title'}" />
		<input type="hidden" name="author" value="$userFormInput{'author'}" />
		<input type="hidden" name="type" value="$userFormInput{'type'}" />
		<input type="hidden" name="archive" value="$userFormInput{'archive'}" />
		<input type="hidden" name="validFrom" value="$userFormInput{'validFrom'}" />
		<input type="hidden" name="expirationDay" value="$userFormInput{'expirationDay'}" />
		<input type="hidden" name="textNews" value="$userFormInput{'textNews'}" />
		</fieldset>
	</form>
</div>
CONTENT

	return $content;

}

sub printThanks() {

	my $content = <<CONTENT;
<div id="contents">
	<h1>News Inserita Correttamente</h1>
	<p>La nuova news è stata inserita nel Database</p>
</div>
CONTENT

	return $content;
}

sub checkInputs() {
	
	my $errors = "";
	if (length($userFormInput{'title'}) < 5) {
    	$errors .= "Titolo troppo corto (meno di 5 caratteri)<br />";
    }
    
    if ($userFormInput{'author'} !~ /^\D{3}(\D)*$/) {
    	$errors .= "Autore non corretto<br />";
    }
    
    if (length($userFormInput{'textNews'}) < 10) {
    	$errors .= "Testo news troppo corto (meno di 10 caratteri)<br />";
    }
    
    my $startDateCorrect = &checkCorrectDate($userFormInput{'validFrom'});
    if ( $startDateCorrect ne true) {
        $errors .= "Data di inizio validità non corretta <br />";   
    }
    
    my $endDateCorrect = &checkCorrectDate($userFormInput{'expirationDay'});
    if ($endDateCorrect ne true) {
        $errors .= "Data di fine validità non corretta <br />";   
    }
    
    if ($startDateCorrect and $endDateCorrect) {
        if (&checkDatesCronologicallyCorrect($userFormInput{'validFrom'}, $userFormInput{'expirationDay'}) ne true) {
            $errors .= "Data di scadenza minore di quella di inizio validità <br />";      
        }
    }
	
	return $errors;
	
}

$page = new CGI;
$content;

$cookie = $page->cookie("CGISESSIONID") || undef;
if (!defined($cookie)) {
	print $page->redirect($siteForCGI . $folderBase . "reservedzone/login.html");
}

$userFormInput{'submit'} = $page->param('submit');

if ($userFormInput{'submit'} ne 0) {
	
	$userFormInput{'title'} = $page->param('title');
	$userFormInput{'author'} = $page->param('author');
	$userFormInput{'textNews'} = $page->param('textNews');
	$userFormInput{'type'} = $page->param('type');
	$userFormInput{'archive'} = $page->param('archive');
	
	foreach $userInput (keys %userFormInput) {
		if ($userFormInput{$userInput} eq 0) {
			$userFormInput{$userInput} = "";
		}
		utf8::decode($userFormInput{$userInput});
		$userFormInput{$userInput} =~ s/\&/\&amp<\;/g;
		$userFormInput{$userInput} =~ s/</\&lt\;/g;
		$userFormInput{$userInput} =~ s/>/\&gt\;/g;
	}
}

$title = "Inserisci Nuova News";
$content = &printFormInsert("", $page->param('validFrom'), $page->param('expirationDay'));
$secondLevel = &createSecondLevelMenu();


if ($userFormInput{'submit'} eq "Conferma") {
	
    $userFormInput{'validFrom'} = $page->param('validFrom');
    $userFormInput{'expirationDay'} = $page->param('expirationDay');
    
	my $result = &insertNews(\%userFormInput);
	if ($result) {
		
		$title = "Inserimento Avvenuto";
		$content = &printThanks();
	}
	else {
		
		$title = "Errore ! ! ";
		$content = &printFormInsert("Problemi nell'inserimento della news. Riprovare");
	}
	
}	
if ($userFormInput{'submit'} eq "Inserisci") {
	
    $userFormInput{'validFrom'} = "" . $page->param('validDay') . "/" . 
	                              $page->param('validMonth') . "/" .
	                              $page->param('validYear');
	$userFormInput{'expirationDay'} = "" . $page->param('expirationDay') . "/" .
	                                  $page->param('expirationMonth') . "/" . 
	                                  $page->param('expirationYear');
    
	my $errors = &checkInputs();
	
	if ($errors eq "") {
		
		$title = "Verifica Informazioni News";
		$content = &printReport();
		
	}
	else {
		
		$content = &printFormInsert($errors);			
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

