#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use utf8;

require "GlobalVariables.pl";
require "WorkWithFiles.pl";
require "CreateSecondLevelMenu.cgi";
require "FunctionsAdmin.cgi";

sub printFormDeleteUser() {

	my $message = $_[0];
	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}
	
	my $userOptions = &getUsers();

	my $content = <<CONTENT;
<div id="contents">
	<h1>Elimina Utente</h1>
	$message
	<form method="post" action="DeleteUser.cgi" >
	<fieldset>
	<legend>Selezione Utente</legend>
	<label for="userID">Utente: </label>
	<select name="userID" id="userID">
	$userOptions
	</select>
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" name="submit" value="Elimina" class="button" />
	<input type="reset" name="reset" value="Reset" class="button" />
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

$title = "Cancellazione Utente";
$content = &printFormDeleteUser();
$secondLevel = &createSecondLevelMenu();

if ($userFormInput{'submit'} eq "Elimina") {

	$userFormInput{'userID'} = $page->param('userID');
	
	my $result = &deleteUser($userFormInput{'userID'});
	
	if ($result) {
		$content = &printFormDeleteUser("Operazione Completata");
	}
	else {
		$content = &printFormDeleteUser("Cancellazione non eseguita. Riprovare");
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
