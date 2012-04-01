#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use utf8;

require "SendMail.cgi";

sub sendMailWebmaster() {

	my %fields = %{$_[0]};
	
	my $message = 
"$fields{'name'} $fields{'surname'} ($fields{'email'}) scrive:
Oggetto: $fields{'subject'}
Messaggio: $fields{'messageMail'}";

	utf8::encode($message);
	
	my %messageDetails;
	
	$messageDetails{'message'} = $message;
	$messageDetails{'emailTo'} = 'webinformatica@math.unipd.it';
	$messageDetails{'email'} = $fields{'email'};
	$messageDetails{'subject'} = 'Nuovo messaggio da informatica.math.unipd.it';
	
	my $result = &sendMail(\%messageDetails);
	
	return $result;

}

1;
