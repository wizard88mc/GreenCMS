#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use utf8;
use CGI::Session;
use CGI::Cookie;

binmode STDIN, ":utf8";
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";

require "GlobalVariables.pl";

{
	
	$page = new CGI;
	
	%cookies = fetch CGI::Cookie;
	
	$sessionID = $cookies{'CGISESSIONID'}->value;
	
	$session = new CGI::Session("drive:File", $sessionID, {Directory=>"/tmp"});
	
	$session->expire('0m');
	
	$session->delete();
	
	my $cookie = new CGI::Cookie(-name=>'CGISESSIONID', -expires=>'0m');
	
	print $page->redirect(-uri=>"https://$address/$folderBase" . "reservedzone/logout.html", -cookie=>$cookie);
	
}
