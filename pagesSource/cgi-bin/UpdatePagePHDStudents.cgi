#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use CGI::Session;
use CGI::Cookie;
use utf8;

require "GlobalVariables.pl";
require "CreateSecondLevelMenu.cgi";
require "UpdatePHDStudent.cgi";
require "WorkWithFiles.pl";
require "UpdatePHDStudentEn.cgi";
require "FunctionsPHDStudents.cgi";

sub printFormUpdatePage() {

	my $message = $_[0];
	
	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Aggiornamento pagina Dottorato</h1>
	$message
	<form action="UpdatePagePHDStudents.cgi" method="post">
	<fieldset>
	<legend class="hidden">Unica</legend>
	<p>Per aggiornare la pagina dei Dottorandi cliccare il bottone </p>
	<input type="submit" name="submit" value="Aggiorna" class="button" />
	</form>
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

$title = "Aggiornamento pagina Dottorato";
$content = &printFormUpdatePage();
$secondLevel = &createSecondLevelMenu();

if ($input{'submit'} eq "Aggiorna") {
	
    &moveXMLFile();
	&updatePHDStudent();
	&updatePHDStudentEn();
	$content = &printFormUpdatePage("Aggiornamento eseguito");
	
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

	
	

