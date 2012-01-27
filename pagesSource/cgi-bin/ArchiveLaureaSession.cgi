#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use CGI::Session;
use CGI::Cookie;
use utf8;

require "GlobalVariables.pl";
require "WorkWithFiles.pl";
require "CreateSecondLevelMenu.cgi";
require "FunctionsUploadTesi.cgi";

sub printFormCloseSession() {
	
	my $message = $_[0];
	
	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Archivia Tesi</h1>
	$message
	<form action="ArchiveLaureaSession.cgi" method="post">
	<fieldset>
	<legend>Sessione Laurea</legend>
	<label for="month">Mese Sessione Laurea: </label>
	<select name="month" id="month">
		<option value="01">Gennaio</option>
		<option value="02">Febbraio</option>
		<option value="03">Marzo</option>
		<option value="04">Aprile</option>
		<option value="05">Maggio</option>
		<option value="06">Giugno</option>
		<option value="07">Luglio</option>
		<option value="08">Agosto</option>
		<option value="09">Settembre</option>
		<option value="10">Ottobre </option>
		<option value="11">Novembre</option>
		<option value="12">Dicembbre</option>
	</select><br /><br />
	<label for="year">Anno Sessione Laurea: </label>
	<select name="year" id="year">
		<option value="2010">2010</option>
		<option value="2011">2011</option>
		<option value="2012">2012</option>
		<option value="2013">2013</option>
		<option value="2014">2014</option>
		<option value="2015">2015</option>
		<option value="2016">2016</option>
		<option value="2017">2017</option>
		<option value="2018">2018</option>
		<option value="2019">2019</option>
		<option value="2020">2020</option>
	</select>
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" name="submit" value="Archivia" class="button" />
	</fieldset>
	</form>
</div>
CONTENT
	
	return $content;
	
}


$page = new CGI;

$cookie = $page->cookie("CGISESSIONID") || undef;
if (!defined($cookie)) {
	print $page->redirect($siteForCGI . $folderBase . "reservedzone/login.html");
}

$userFormInput{'submit'} = $page->param('submit');

$title = "Archiviazione Tesi";
$content = &printFormCloseSession();
$secondLevel = &createSecondLevelMenu();

if ($userFormInput{'submit'} eq "Archivia") {

	$userFormInput{'month'} = $page->param('month');
	$userFormInput{'year'} = $page->param('year');
	
	my $result = &archiveThesis($userFormInput{'month'}, $userFormInput{'year'});
	if ($result eq "ok") {
		
		#creo archivio file e lo sposto in cartella dedicata
		my $archiveThesis = "Tesi_$userFormInput{'year'}_$userFormInput{'month'}.tgz";
		my $archivePresentation = "Presentazioni_$userFormInput{'year'}_$userFormInput{'month'}.tgz";
		
		my $cmd = "tar -cvzf " . $siteForCGI . "private/archivio/$archiveThesis -C $siteForCGI" . "private/tesimagistrale/ . 1>/dev/null";
		system($cmd);
		
		$cmd = "tar -cvzf " . $siteForCGI . "private/archivio/$archivePresentation -C $siteForCGI" . "private/presentazionimagistrale/ . 1>/dev/null";
		system($cmd);	
		
		$cmd = "rm " . $siteForCGI . "private/tesimagistrale/*.* $siteForCGI" . "private/presentazionimagistrale/*.*";
		system($cmd);
		
		$content = &printFormCloseSession("Operazione Avvenuta");
	}
	else {
		$content = &printFormCloseSession("Operazione non completata");
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




