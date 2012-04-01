#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use utf8;

require "GlobalVariables.pl";
require "CreateSecondLevelMenu.cgi";
require "FunctionsAdmin.cgi";
require "WorkWithFiles.pl";

sub printFormAssignPermission() {
	
	my $message = $_[0];
	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}
	
	my $userOptions = &getUsers();
	
	my $permissionOptions = &getPermissions();
	
	my $content = <<CONTENT;
<div id="contents">
	<h1>Assegna Privilegi</h1>
	$message
	<form method="post" action="AssignPermission.cgi">
	<fieldset>
	<legend>Scelta Utente/Opzione</legend>
	<label for="userID">Utente: </label>
	<select name="userID" id="userID" >
	$userOptions
	</select>
	<br /><br />
	<label for="permissionID">Permesso: </label>
	<select name="permissionID" id="permissionID">
	$permissionOptions
	</select>
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" name="submit" class="button" value="Assegna" />
	<input type="reset" name="reset" value="Reset" class="button" />
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

$userFormInput{'submit'} = $page->param('submit');

my $stringSecondLevel = &createSecondLevelMenu();
my $title = "Assegna Permessi";
my $content = &printFormAssignPermission();

if ($userFormInput{'submit'} eq "Assegna") {
	
	$userFormInput{'userID'} = $page->param('userID');
	$userFormInput{'permissionID'} = $page->param('permissionID');
	
	my $result = &assignPermission($userFormInput{'userID'}, $userFormInput{'permissionID'});
	$content = &printFormAssignPermission($result);
		
}

utf8::encode($content);

my $template = &openFile($siteForCGI . "reservedzone/reservedtemplate.html") or die "$!";

$content = $stringSecondLevel . $content;
	
$template =~ s/<pageContent\/>/$content/g;
$template =~ s/<pageTitle\/>/$title/g;
	
print <<CONTENT;
Content-type:text/html\n\n
$template

CONTENT
