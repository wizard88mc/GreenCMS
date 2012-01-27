#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use utf8;

require "GlobalVariables.pl";
require "WorkWithFiles.pl";
require "CreateSecondLevelMenu.cgi";

sub printMainAdministration() {
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Area Riservata</h1>
	<p>Benvenuto nell'area riservata</p>
	<p>Alla Sua destra troverà il menu di navigazione a seconda del livello
	di permesso che Le è stato assegnato</p>
</div>
CONTENT

	utf8::encode($content);

return $content;

}


$page = new CGI;

$cookie = $page->cookie("CGISESSIONID") || undef;
if (!defined($cookie)) {
	print $page->redirect($siteForCGI . $folderBase . "reservedzone/login.html");
}
else {

	
	my $template = &openFile($siteForCGI . "reservedzone/reservedtemplate.html") or die "$!";
	
	my $stringSecondLevel = &createSecondLevelMenu();
	my $content = &printMainAdministration() or die "$!";
	
	$content = $stringSecondLevel . $content;
	
	$template =~ s/<pageContent\/>/$content/g;
	$template =~ s/<pageTitle\/>/Area Riservata/g;
	
print <<CONTENT;
Content-type:text/html\n\n
$template

CONTENT
	
}




