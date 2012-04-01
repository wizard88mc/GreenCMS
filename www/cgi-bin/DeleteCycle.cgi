#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use CGI::Session;
use CGI::Cookie;
use utf8;

binmode STDIN, ":utf8";
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";

require "CreateSecondLevelMenu.cgi";
require "GlobalVariables.pl";
require "WorkWithFiles.pl";
require "FunctionsPHDStudents.cg";

sub printFormDeleteCycle() {
	
	my $message = $_[0];

	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}
	
	my $cycleList = &getCyclesList();
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Eliminazione Ciclo Dottorato</h1>
	$message
	<form action="DeleteCycle.cgi" method="post">
	<fieldset>
	<legend>Seleziona Ciclo</legend>
	<label for="cycleID">Ciclo Da Eliminare</label>
	<select name="cycleID" id="cycleID">
	$cycleList
	</select>
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" name="submit" value="Elimina" />
	</fieldset>
	</fom>
</div>

CONTENT

	return $content;
	
}

$page = new CGI;
$cookie = $page->cookie("CGISESSIONID") || undef;
if (!defined($cookie)) {
	print $page->redirect($siteFolderCGI . $folderBase . "reservedzone/login.html");
}

$input{'submit'} = $page->param('submit');
$input{'cycleID'}  = $page->param('cycleID');

$title = "Eliminazione Ciclo Dottorato";
$content = &printFormDeleteCycle();
$secondLevel = &createSecondLevelMenu();

if ($input{'submit'} eq "Elimina") {
	
	my $result = &deleteCycle();
	$content = &printFormDeleteCycle($result);	
}

$template = &openFile($siteForCGI . "reservedzone/reservedtemplate.html") or die "$!";
utf8::decode($template);
	
$content = $secondLevel . $content;
	
$template =~ s/<pageContent\/>/$content/g;
$template =~ s/<pageTitle\/>/$title/g;
	
print <<CONTENT;
Content-type:text/html\n\n
$template

CONTENT




