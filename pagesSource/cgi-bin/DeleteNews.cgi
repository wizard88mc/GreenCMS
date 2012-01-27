#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use CGI::Session;
use CGI::Cookie;
use utf8;

require "GlobalVariables.pl";
require "WorkWithFiles.pl";
require "CreateSecondLevelMenu.cgi";
require "FunctionsNews.cgi";

#form per la scelta della news da eliminare
sub printFormDelete() {
	
	my $message = $_[0];
	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}
	
	my $newsOption = &getNewsListOptions();
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Elimina News</h1>	
	$message
	<form method="post" action="DeleteNews.cgi">
	<fieldset>
	<legend>Seleziona News</legend>
	<label for="idNewsDelete">News da eliminare</label>
	<select id="idNewsDelete" name="idNewsDelete" >
	$newsOption
	</select>
	</fieldset>                                   
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input class="button" type="submit" name="submit" value="Elimina" />
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

$title = "Elimina News";
$content = &printFormDelete();
$secondLevel = &createSecondLevelMenu();

if ($page->param('submit') eq "Elimina") {
	
	my $result = &deleteNews($page->param('idNewsDelete'));
	
	if ($result) {
		
		$content = &printFormDelete("Eliminazione Avvenuta");
	}
	else {
		
		$content = &printFormDelete("Non sono riuscito ad eliminare la news");
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


