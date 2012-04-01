#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use utf8;

require "GlobalVariables.pl";
require "WorkWithFiles.pl";
require "CreateSecondLevelMenu.cgi";
require "FunctionsSeminary.cgi";

sub printFormAssociation() {

	my $message = $_[0];
	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}
	my $contactsList = &getContactsOptions();
	my $mailingList = &getMailingListOptions();
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Associa Contatto - Mailing List</h1>
	$message
	<form method="post" action="AssociateMailingContact.cgi">
	<fieldset>
	<legend>Seleziona Mailing List</legend>
	<label for="mailingAssociate">Mailing List: </label>
	<select id="mailingAssociate" name="mailingAssociate" >
		$mailingList
	</select>
	</fieldset>
	<fieldset>
	<legend>Seleziona Contatto/i</legend>
	<label for="contactAssociate">Contatto: </label>
	<select id="contactAssociate" name="contactAssociate" >
		$contactsList
	</select>
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" class="button" name="submit" value="Associa" />
	<input type="reset" class="button" value="Reset" />
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

$stringSecondLevel = &createSecondLevelMenu();
$content = &printFormAssociation();
$title = "Associa Contatto - Mailing List";

if ($userFormInput{'submit'} eq "Associa") {
	
	$userFormInput{'contactAssociate'} = $page->param('contactAssociate');
	$userFormInput{'mailingAssociate'} = $page->param('mailingAssociate');
	
	my $associations = &associateContactMailingList($userFormInput{'contactAssociate'}, $userFormInput{'mailingAssociate'});
	$content = &printFormAssociation("Associazioni Inserite: $associations");

}

utf8::encode($content);

$template = &openFile($siteForCGI . "reservedzone/reservedtemplate.html") or die "$!";
	
$content = $stringSecondLevel . $content;
	
$template =~ s/<pageContent\/>/$content/g;
$template =~ s/<pageTitle\/>/$title/g;
	
print <<CONTENT;
Content-type:text/html\n\n
$template

CONTENT
