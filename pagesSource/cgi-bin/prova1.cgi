#!/usr/bin/perl -w

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

require "InsertThesisPageArchive.cgi";
require "ConnectDatabase.pl";
require "GetTeachersID.pl";
require "GetTeacherInformations.pl";
require "WorkWithFiles.pl";

sub getOptionsRelatore() {
    
    my $optionsSelect = '<optgroup label="Docenti Interni">';
    
    my $DBIConnection = &connectDatabase("www") or die "$!";

    # identificativi per docente interno
    my $idTP = "2";
    my $idTG = "121";

    my $teachersID = &getTeachersID($DBIConnection, $idTP, $idTG) or die "$!";
    
    while (my $teacher = $teachersID->fetchrow_hashref()) {
        
        my $teacherID = $teacher->{'ID'};
        my $nameSurnameQuery = "SELECT Persona.VARCHAR02 as Cognome, Persona.VARCHAR03 as Nome
FROM Persona
WHERE Persona.ID = $teacherID; ";
        
       my $queryHandle = $DBIConnection->prepare($nameSurnameQuery);
        $queryHandle->execute();
	
        my ($surname, $name) = $queryHandle->fetchrow_array();
        
        my $teacherName = $surname . ' ' . $name;
        
        $optionsSelect .= "<option value=\"$teacherName\">$teacherName</option>";
        
    }
    
    $optionsSelect .= '</optgroup>';
    
    $optionsSelect .= '<optgroup label="Docenti Esterni">';
    #identificativi per docente esterno
    $idTP = "10";
	$idTG = "121";
	
	$teachersID = &getTeachersID($DBIConnection, $idTP, $idTG) or die "$!";
    
    while (my $teacher = $teachersID->fetchrow_hashref()) {
        
        my $teacherID = $teacher->{'ID'};
        my $nameSurnameQuery = "SELECT Persona.VARCHAR02 as Cognome, Persona.VARCHAR03 as Nome
FROM Persona
WHERE Persona.ID = $teacherID; ";
        
        my $queryHandle = $DBIConnection->prepare($nameSurnameQuery);
        $queryHandle->execute();
	
        my ($surname, $name) = $queryHandle->fetchrow_array();
        
        my $teacherName = $surname . ' ' . $name;
        
        $optionsSelect .= "<option value=\"$teacherName\">$teacherName</option>";
        
    }
	
    $optionsSelect .= '</optgroup>';
    
    $DBIConnection->disconnect();
    
    return $optionsSelect;
}

print &getOptionsRelatore();
