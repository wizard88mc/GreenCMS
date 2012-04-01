#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use utf8;
use Time::localtime;
use Date::Calc qw(Add_Delta_Days Delta_Days);

use DBI;
use DBD::mysql;
use XML::LibXML;
use HTML::Entities;
use File::Basename;
use utf8;

require "GlobalVariables.pl";
require "GlobalFunctions.cgi";
require "WorkWithFiles.pl";
require "CreateSecondLevelMenu.cgi";
require "FunctionsCommissioni.cgi";

#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use CGI::Session;
use CGI::Cookie;
use utf8;

require "GlobalVariables.pl";
require "GlobalFunctions.cgi";
require "WorkWithFiles.pl";
require "CreateSecondLevelMenu.cgi";
require "FunctionsCommissioni.cgi";


my $totaleCandidati = 16;
my $turni = 3;
my $candidatiPerTurnoBase;
my $resto;

{
    use integer;
$candidatiPerTurnoBase = $totaleCandidati / $turni;
$resto = $totaleCandidati % $turni;
}
my @candidatiPerTurno;

for (my $i = 0; $i < $turni; $i++) {
     $candidatiPerTurno[$i] = $candidatiPerTurnoBase;   
}

my $i = 0;
while ($i < $resto) {
     $candidatiPerTurno[$i]++;
     $i++;
}

print @candidatiPerTurno;
