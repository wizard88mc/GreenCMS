#!/usr/bin/perl 

require "/etc/apache2/informatica_dev/perl/GlobalVariables.pl";
require "/etc/apache2/informatica_dev/perl/GlobalFunctions.pl";
require "/etc/apache2/informatica_dev/perl/MoveNewActiveNews.pl";
require "/etc/apache2/informatica_dev/perl/MoveNewsCron.pl";
require "/etc/apache2/informatica_dev/perl/SendEventMailCron.pl";



{

    &moveNewActiveNews();	
	&moveNewsCron();
	&sendEventMailCron();
	
}
