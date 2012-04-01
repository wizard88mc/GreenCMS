#!/usr/bin/perl

use CGI qw(:standart);
use CGI::Carp qw(fatalsToBrowser);
use utf8;

require "GlobalVariables.pl";
require "WorkWithFiles.pl";
require "CreateSecondLevelMenu.cgi";
require "FunctionsSeminary.cgi";

sub printFormDeleteMailingList() {

	my $mailingList = &getMailingListOptions();
	my $message = $_[0];
	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}

	my $content = <<CONTENT;
<div id="contents">
	<h1>Seleziona la Mailing List da eliminare</h1>
	$message
	<form method="post" action="DeleteMailingList.cgi">
	<fieldset>
	<legend>Mailing List</legend>
	<label for="idDeleteMailingList">Mailing List Name: </label>
	<select id="idDeleteMailingList" name="idDeleteMailingList" >
		$mailingList
	</select>
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" class="button" value="Elimina" name="submit" />
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

$title = "Elimina Mailing List";
$content = &printFormDeleteMailingList();
$secondLevel = &createSecondLevelMenu();

if ($userFormInput{'submit'} eq "Elimina") {

	$userFormInput{'idDeleteMailingList'} = $page->param('idDeleteMailingList');
	
	my $result = &deleteMailingList($userFormInput{'idDeleteMailingList'});
	
	if ($result) {
		
		$content = &printFormDeleteMailingList("Eliminazione Avvenuta");
	}
	else {
		
		$content = &printFormDeleteMailingList("Problemi nell'eliminazione. Riprovare");
	}

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

