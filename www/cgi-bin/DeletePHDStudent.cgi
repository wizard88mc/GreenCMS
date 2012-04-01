#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use utf8;

require "GlobalVariables.pl";
require "WorkWithFiles.pl";
require "CreateSecondLevelMenu.cgi";
require "FunctionsPHDStudents.cgi";

sub printFormChoosePHDStudent() {
	
	$message = $_[0];
	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}
	
	my $phdList = &getPHDList();
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Elimina Dottorando</h1>
	$message
	<form method="post" action="DeletePHDStudent.cgi" >
	<fieldset>
	<legend>Scelta Dottorando</legend>
	<label for="idPHDStudent">Seleziona il Dottorando da eliminare</label>
	<select id="idPHDStudent" name="idPHDStudent">
	$phdList
	</select>
	</fieldset>
	<fieldset>
	<legend></legend>
	<input type="submit" name="submit" value="Elimina" class="button" />
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

$userFormInput{'submit'} = $page->param("submit");

$title = "Eliminazione Dottorando";
$content = &printFormChoosePHDStudent();
$secondLevel = &createSecondLevelMenu();


if ($userFormInput{'submit'} eq "Elimina") {
	
	$userFormInput{'idPHDStudent'} = $page->param("idPHDStudent");
	
	my $result = &deletePHDStudent($userFormInput{'idPHDStudent'});
	
	if ($result) {
		
		$title = "Eliminazione Avvenuta";
		$content = &printFormChoosePHDStudent("Operazione Completata");
	}
	else {
		
		$title = "Errore";
		$content = &printFormChoosePHDStudent("errore nell'eliminazione. Riprovare");
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


