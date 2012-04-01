#!/usr/bin/perl

use CGI qw(:standart);
use CGI::Carp qw(fatalsToBrowser);
use utf8;

require "GlobalVariables.pl";
require "WorkWithFiles.pl";
require "CreateSecondLevelMenu.cgi";
require "FunctionsSeminary.cgi";

sub printFormNewMailingList() {

	my $message = $_[0];
	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}

	my $content = <<CONTENT;
<div id="contents">
	<h1>Inserisci Nuova Mailing List</h1>
	$message
	<form method="post" action="NewMailingList.cgi">
	<fieldset>
	<legend>Nuova Mailing List</legend>
	<label for="nameNewMailingList">Nome Mailing List: </label>
	<input type="text" id="nameNewMailingList" name="nameNewMailingList" />
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" class="button" value="Crea" name="submit" />
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


$title = "Nuova Mailing List";
$content = &printFormNewMailingList();
$secondLevel = &createSecondLevelMenu();

if ($userFormInput{'submit'} eq "Crea") {

	$userFormInput{'nameNewMailingList'} = $page->param('nameNewMailingList');
	utf8::decode($userFormInput{'nameNewMailingList'});
	$userFormInput{'nameNewMailingList'} =~ s/\&/\&amp\;/g;
	$userFormInput{'nameNewMailingList'} =~ s/</\&lt\;/g;
	$userFormInput{'nameNewMailingList'} =~ s/>/\&gt\;/g;
	
	if (($userFormInput{'nameNewMailingList'} eq "")) { 
		
		$content = &printFormNewMailingList("Nome vuoto");
	}
	else {
		
		my $result = &insertNewMailingList($userFormInput{'nameNewMailingList'});
		if ($result) {
			
			$title = "Inserimento Avvenuto";
			$content = &printFormNewMailingList("Nuova Mailing List inserita");
		}
		else {
			
			$content = &printFormNewMailingList("Inserimento non eseguito. Riprovare");
		}
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




