#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use utf8;

require "ExtractXML.pl";
require "GlobalVariables.pl";
require "WorkWithFiles.pl";

#crea il template utilizzato per le pagine dell'area riservata
sub createReservedTemplate() {
	
	my $fileXMLMenu = &extractXML("../pagesSource/globalDetails/FirstLevelMenu.xml");
	
	my $addressComplete = "$address/$folderBase";
	$addressComplete =~ s/\/\//\//g;
	
	#creo il menu di primo livello della pagina (devo mettere percorso completo per eliminare l'https del protocollo)
	my $firstLevelMenu = 
	"<div id=\"navigation\">
		<ul>";
		
		foreach $linkMenu ($fileXMLMenu->findnodes('firstLevelMenuEntry')->get_nodelist) {
			
			my $link = "";
			
			if (index($linkMenu->findvalue('linkMenuEntryPageTarget'), ".cgi") == -1) {
				
				$link = "<li><a href=\"http://$addressComplete" . $linkMenu->findvalue('linkMenuEntryPageTarget') ."\" title=\"" . $linkMenu->findvalue('linkMenuEntryAlt') ."\">". $linkMenu->findvalue('linkMenuEntryText') ."</a></li>";	
			}
			else {
				$link = "<li><a href=\"http://$address/cgi-bin/". $linkMenu->findvalue('linkMenuEntryPageTarget') ."\" title=\"". $linkMenu->findvalue('linkMenuEntryAlt') ."\">". $linkMenu->findvalue('linkMenuEntryText') ."</a></li>";
			}
			
			$firstLevelMenu .= $link;
		}
		
	$firstLevelMenu .= " 
		</ul>
	</div>";
	
	#costruisco pagina
	my $finalPage = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">
<html xmlns=\"http://www.w3.org/1999/xhtml\"  xml:lang=\"it\" lang=\"it\">
<head>
    <title><pageTitle/></title>
    <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/>
    <meta name=\"title\" content=\"Area Riservata\" />
	<meta name=\"language\" content=\"italian it\" />

	<link type=\"text/css\" rel=\"stylesheet\" href=\"../style/base.css\" media=\"screen\" />
</head>
<body>";

	my $headerPageText = "";
	#recupero header per la pagina
	$headerPageText = &openFile("../pagesSource/globalDetails/header.html") or die "$!";
	
	$headerPageText .= "<div id=\"main\">";
	
	#elimno la parte di utility nell'header
	my $divDeleteStart = index($headerPageText, "<div id=\"headerUtility\">");
	
	my $divDeleteEnd = index($headerPageText, "</div>", $divDeleteStart) + length("</div>");
	
	substr($headerPageText, $divDeleteStart, $divDeleteEnd - $divDeleteStart, "");
	
	$finalPage .= $headerPageText;
	
	$finalPage .= $firstLevelMenu;
	
	$finalPage .= "<div id=\"contents-right\">";
	
	$finalPage .= "<secondLevelMenu\/>";
	
	$finalPage .= "<pageContent\/>";
	
	#recupero footer per la pagina
	my $footerText = &openFile("../pagesSource/globalDetails/footer.html"); #estratto contenuto del footer
	
	my $footerLink = index($footerText, "href=\"/cgi-bin/");
	substr($footerText, $footerLink, length("href=\"/"), "href=\"http://$address/folderBase/");
	
	$finalPage .= $footerText;
	
	$finalPage .= "
	</body>
	</html>";
	
	my $pathSRC = "src=\"../";  #path di default per i link indicati da src
	my $pathHREF = "href=\"../"; #path di default per i link indicati da href
	
	$finalPage =~ s/$pathSRC/src="$parentPathCGI\//g; 
	$finalPage =~ s/$pathHREF/href="$parentPathCGI\//g;
	$finalPage =~ s/<secondLevelMenu\/>//g;
	$finalPage =~ s/<linksAccessibility\/>//g;
	
	&createFile($sitePath . "reservedzone/reservedtemplate.html", $finalPage);
	
	#dalla pagina login.html, logout.html e loginincorrect.html elimino la parte di utility nell'header e cambio tutti gli indirizzi da https a http
	my $login = &openFile($sitePath . "reservedzone/login.html");
	
	#cerco inizio e fine del div id="navigation"
	my $startMenu = index($login, "<div id=\"navigation\">");
	my $endDiv = index($login, "</div>", $startMenu);
	
	#sostituisco tutti gli href con l'indirizzo completo
	my $position = index($login, 'href="/', $startMenu);
	
	while ($position != -1) {
		substr($login, $position, length('href="/'), "href=\"http://$address/$folderBase");
		$position = index($login, 'href="/', $position + length("href=\"http://$address/$folderBase"));
	}
	
	#elimino il div id="headerUtility"
	$divDeleteStart = index($login, "<div id=\"headerUtility\">");
	$divDeleteEnd = index($login, "</div>", $divDeleteStart) + length("</div>");
	substr($login, $divDeleteStart, $divDeleteEnd - $divDeleteStart, "");
	
	unlink($sitePath . "reservedzone/login.html") or die "$!";
	&createFile($sitePath . "reservedzone/login.html", $login);
	
	my $logout = &openFile($sitePath . "reservedzone/logout.html");
	
	#cerco inizio e fine del div id="navigation"
	$startMenu = index($logout,"<div id=\"navigation\"");
	$endDiv = index($logout, "</div>", $startMenu);
	
	#sostituisco tutti gli href con l'indirizzo completo
	$position = index($logout, 'href="/', $startMenu);
	
	while ($position != -1) {
		substr($logout, $position, length('href="/'), "href=\"http://$address/$folderBase");
		$position = index($logout, 'href="/', $position + length("href=\"http://$address/$folderBase"));
	}
	
	unlink($sitePath . "reservedzone/logout.html");
	&createFile($sitePath . "reservedzone/logout.html", $logout);
	
	my $logIncorrect = &openFile($sitePath . "reservedzone/loginincorrect.html");
	
	#cerco inizio e fine del div id="navigation"
	$startMenu = index($logIncorrect,"<div id=\"navigation\"");
	$endDiv = index($logIncorrect, "</div>", $startMenu);
	
	#sostituisco tutti gli href con l'indirizzo completo
	$position = index($logIncorrect, 'href="/', $startMenu);
	
	while ($position != -1) {
		substr($logIncorrect, $position, length('href="/'), "href=\"http://$address/$folderBase");
		$position = index($logIncorrect, 'href="/', $position + length("href=\"http://$address/$folderBase"));
	}
	
	#elimino il div id="headerUtility"
	$divDeleteStart = index($logIncorrect, "<div id=\"headerUtility\">");
	$divDeleteEnd = index($logIncorrect, "</div>", $divDeleteStart) + length("</div>");
	substr($logIncorrect, $divDeleteStart, $divDeleteEnd - $divDeleteStart, "");
	
	unlink($sitePath . "reservedzone/loginincorrect.html");
	&createFile($sitePath . "reservedzone/loginincorrect.html", $logIncorrect);
		
	print "ReservedTemplate";
}
