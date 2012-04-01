#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use HTML::Entities;
use utf8;

require "GlobalVariables.pl";
require "WorkWithFiles.pl";
require "CreateSecondLevelMenu.cgi";
require "FunctionsSeminary.cgi";

sub printFormDeleteContact() {

	my $message = $_[0];
	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}
	my $contactsOptions = &getContactsOptions();
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Elimina Contatto</h1>
	$message
	<form method="post" action="DeleteContact.cgi">
	<fieldset>
	<legend>Seleziona Contatto</legend>
	<label for"userDelete">Nome Contatto</label>
	<select id="userDelete" name="userDelete" >
		$contactsOptions
	</select>
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" class="button" name="submit" value="Elimina" />
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

$secondLevel = &createSecondLevelMenu();
$title = "Elimina Contatto";
$content = &printFormDeleteContact();

if ($userFormInput{'submit'} eq "Elimina") {

	$userFormInput{'userDelete'} = $page->param('userDelete');
	
	my $result = &deleteContact($userFormInput{'userDelete'});
	
	if ($result) {
		
		$content = &printFormDeleteContact("Eliminazione Avvenuta");
	}
	else {
		
		$content = &printFormDeleteContact("Problemi nell'esecuzione. Riprovare");
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


