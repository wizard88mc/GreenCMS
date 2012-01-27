#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use CGI::Cookie;
use CGI::Session;
use utf8;

require "GlobalVariables.pl";

{
	
	$page = new CGI;
	
	%cookies = fetch CGI::Cookie;
	if (defined($cookies{'CGISESSIONID'})) {
		$sessionID = $cookies{'CGISESSIONID'}->value;
	
		if (defined($sessionID)) {
			print $page->redirect(-uri=>"https://$address/cgi-bin/MainAdministration.cgi");
		}
	}
	print $page->redirect(-uri=>"https://$address/" . $folderBase . "reservedzone/login.html");
	
	
}
