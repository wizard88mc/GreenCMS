#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use utf8;

require "GlobalVariables.pl";
require "WorkWithFiles.pl";
require "CreateSecondLevelMenu.cgi";
require "FunctionsSeminary.cgi";
require "SendEventMail.cgi";


sub printReport() {

	my $mailingListName = "";
	
	foreach my $id (@{$userFormInput{'mailingList'}}) {
		$mailingListName .= &getMailingListName($id) . ", ";
	}
	
	my $textWithLinks = $userFormInput{'abstract'};
	$textWithLinks = &removeLinkTags($textWithLinks);
	
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Riepilogo Seminario</h1>
	<form method="post" action="NewSeminary.cgi">
		<fieldset>
		<legend>Report</legend>
		<p><strong>Titolo: </strong>$userFormInput{'title'}</p>
		<p><strong>Data: </strong>$userFormInput{'date'}</p>
		<p><strong>Ora: </strong>$userFormInput{'time'}</p>
		<p><strong>Luogo: </strong>$userFormInput{'place'}</p>
		<p><strong>Relatore: </strong>$userFormInput{'speaker'} ($userFormInput{'affiliazione'})</p>
		<p><strong>CV Relatore: </strong>$userFormInput{'speakerCV'}</p>
		<p><strong>Abstract: </strong>$textWithLinks</p>
		<p><strong>Mailing List: </strong>$mailingListName</p>
		<p><strong>Indirizzi Addizionali: </strong>$userFormInput{'additionalMails'}</p>
		</fieldset>
		<fieldset>
		<legend class="hidden">Bottoni</legend>
		<input type="submit" name="submit" class="button" value="Conferma" />
		<input type="submit" class="button" name="submit" value="Indietro" />
		</fieldset>
		<input type="hidden" name="title" value="$userFormInput{'title'}" />
		<input type="hidden" name="date" value="$userFormInput{'date'}" />
		<input type="hidden" name="time" value="$userFormInput{'time'}" />
		<input type="hidden" name="place" value="$userFormInput{'place'}" />
		<input type="hidden" name="speaker" value="$userFormInput{'speaker'}" />
		<input type="hidden" name="speakerCV" value="$userFormInput{'speakerCV'}" />
		<input type="hidden" name="affiliazione" value="$userFormInput{'affiliazione'}" />
		<input type="hidden" name="abstract" value="$userFormInput{'abstract'}" />
		<input type="hidden" name="lang" value="$userFormInput{'lang'}" />
		<input type="hidden" name="mailingList" value="@{$userFormInput{'mailingList'}}" />
		<input type="hidden" name="additionalMails" value="$userFormInput{'additionalMails'}" />
	</form>
</div>
CONTENT

	return $content;
}


sub printForm() {

	my $message = $_[0];
	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}
	my $mailingList = &getMailingListCheckbox();
	
	my $seminarDate = $_[1];
	my $seminarDayOptions, $seminarMonthOptions, $seminarYearOptions;
	
	if ($seminarDate) {
	     my ($day, $month, $year) = &getDateComponentsFromItalianDate($seminarDate);
	     $seminarDayOptions = &getDaysOptions($day);
	     $seminarMonthOptions = &getMonthsOptions($month);
	     $seminarYearOptions = &getYearsOptions($year);
	}
	else {
	    $seminarDayOptions = &getDaysOptions();
	    $seminarMonthOptions = &getMonthsOptions();
	    $seminarYearOptions = &getYearsOptions();
	}
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Inserisci nuovo seminario</h1>
	$message
	<form method="post" action="NewSeminary.cgi">
	<fieldset>
	<legend>Informazioni Generali</legend>
	<label for="title">Titolo: </label>
	<input type="text" name="title" id="title" value="$userFormInput{'title'}" /><br />
	<label for="dateDay">Data: </label>
	<input type="text" name="dateDay" id="dateDay" value="$seminarDayOptions" />
	<input type="text" name="dateMonth" id="dateMonth" value="$seminarMonthOptions" />
	<input type="text" name="dateYear" id="dateYear" value="$seminarYearOptions" />
	<br />
	<label for="time">Ora: (hh:mm)</label>
	<input type="text" name="time" id="time" value="$userFormInput{'time'}" /><br />
	<label for="place">Luogo: </label>
	<input type="text" name="place" id="place" value="$userFormInput{'place'}" /><br />
	</fieldset>
	<fieldset>
	<legend>Maggiori Informazioni</legend>
	<label class="block" for="speaker">Relatore: </label>
	<input type="text" name="speaker" id="speaker" value="$userFormInput{'speaker'}" /><br />
	<label for="affiliazione">Affiliazione: </label>
	<input type="text" name="affiliazione" id="affiliazione" value="$userFormInput{'affiliazione'}" /><br />
	<label class="block" for="abstract">Abstract: </label><input type="button" class="button" value="Aggiungi link" onClick="addNewLinkSeminary()" />
	<textarea id="abstract" name="abstract" cols="50" rows="5" >$userFormInput{'abstract'}</textarea><br />
	<label for="speakerCV">CV Relatore: </label>
	<textarea id="speakerCV" name="speakerCV" cols="50" rows="5" >$userFormInput{'speakerCV'}</textarea><br />
	<input type="checkbox" name="lang" id="lang" value="en" />
	<label for="lang">Campi compilati in inglese</label><br /><br />
	</fieldset>
	<fieldset>
	<legend>Mailing List</legend>
	$mailingList
	<br />
	<label for="additionalMails">Indirizzi Addizionali (separati da virgola)</label>
	<input type="text" name="additionalMails" id="additionalMails" value="$userFormInput{'additionalMails'}" />
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

