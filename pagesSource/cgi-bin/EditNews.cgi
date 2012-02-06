#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use CGI::Session;
use CGI::Cookie;
use utf8;

require "GlobalVariables.pl";
require "GlobalFunctions.cgi";
require "WorkWithFiles.pl";
require "CreateSecondLevelMenu.cgi";
require "FunctionsNews.cgi";


sub printfFormChooseNews() {
	
	my $message = $_[0];
	if ($message ne "") {
		
		$message = "<div id=\"message\">$message</div>";
	}
	
	my $activeNewsOptions = &getNewsListOptions();
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Modifica News</h1>	
	$message
	<form method="post" action="EditNews.cgi">
	<fieldset>
	<legend>Seleziona News</legend>
	<label for="idEditNews">News da modificare: </label>
	<select name="idEditNews" name="idEditNews">
		$activeNewsOptions
	</select>
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input class="button" type="submit" name="submit" value="Seleziona" class="button" />
	</fieldset>
	</form>
</div>
CONTENT

	return $content;
}


sub printFormEdit() {
	
	my $newsID = $_[0];
	my $message = $_[1];
	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}
	
	my %newsDetails = &getNewsDetails($newsID);
	
	my $optionType = "<option value=\"G\">Generale</option>";
	if ($newsDetails{'type'} eq "L") {
		$optionType .= "<option value=\"L\" selected=\"selected\">Laurea</option>";
	}
	else {
		$optionType .= "<option value=\"L\">Laurea</option>";
	}
	if ($newsDetails{'type'} eq "LM") {
		$optionType .= "<option value=\"LM\" selected=\"selected\">Laurea Magistrale</option>";
	}
	else {
		$optionType .= "<option value=\"LM\">Laurea Magistrale</option>";
	}
	
	my $archive;
	if ($newsDetails{'archive'} eq "T") {
		$archive = "
		<label for=\"archiveYes\">Archivio</label>
		<input type=\"radio\" name=\"archive\" id=\"archiveYes\" value=\"T\" checked=\"checked\" /><br /><br />
		<label for=\"archiveNo\"><strong>Non</strong> Archiviare </label>
		<input type=\"radio\" name=\"archive\" id=\"archiveNo\" value=\"F\" />";
	}
	else {
		$archive = "
		<label for=\"archiveYes\">Archive Yes</label>
		<input type=\"radio\" name=\"archive\" id=\"archiveYes\" value=\"T\" /><br /><br />
		<label for=\"archiveNo\">Archive No</label>
		<input type=\"radio\" name=\"archive\" id=\"archiveNo\" value=\"F\" checked=\"checked\" />";
	}
	
	my ($validDay, $validMonth, $validYear) = &getDateComponentsFromItalianDate($newsDetails{'validFrom'});
	my ($expireDay, $expireMonth, $expireYear) = &getDateComponentsFromItalianDate($newsDetails{'expiration'});
	
	$daysOptionsValid = &getDaysOptions($validDay);
	$monthsOptionsValid = &getMonthsOptions($validMonth); 
	$yearsOptionsValid = &getYearsOptions($validYear);
	
	$daysOptionsExpired = &getDaysOptions($expireDay);
	$monthsOptionsExpired = &getMonthsOptions($expireMonth);
	$yearsOptionsExpired = &getYearsOptions($expireYear);
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Modifica News</h1>	
	$message
	<form method="post" action="EditNews.cgi">
	<fieldset>
	<legend>Informazioni Generali</legend>
	<label for="title">Titolo: </label>
	<input type="text" name="title" id="title" value="$newsDetails{'title'}" /><br />
	<label for="publisher">Autore: </label>
	<input type="text" name="publisher" id="publisher" value="$newsDetails{'publisher'}" /><br />
	</fieldset>
	<fieldset>
	<legend>Dettagli News</legend>
	<label for="textNews">Testo News: </label><input type="button" class="button" value="Aggiungi Link" onClick="addNewLink();" />
	<textarea name="textNews" id="textNews" rows="8" cols="20" >$newsDetails{'textNews'}</textarea><br />
	<br /><br />
	<label for="type">Tipo News: </label>
	<select name="type" id="type" >
		$optionType
	</select>
	<br /><br />
	$archive
	<br /><br />
	<label for="validDay">News a partire da: </label>
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
	<input class="button" type="submit" class="button" name="submit" value="Modifica" />
	<input class="button" type="submit" value="Indietro" />
	</fieldset>
	<input type="hidden" name="idEditNews" value="$newsID" />
	</form>
