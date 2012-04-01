#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use CGI::Cookie;
use CGI::Session;
use utf8;
use XML::LibXML;

require "GlobalVariables.pl";

{
$page = new CGI;
$username = $page->param('username');
$password = $page->param('password');


open SSLAUTH, "|-","/usr/local/sbin/sslunixauthenticate.sh", "/etc/SSLAUTH/sslauth-dip.conf" or die "Cannot open process pipe:$!\n";

print SSLAUTH "$username";
print SSLAUTH "\n";
print SSLAUTH "$password";
print SSLAUTH "\n";
close SSLAUTH;
$| = 1;

if ($? == 0 ){


	my $session = new CGI::Session("drive:File", undef, {Directory=>"/tmp"});


	my $sessionID = $session->id();
	my $cookie = new CGI::Cookie(-name=>'CGISESSIONID', -value=>"$sessionID", -expires=>'15m');
	
	$fileXML .= "UserPermission.xml";

	my $parser = XML::LibXML->new();
	
	my $document = $parser->parse_file($fileXML);
	my $root = $document->getDocumentElement;
	
	my $userID = $root->findvalue("//TableUser/User[UserID = \"$username\"]/ID");

	if ($userID eq "") {
		$userID = 0;
	}

	my $userPermissions = $root->find("//TableUserPermissions/UserPermission[UserID=$userID]");
	my $stringPermissions = "";
	
	foreach $userPermission ($userPermissions->get_nodelist) {
	
		$stringPermissions .= $userPermission->findvalue('IDPermission');
	
	}
	
	$session->param('userPermission', $stringPermissions);

	print $page->redirect(-uri=>"https://$address/cgi-bin/MainAdministration.cgi", -cookie=>$cookie);
		
}
else {
	
    print "Location: https://$address/" . $folderBase . "reservedzone/loginincorrect.html\n\n";
}

}
