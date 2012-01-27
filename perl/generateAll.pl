#!/usr/bin/perl

use utf8;

binmode STDIN, ":utf8";
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";

require "CreatePages.pl";
require "CreatePageCoursesLaurea.pl";
require "CreatePageCoursesMagistrale.pl";
require "GlobalVariables.pl";
require "MoveFolders.pl";
require "CreateReservedTemplate.pl";
require "UpdatePHDStudent.pl";
require "UpdatePHDStudentEn.pl";
require "CreatePageCoursesMagistraleEn.pl";
require "CreatePageCoursesLaureaEn.pl";
require "UpdatePageArchiveThesis.pl";

{
	&moveFolders();
	&createPages();
	
	&createPageCoursesLaurea();
	&createPageCoursesMagistrale();
	&createPageCoursesLaureaEn();
	&createPageCoursesMagistraleEn();
	
	&updatePHDStudent();
	&updatePHDStudentEn();
	
	&updatePageArchiveThesis();
	
	&createReservedTemplate();
	
	#my @commands = ("chgrp -R", "www-data", "/var/www");
	my $command = "chgrp -R www-data /var/www/";
	system($commands);
	
	my $commands = "chmod -R 777 /var/www";
	system($commands);
	
	print "\n Script Completed \n";
	
	
}
