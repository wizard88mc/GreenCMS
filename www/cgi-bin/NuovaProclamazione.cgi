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
	
	# se $userFormInput{'giorno'} definito lo imposto di default
	if ($userFormInput{'giorno'}) {
	    my ($day, $month, $year) = &getDateComponentsFromItalianDate($userFormInput{'giorno'});
	     $giornoCommissione = &getDaysOptions($day);
	     $meseCommissione = &getMonthsOptions($month);
	}
	
	my $orePossibili = &getOreOrari();
	my $minutiPossibili = &getMinutiOrari();
	my $minutiDistacco = &getMinutiOrari();
	my $optionsProfessore = &getOptionsProfessore();
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Inserisci Nuova Proclamazione</h1>
	$message
	<form method="post" action="NuovaProclamazione.cgi">
	<fieldset>
	<legend>Informazioni Generali</legend>
	<label for="giorno">Giorno: </label>
	<select name="giorno" id="giorno">$giornoCommissione</select>
	<select name="mese" id="mese">$meseCommissione</select><br />
	<label for="ora">Ora: </label>
	<select name="ora" id="ora">$orePossibili</select>:
	<select name="minuti" id="minuti">$minutiPossibili</select><br />
	<label for="aula">Aula</label>
	<input type="text" name="aula" id="aula" value="$userFormInput{'aula'}" /><br />
	<label for="turni">Numero turni : </label>
	<select name="turni" id="turni">
	    <option value="1">1</option><option value="2">2</option>
	    <option value="3">3</option><option value="4">4</option>
	    <option value="5">5</option><option value="6">6</option></select><br />
	<label for="distacco">Distanza gruppi: </label>
	<select name="distacco" id="distacco">$minutiDistacco</select>
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
	<select name="componenti">$optionsProfessore</select>
	<select name="componenti">$optionsProfessore</select><br />
	<label for="supplenti">Supplenti: </label>
	<select name="supplenti" id="supplenti">$optionsProfessore</select>
	<select name="supplenti">$optionsProfessore</select>
	<select name="supplenti">$optionsProfessore</select>
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" class="button" name="submit" value="Avanti" />
	<input type="reset" class="button" value="Annulla" />
	</fieldset>
	</form>
</div>
CONTENT

	return $content;
}

sub printFormCommissioneCompleta() {
    
    my $stringComponenti = '';
    foreach my $componente (@{$userFormInput{'componenti'}}) {
	    if ($componente ne "") {
	        $stringComponenti .= ", $componente";
	    }
	}
	$stringComponenti =~ s/, //;
	
	my $stringSupplenti = '';
	foreach my $componente (@{$userFormInput{'supplenti'}}) {
	    if ($componente ne "") {
	        $stringSupplenti .= ", $componente";
	    }
	}
	$stringSupplenti =~ s/, //;
	
	my @arrayDivisioneTurni = &dividiCandidati($userFormInput{'turni'});
	my $stringTextareaCandidati = '';
	
	foreach $stringCandidati (@arrayDivisioneTurni) {
	    $stringTextareaCandidati .= 
	    "<textarea name=\"candidati\" rows=\"8\" cols=\"20\">$stringCandidati</textarea><br />";
	}
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Riepilogo News</h1>
	<form method="post" action="NuovaProclamazione.cgi" accept-charset="UTF-8">
	<fieldset>
	<legend>Informazioni generali</legend>
	<p><strong>Data: </strong>$userFormInput{'giorno'}</p>
	<p><strong>Ora Inizio: </strong>$userFormInput{'orario'}</p>
	<p><strong>Aula: </strong>$userFormInput{'aula'}</p>
	<p><strong>Numero di turni: </strong>$userFormInput{'turni'}</p>
	<p><strong>Distanza tra turni: </strong>$userFormInput{'distacco'}</p>
	<p><strong>Presidente: </strong> $userFormInput{'presidente'}</p>
	<p><strong>Commissione: </strong>$stringComponenti</p>
	<p><strong>Supplenti: </strong>$stringSupplenti</p>
	</fieldset>
	<fieldset>
	<legend>Divisione candidati: </legend>
	$stringTextareaCandidati
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" class="button" name="submit" value="Completa" />
	<input type="submit" class="button" name="submit" value="Indietro" />
	<input type="hidden" name="giorno" value="$userFormInput{'giorno'}" />
	<input type="hidden" name="orario" value="$userFormInput{'orario'}" />
	<input type="hidden" name="aula" value="$userFormInput{'aula'}" />
	<input type="hidden" name="turni" value="$userFormInput{'turni'}" />
	<input type="hidden" name="distacco" value="$userFormInput{'distacco'}" />
	<input type="hidden" name="presidente" value="$userFormInput{'presidente'} " />
	<input type="hidden" name="commissione" value="$stringComponenti" />
	<input type="hidden" name="supplenti" value="$stringSupplenti" />
	</fieldset>
	</form>
</div>
CONTENT

	return $content;

}