</div>	
CONTENT

	return $content;
}

sub checkInputs() {
	
	my $errors = "";
	
	if (length($userFormInput{'title'}) < 5) {
    	$errors .= "Titolo troppo corto (meno di 5 caratteri)<br />";
    }
    
    if ($userFormInput{'publisher'} !~ /^\D{3}(\D)*$/) {
    	$errors .= "Autore non corretto<br />";
    }
    
    if (length($userFormInput{'title'}) < 10) {
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
    
    if ($startDateCorrect eq true && $endDateCorrect eq true) {
        if (&checkDatesCronologicallyCorrect($userFormInput{'validFrom'}, $userFormInput{'expirationDay'}) ne true) {
            $errors .= "Data di scadenza minore di quella di inizio validità <br />";      
        }
    }
	
	return $errors;
	
}


$page = new CGI;

$cookie = $page->cookie("CGISESSIONID") || undef;
if (!defined($cookie)) {
	print $page->redirect($siteForCGI . $folderBase . "reservedzone/login.html");
}


$userFormInput{'submit'} = $page->param('submit');


$title = "Modifica News";
$content = &printfFormChooseNews();
$secondLevel = &createSecondLevelMenu();


if ($userFormInput{'submit'} eq "Modifica") {
	
    $userFormInput{'idEditNews'} = $page->param('idEditNews');
	$userFormInput{'title'} = $page->param('title');
	$userFormInput{'publisher'} = $page->param('publisher');
	$userFormInput{'textNews'} = $page->param('textNews');
	$userFormInput{'type'} = $page->param('type');
	$userFormInput{'archive'} = $page->param('archive');
	$userFormInput{'validFrom'} = "" . $page->param('validDay') . "/" . 
	                              $page->param('validMonth') . "/" .
	                              $page->param('validYear');
	$userFormInput{'expirationDay'} = "" . $page->param('expirationDay') . "/" .
	                                  $page->param('expirationMonth') . "/" . 
	                                  $page->param('expirationYear');
	
	foreach $userInput (keys %userFormInput) {
		if ($userFormInput{$userInput} eq 0) {
			$userFormInput{$userInput} = "";
		}
		utf8::decode($userFormInput{$userInput});
		$userFormInput{$userInput} =~ s/\"/''/g;
		$userFormInput{$userInput} =~ s/\&/\&amp\;/g;
		$userFormInput{$userInput} =~ s/</\&lt\;/g;
		$userFormInput{$userInput} =~ s/>/\&gt\;/g;
	}

	my $errors = &checkInputs();
	if ($errors eq "") {
		
		my $result = &editNews(\%userFormInput);
		
		if ($result) {
			
			$title = "Modifica Avvenuta";
			$content = &printfFormChooseNews("Informazioni Aggiornate");
		}
		else {
			
			$title = "Errore";
			$content = &printFormEdit($userFormInput{'idEditNews'}, "Problemi nell'aggiornamento");
		}
	
	}
	else {
		
		$content = &printFormEdit($userFormInput{'idEditNews'}, $errors);			
	}
	
}

if ($userFormInput{'submit'} eq "Seleziona") {
		
	$userFormInput{'idEditNews'} = $page->param('idEditNews');
	
	$content = &printFormEdit($userFormInput{'idEditNews'});
		
}	
	

utf8::encode($content);

my $template = &openFile($siteForCGI . "reservedzone/reservedtemplate.html") or die "$!";
	
$content = $secondLevel . $content;
	
$template =~ s/<pageContent\/>/$content/g;
$template =~ s/<pageTitle\/>/$title/g;
	
print <<CONTENT;
Content-type:text/html\n\n
$template

CONTENT

