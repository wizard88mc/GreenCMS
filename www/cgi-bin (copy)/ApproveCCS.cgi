#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use utf8;

require "GlobalVariables.pl";
require "WorkWithFiles.pl";
require "CreateSecondLevelMenu.cgi";
require "FunctionsCCS.cgi";

#stampa form per l'approvazione del CCS
sub printFormChooseCCS() {
	
	my $message = $_[0];
	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}
	
	my $ccsToApproveOption = &getCCSToApprove();

	my $content = <<CONTENT;
<div id="contents">
	<h1>Approvazione CCS</h1>
	$message
	<form method="post" action="ApproveCCS.cgi">
	<fieldset>
	<legend>Selezione CCS</legend>
	<label for="approveID">CCS da Approvare</label>
	<select id="approveID" name="approveID" >
	$ccsToApproveOption
	</select>
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" class="button" name="submit" value="Approva" />
	</fieldset>
	</form>	
</div>
CONTENT

	return $content;
}	

sub approveCCS() {
	
	eval {
		#parametro: ID del CCS da approvare
		my $ccsID = $_[0];

		#trasformo il CCS da InApprovazione ad Approvato
		my $ccsFolder = &approveCCSXML($ccsID);
		
		if ($ccsFolder != 0) {
			my $fileHTACX = $siteForCGI . "documenti/verbaliccs/$ccsFolder/.htaccess";
			
			#elimino file htaccess
			unlink($fileHTACX) or die "$!";
			
			return 1;
		}
		else {
			return 0;
		}
	}
	or do {
		return 0;
	}
	
}

$page = new CGI;


$cookie = $page->cookie("CGISESSIONID") || undef;
if (!defined($cookie)) {
	print $page->redirect($siteForCGI . $folderBase . "reservedzone/login.html");
}


$stringSecondLevel = &createSecondLevelMenu();
$titlePage = "Approva CCS";
$content = &printFormChooseCCS();


if ($page->param('submit') eq "Approva") {
	
	my $result = &approveCCS($page->param('approveID'));
	if ($result) {
		$content = &printFormChooseCCS("Approvazione avvenuta");
	}
	else {
		$content = &printFormChooseCCS("Errore durante l'esecuzione del comando. Riprovare");
	}
	
}

utf8::encode($content);

$content = $stringSecondLevel . $content;

my $template = &openFile($siteForCGI . "reservedzone/reservedtemplate.html") or die "$!";


$template =~ s/<pageContent\/>/$content/g;
$template =~ s/<pageTitle\/>/$titlePage/g;

print <<CONTENT;
Content-type:text/html\n\n
$template

CONTENT


