#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use utf8;

require "GlobalVariables.pl";
require "WorkWithFiles.pl";
require "CreateSecondLevelMenu.cgi";
require "FunctionsSeminary.cgi";

sub printFirstStepEliminateAssociation() {
	
	my $message = $_[0];
	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}
	my $mailingList = &getMailingListOptions();

	my $content = <<CONTENT;
<div id="contents">
	<h1>Seleziona la Mailing List</h1>
	$message
	<form method="post" action="DeleteAssociationMailingContact.cgi">
	<fieldset>
	<legend>Mailing List</legend>
	<label for="idMailingListDeleteAssociation">Nome Mailing List: </label>
	<select id="idMailingListDeleteAssociation" name="idMailingListDeleteAssociation" >
		$mailingList
	</select>
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" class="button" value="Trova Contatti" name="submit" />
	</fieldset>
	</form>
</div>
CONTENT

	return $content;
}

sub printFormSelectContactsMailingList() {

	my $contactsList= &getContactsMailingListOption($userFormInput{'idMailingListDeleteAssociation'});

	my $content = <<CONTENT;
<div id="contents">
	<h1>Seleziona Contatto</h1>
	<form method="post" action="DeleteAssociationMailingContact.cgi">
	<fieldset>
	<legend>Seleziona Contatto</legend>
	<label for="idContactEliminateAssociation">Seleziona Contatto: </label>
	<select id="idContactEliminateAssociation" name="idContactEliminateAssociation" >
		$contactsList
	</select>
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" class="button" value="Elimina Associazione" name="submit" />
	</fieldset>
	<input type="hidden" name="idMailingListDeleteAssociation" value="$userFormInput{'idMailingListDeleteAssociation'}" />
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

if ($userFormInput{'submit'} ne 0) {

	$userFormInput{'idMailingListDeleteAssociation'} = $page->param('idMailingListDeleteAssociation');
	$userFormInput{'idContactEliminateAssociation'} = $page->param('idContactEliminateAssociation');

}

$secondLevel = &createSecondLevelMenu();
$title = "Elimina Associazione Mailing List - Contatto";
$content = &printFirstStepEliminateAssociation();


if ($userFormInput{'submit'} eq "Elimina Associazione") {

	my $result = &deleteAssociation($userFormInput{'idContactEliminateAssociation'}, $userFormInput{'idMailingListDeleteAssociation'});
	
	if ($result) {
		
		$content = &printFirstStepEliminateAssociation("Associazione eliminata");
	}
	else {
		
		$content = &printFirstStepEliminateAssociation("Operazione NON eseguita. Riprovare");
	}
		
}
if ($userFormInput{'submit'} eq "Trova Contatti") {

	$title = "Seleziona Contatto";
	$content = &printFormSelectContactsMailingList();
}


utf8::encode($content);

my $template = &openFile($siteForCGI . "reservedzone/reservedtemplate.html") or die "$!";
	
$content = $secondLevel . $content;
	
$template =~ s/<pageContent\/>/$content/g;
$template =~ s/<pageTitle\/>/$title/g;

print <<CONTENT;
Content-type: text/html\n\n
$template

CONTENT

