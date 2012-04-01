#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use utf8;

require "WorkWithFiles.pl";
require "GlobalVariables.pl";
require "SendEmailWebmaster.cgi";


sub printFormMessage() {
	
	my $message = $_[0];
	if ($message ne "") {
		$message = "<div id=\"message\">$message</div>";
	}
	
	my $content = <<CONTENT;
	$message
	<form method="post" action="ContactWebmasteren.cgi">
	<fieldset>
	<legend>General informations</legend>
	<label for="name">Name: </label>
	<input type="text" name="name" id="name" value="$userFormInput{'name'}" /><br />
	<label for="surname">Surname: </label>
	<input type="text" name="surname" id="surname" value="$userFormInput{'surname'}" /><br />
	<label for="email">Email: </label>
	<input type="text" name="email" id="email" value="$userFormInput{'email'}" /><br />
	</fieldset>
	<fieldset>
	<legend>Message</legend>
	<label for="subject">Subject: </label>
	<input type="text" name="subject" id="subject" value="$userFormInput{'subject'}" />
	<label for="messageMail">Message: </label>
	<textarea id="messageMail" name="messageMail" cols="20" rows="5">$userFormInput{'messageMail'}</textarea>
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" name="submit" value="Send" class="button" />
	<input type="reset" value="Reset" class="button" />
	</fieldset>
	</form>
CONTENT

	return $content;

}


sub printThanks() {
	
	my $content = <<CONTENT;
	<p>Operation complete. Thank you to contact us</p>
CONTENT

	return $content;
}


sub checkBadContent() {
	
	my $string = $_[0];

	if ((index($string, "<?") != -1) || (index($string, "?>") != -1) || (index($string, "<\%") != -1) || (index($string, "\%>") != -1)
		|| (index($string, "script") != -1) || (index($string, "/script") != -1)) {
		return "bad";
		}
		
	return "";


}


sub checkFields() {
	
	
	my $errors = "";
	if ($userFormInput{'name'} !~ /^\D{3}(\D)*$/ || (&checkBadContent($userFormInput{'name'}) ne "")) {
    	$errors .= "Name non correct<br />";
    }
    if ($userFormInput{'surname'} !~ /^\D{3}(\D)*$/ || (&checkBadContent($userFormInput{'surname'}) ne "")) {
    	$errors .= "Surname non correct<br />";
    }
	if ($userFormInput{'email'} !~ /^([\w\-\+\.]+)([\w]+)\@([\w]+)([\w\-\+\.]+)\.([\w\-\+\.]+)$/ || (&checkBadContent($userFormInput{'email'}) ne "")) {
    	$errors .= "Email address not correct<br />";
    }
    if (length($userFormInput{'subject'}) < 5 || (&checkBadContent($userFormInput{'subject'}) ne "")) {
    	$errors .= "Message subject not correct<br />";		
    }
    if (length($userFormInput{'messageMail'}) < 30 || (&checkBadContent($userFormInput{'messageMail'}) ne "")) {
    	$errors .= "Messagge not correct<br />";		
    }
	
	return $errors;
	
}


$page = new CGI;

$userFormInput{'submit'} = $page->param('submit');

$content = &printFormMessage();

if ($fields{'submit'} eq "Send") {
	
	$userFormInput{'name'} = $page->param('name');
	$userFormInput{'surname'} = $page->param('surname');
	$userFormInput{'email'} = $page->param('email');
	$userFormInput{'subject'} = $page->param('subject');
	$userFormInput{'messageMail'} = $page->param('messageMail');
	
	foreach $userInput (keys %userFormInput) {
		if ($userFormInput{$userInput} eq 0) {
			$userFormInput{$userInput} = "";
		}
		$userFormInput{$userInput} =~ s/"//g;
	}
	
	my $errors = &checkFields();	
	
	if ($errors eq "") {
		my $result = &sendMailWebmaster(\%userFormInput);
		
		if ($result eq "") {
			$content = &printThanks();	
		}
		else {
			$content = &printFormMessage("Some problems occured");
		}
	}
	else {
		$content = &printFormMessage($errors);	
	}
	
}

utf8::encode($content);

my $pageTemplate = &openFile($siteForCGI . "scriviwebmasteren.html");

$pageTemplate =~ s/scriviwebmaster.html/ContactWebmaster.cgi/g;

my $startP = index($pageTemplate, "<p id=\"linkPage\">");

my $endP = index($pageTemplate, "</p>", $startP);

substr($pageTemplate, $startP, $endP + length("</p>") - $startP, $content);

print <<CONTENT;
Content-type: text/html\n\n
$pageTemplate

CONTENT


