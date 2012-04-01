#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use XML::Simple;
use Data::Dumper;
use utf8;

binmode STDIN, ":utf8";
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";

require "GlobalVariables.pl";

sub createFirstLevelMenu() {

print <<NAVIGATION;
<div id="navigation">
	<ul>
		<li><a href="http://lauree-informatiche.math.unipd.it/testing/index.html">Home</a></li>
		<li><a href="http://lauree-informatiche.math.unipd.it/testing/laurea/laurea.html">Laurea in Informatica</a></li>
		<li><a href="http://lauree-informatiche.math.unipd.it/testing/laureamagistrale/laureamagistrale.html">Laurea Magistrale in Informatica</a></li>
		<li><a href="http://lauree-informatiche.math.unipd.it/testing/dottorato/dottorato.html">Dottorato di Ricerca in Informatica</a></li>
		<li><a href="http://lauree-informatiche.math.unipd.it/testing/organizzazione/organizzazione.html">Organizzazione</a></li>
		<li><a href="http://lauree-informatiche.math.unipd.it/cgi-bin/News.cgi">News, eventi e seminari</a></li>
		<li><a href="#">Studiare all'estero</a></li>
		<li><a href="http://lauree-informatiche.math.unipd.it/testing/servizi/index.html">Servizi</a></li>
		<li><a href="http://lauree-informatiche.math.unipd.it/testing/strutture/index.html">Strutture</a></li>
		<li><a href="#">Archivio</a></li>
	</ul>
</div>
NAVIGATION
}


1;