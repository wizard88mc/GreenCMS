#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use utf8;

binmode STDIN, ":utf8";
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";

require "GlobalVariables.pl";

sub createHead() {

print <<HEAD;
Content-type: text/html\n\n
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"  xml:lang="it" lang="it">
<head>
    <title>$_[0]</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <meta name="title" content="Area Riservata" />
	<meta name="language" content="italian it" />

	<link type="text/css" rel="stylesheet" href="$sitePath/style/base.css" media="screen" />
</head>
<body>
HEAD
}

1;