sub printThanks() {

	my $count = $_[0];
	my $content = <<CONTENT;
<div id="contents">
	<h1>Seminario Inserito Correttamente</h1>
	<p>Il seminario è stato inserito correttamente - $count email inviate</p>
</div>
CONTENT

	return $content;
}


sub checkInputs() {

	my $errors = "";
	if ($userFormInput{'title'} eq "") {
    	$errors .= "Titolo non corretto<br />";
    }
    
    if (&checkCorrectDate($userFormInput{'date'}) ne true) {
        $errori .= 'Giorno di seminario errato<br />';   
    }
	
	if ($userFormInput{'time'} =~ m/^\d{2}\:\d{2}$/) {
    	my $hour = substr($userFormInput{'time'}, 0, 2);
		my $minute = substr($userFormInput{'time'}, 3);
		if (($hour < 8) || ($userFormInput > 22) || $minute < 0 || minute > 59) {
			$errors .= "Orario non corretto (hh:mm)<br />";
		}
    }
	else {
		$errors .= "Formato ora non corretto<br />";
	}
	
	if ($userFormInput{'place'} !~ /^.{3}(.)*$/) {
    	$errors .= "Luogo del seminario non corretto<br />";
    }

	if ($userFormInput{'speaker'} !~ /^\D{3}(\D)*$/) {
    	$errors .= "Relatore non corretto<br />";
    }
    
    if ($userFormInput{'mailingList'} == 0) {
    	$errors .= "Nessuna Mailing List Selezionata<br />";
    }
    
    if (length($userFormInput{'additionalMails'}) != 0) {
    	
    	my @mails = split(',', $userFormInput{'additionalMails'});
    	my $mailsErrors = 0;
    	
    	foreach my $mail (@mails) {
    		$mail =~ s/^\s+//;
    		$mail =~ s/\s+$//;
    		if ($mail !~ /^([\w\-\+\.]+)([\w]+)\@([\w]+)([\w\-\+\.]+)\.([\w\-\+\.]+)$/) {
    			$mailsErrors += 1;
    		}
    	}
    	
    	if ($mailsErrors != 0) {
    		$errors .= "Indirizzi addizionali non corretti";
    	}
    	
    	
    }
	
	return $errors;
}


$page = new CGI;

#$cookie = $page->cookie("CGISESSIONID") || undef;
#if (!defined($cookie)) {
#	print $page->redirect($siteForCGI . $folderBase . "reservedzone/login.html");
#}

$userFormInput{'submit'} = $page->param('submit');

if ($userFormInput{'submit'} ne 0) {
	
	$userFormInput{'title'} = $page->param('title');
	$userFormInput{'time'} = $page->param('time');
	$userFormInput{'place'} = $page->param('place');
	$userFormInput{'speaker'} = $page->param('speaker');
	$userFormInput{'affiliazione'} = $page->param('affiliazione');
	$userFormInput{'speakerCV'} = $page->param('speakerCV');
	$userFormInput{'abstract'} = $page->param('abstract');
	$userFormInput{'additionalMails'} = $page->param('additionalMails');
	@mailing = $page->param('mailingList');
	@{$userFormInput{'mailingList'}}= @mailing;
	$userFormInput{'lang'} = $page->param('lang');
	
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
}

$title = "Nuovo Seminario";
$content = &printForm();
#$secondLevel = &createSecondLevelMenu();

if ($userFormInput{'submit'} eq "Conferma") {
    
    $userFormInput{'date'} = $page->param('date');
	
	my $eventID = &insertNewSeminary(\%userFormInput);
	
	if ($eventID != 0) {
		my $count = &sendEventMail($eventID);
		$title = "Inserimento Avvenuto";
		$content = &printThanks($count);
	}
	else {
		$title = "Errore nell'inserimento";
		$content = &printForm("Errore nell'inserimento del seminario. Riprovare");
	}
	
}
if ($userFormInput{'submit'} eq "Inserisci") {
		
    $userFormInput{'date'} = $page->param('dateDay') . '/' . $page->param('dateMonth') .'/' .
        $page->param('dateYear');
    
	my $errors = &checkInputs();
	
	if ($errors eq "") {
		$title = "Rivedi Informazioni";
		$content = &printReport();
	
	}
	else {
		$content = &printForm($errors, $userFormInput{'date'});
		
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