sub printEnd() {
    
    my $nomePagina = $_[0];
    
    my $content = <<CONTENT;
<div id="contents">
	<h1>Operazione Completata</h1>
	<p>Proclamazione di Laurea inserita correttamente</p>
	<p>La pagina creata si chiama $nomePagina</p>
</div>
CONTENT


	return $content;
}

sub checkInputs() {
    
    my $errors = '';
    if (&checkCorrectDate($userFormInput{'giorno'}) eq false) {
        $errors .= "Data non corretta<br />";       
    }
    if (length($userFormInput{'aula'}) < 2) {
        $errors .= "Aula non inserita<br />";
    }
	if (length($userFormInput{'presidente'}) < 3) {
	    $errors .= "Presidente di commissione non inserito<br />";
	}
}

$page = new CGI;
$content;

$cookie = $page->cookie("CGISESSIONID") || undef;
if (!defined($cookie)) {
	print $page->redirect($siteForCGI . $folderBase . "reservedzone/login.html");
}

$userFormInput{'submit'} = $page->param('submit');

if ($userFormInput{'submit'} ne 0) {
	 
	$userFormInput{'aula'} = $page->param('aula');
	$userFormInput{'presidente'} = $page->param('presidente');
	$userFormInput{'turni'} = $page->param('turni');
	$userFormInput{'distacco'} = $page->param('distacco');
	
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

$title = "Inserisci Nuova Proclamazione";
$content = &printFormNuovaCommissione();
$secondLevel = &createSecondLevelMenu();

# inserisco commissione di laurea nel file XML 
if ($userFormInput{'submit'} eq "Avanti") {
    
    my @currentDate = &getCurrentDate();
    $userFormInput{'giorno'} = $page->param('giorno') .'/' . 
                                  $page->param('mese') . '/' . 
                                  $currentDate[0];
    $userFormInput{'orario'} = $page->param('ora') .':' . $page->param('minuti');
    @{$userFormInput{'componenti'}} = $page->param('componenti');
	@{$userFormInput{'supplenti'}} = $page->param('supplenti');
	
    my $errors = &checkInputs();
    
    if ($errors eq "") {
        $content = &printFormCommissioneCompleta();
    }
    else {
        $content = &printFormNuovaCommissione($errors);
    }
    
}
if ($userFormInput{'submit'} eq "Completa") {
    
    $userFormInput{'giorno'} = $page->param('giorno');   
    $userFormInput{'orario'} = $page->param('orario');
    $userFormInput{'commissione'} = $page->param('commissione');
    $userFormInput{'supplenti'} = $page->param('supplenti');
    @{$userFormInput{'candidati'}} = $page->param('candidati');
    
    my $result = &insertNuovaProclamazione(\%userFormInput);
    
    if ($result == 1) {
        # inserimento della commissione andata a buon fine, creo pagina
        my $paginaCreata = &creaPaginaCommissione(0); # invocazione funzione di creazione pagia
        if ($paginaCreata ne "") {
            # stampo messaggio di operazione completata   
            $content = &printEnd($paginaCreata);
        }
    }
    else {
        # qualcosa è andato storto, ristampo passo 1 della form per la proclamazione
        $content = &printFormNuovaCommissione("Inserimento non riuscito. Riprovare");
    }
}

if ($userFormInput{'submit'} eq "Indietro") {
    
    $userFormInput{'giorno'} = $page->param('giorno');
    $content = &printFormNuovaCommissione();
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

