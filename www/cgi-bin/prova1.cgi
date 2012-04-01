#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use utf8;
use Time::localtime;
use Date::Calc qw(Add_Delta_Days Delta_Days);

use DBI;
use DBD::mysql;
use XML::LibXML;
use HTML::Entities;
use File::Basename;
use utf8;

require "GlobalVariables.pl";
require "GlobalFunctions.cgi";
require "WorkWithFiles.pl";
require "CreateSecondLevelMenu.cgi";
require "FunctionsCommissioni.cgi";

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
require "FunctionsCommissioni.cgi";

sub printFormNuovaCommissione() {
	
	my $message = "";
	if ($_[0]) {
	    $message = $_[0];
		$message = "<div id=\"message\">$message</div>";
	}
	
	my $giornoCommissione = &getDaysOptions();
	my $meseCommissione = &getMonthsOptions();
	my $orePossibili = &getOreOrari();
	my $minutiPossibili = &getMinutiOrari();
	my $optionsProfessore = '<option value="aaa">aaa</option>';
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Inserisci Nuova Commissione</h1>
	$message
	<form method="post" action="prova1.cgi">
	<fieldset>
	<legend>Informazioni Generali</legend>
	<label for="giorno">Giorno: </label>
	<select name="giorno" id="giorno">$giornoCommissione</select>
	<select name="mese" id="mese">$meseCommissione</select><br />
	<label for="ora">Ora: </label>
	<select name="ora" id="ora">$orePossibili</select>:
	<select name="minuti" id="minuti">$minutiPossibili</select><br />
	<label for="aula">Aula</label>
	<input type="text" name="aula" id="aula" value="$userFormInput{'aula'}" />
	</fieldset>
	<fieldset>
	<legend>Commissione</legend>
	<label for="presidente">Presidente</label>
	<select name="presidente" id="presidente">$optionsProfessore</select><br />
	<label for="componente">Componenti Commissione: </label>
	<select name="componenti" id="componente">$optionsProfessore</select>
	<select name="componenti">$optionsProfessore</select>
	<select name="componenti">$optionsProfessore</select>
	<select name="componenti">$optionsProfessore</select>
	<select name="componenti">$optionsProfessore</select><br />
	<label for="supplenti">Supplenti: </label>
	<select name="supplenti" id="supplenti">$optionsProfessore</select>
	<select name="supplenti">$optionsProfessore</select>
	<select name="supplenti">$optionsProfessore</select><br />
	<label for="candidati">Candidati</label>
	<textarea id="candidati" name="candidati" rows="8" cols="20">$userFormInput{'candidati'}</textarea>
	<input type="hidden" name="dataLaurea" value="$userFormInput{'dataLaurea'}" />
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

sub checkInputs() {
    
    my $errors = '';
    if (length($userFormInput{'aula'}) < 2) {
        $errors .= "Aula non inserita<br />";
    }
	if (length($userFormInput{'presidente'}) < 3) {
	    $errors .= "Presidente di commissione non inserito<br />";
	}
	#if ($userFormInput{
}

$page = new CGI;
$content;

#$cookie = $page->cookie("CGISESSIONID") || undef;
#if (!defined($cookie)) {
#	print $page->redirect($siteForCGI . $folderBase . "reservedzone/login.html");
#}

$userFormInput{'submit'} = $page->param('submit');

if ($userFormInput{'submit'} ne 0) {
	
    my @currentDate = &getCurrentDate();
    $userFormInput{'giorno'} = $page->param('giorno') .'/' . 
                                  $page->param('mese') . '/' . 
                                  $currentDate[0];
    $userFormInput{'orario'} = $page->param('ora') .':' . $page->param('minuti'); 
	$userFormInput{'aula'} = $page->param('aula');
	$userFormInput{'presidente'} = $page->param('presidente');
	@{$userFormInput{'componenti'}} = $page->param('componenti');
	$userFormInput{'supplente'} = @{$page->param('supplente')};
	
	foreach $userInput (keys %userFormInput) {
		if ($userFormInput{$userInput} eq 0) {
			$userFormInput{$userInput} = "";
		}
		utf8::decode($userFormInput{$userInput});
		$userFormInput{$userInput} =~ s/\"/''/g;
		$userFormInput{$userInput} =~ s/\&/\&amp<\;/g;
		$userFormInput{$userInput} =~ s/</\&lt\;/g;
		$userFormInput{$userInput} =~ s/>/\&gt\;/g;
	}
}

# inserisco commissione di laurea nel file XML 
#if ($userFormInput{'submit'} eq "Inserisci") {
    
    
    
#}

$title = "Inserisci Nuova Commissione";
$content = &printFormNuovaCommissione();
#$secondLevel = &createSecondLevelMenu();

if ($userFormInput{'submit'} eq "Inserisci") {
$content = "Prova ";
foreach $componente(@{$userFormInput{'componenti'}}) {
    $content .= " $componente";
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

