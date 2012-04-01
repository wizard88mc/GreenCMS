#!/usr/bin/perl

use DBI;
use DBD::mysql;
use HTML::Entities;
use utf8;

require "WorkWithFiles.pl";
require "GlobalVariables.pl";
require "ConnectDatabase.pl";
require "GetTeachersID.pl";
require "GetTeacherInformations.pl";

#funzione che genera testo a caso
sub generateRandomString() {
	my $length_of_randomstring=10;# the length of 
			 # the random string to generate

	my @chars=('a'..'z');
	my $random_string;
	foreach (1..$length_of_randomstring) 
	{
		# rand @chars will generate a random 
		# number between 0 and scalar @chars
		$random_string.=$chars[rand @chars];
	}
	return $random_string;
}

#funzione che sostituisce l'indirizzo email con l'indirizzo nascosto
sub createMaskedEmail() {
	
	my $address = $_[0];	
	
	my $firstPart = substr($address, 0, index($address, "@"));
	my $secondPart = substr($address, index($address, "@") + 1);

	my $addressMasked = "";

	my $randomString = &generateRandomString();	
	$addressMasked .= "<span class=\"aiutoxVisualizzazione\">$randomString</span>";
	$addressMasked .= "<span class=\"nonCambia\">$firstPart</span>";
	$randomString = &generateRandomString();
	$addressMasked .= "<span class=\"aiutoxVisualizzazione\">$randomString</span>";
	$addressMasked .= "<span class=\"nonCambia\">\@</span>";
	$randomString = &generateRandomString();
	$addressMasked .= "<span class=\"aiutoxVisualizzazione\">$randomString</span>";
	$addressMasked .= "<span class=\"nonCambia\">$secondPart</span>";
	$randomString = &generateRandomString();
	$addressMasked .= "<span class=\"aiutoxVisualizzazione\">$randomString</span>";
	
	
	return $addressMasked;
	
}



{
	my $pageTeachers = &openFile($siteForCGI . "organizzazione/docenti.html") or die "$!";
	
	my $srcPath = "src=\"../";
	my $hrefPath = "href=\"../";
	my $newSRC = "src=\"/$folderBase";
	my $newHREF = "href=\"/$folderBase";
	my $linkOrg = "href=\"/$folderBase" . "organizzazione/index.html\"";
	my $oldLinkOrg = "href=\"index.html\"";
	
	$pageTeachers =~ s/$oldLinkOrg/$linkOrg/g; 
	$pageTeachers =~ s/$srcPath/$newSRC/g; 
	$pageTeachers =~ s/$hrefPath/$newHREF/g; 
	
	$pageTeachers =~ s/docentien.html/Docentien.cgi/g;
	
	eval {
	
		my $DBIConnection = &connectDatabase("www") or die "$!";

		my $idTP = "2";
		my $idTG = "121";

		my $teachersID = &getTeachersID($DBIConnection, $idTP, $idTG) or die "$!";

		my $tableInternalTeachers = "
			<table summary=\"La tabella presenta l'elenco dei professori che fanno parte del CCS, presentando nome (con eventuale link al loro sito personale), 
			l'indirizzo email, il numero di telefono ed il numero dell'ufficio  \">
			<caption>Elenco Docenti Interni</caption>";
		$tableInternalTeachers .= "
			<thead>
				<tr>
				<th id=\"c1\" abbr=\"Docente\" scope=\"col\">Docente</th>
				<th id=\"c2\" abbr=\"email\" scope=\"col\">Email</th>
				<th id=\"c3\" abbr=\"Telefono\" scope=\"col\">Numero Telefono</th>
				<th id=\"c4\" abbr=\"Ufficio\" scope=\"col\">Numero Ufficio</th>
				</tr>
			</thead>
			<tbody>";

		my $i = 0;
		
		while (my $teacher = $teachersID->fetchrow_hashref()) {   

			my $teacherID = $teacher->{'ID'};
			
			my %informations = %{&getTeacherInformations($DBIConnection, $teacherID)};

			my $teacherName = $informations{"Cognome"} . " " . $informations{"Nome"};
			
			my $teacherEmail = $informations{"Email"};
			my $teacherPhone = $informations{"Telefono"};
			my $teacherOffice = $informations{"Ufficio"};
			my $teacherSite = $informations{"Sito"};
			my $teacherCollapsed = $informations{"Nome"}.$informations{"Cognome"};
			$teacherCollapsed =~ s/ //g;
			encode_entities($teacherCollapsed);
			$teacherCollapsed =~ s/&Agrave;/a/g;
			$teacherCollapsed =~ s/&agrave;/a/g;
			$teacherCollapsed =~ s/&Egrave;/e/g;
			$teacherCollapsed =~ s/&egrave;/e/g;
			$teacherCollapsed =~ s/&Igrave;/i/g;
			$teacherCollapsed =~ s/&igrave;/i/g;
			$teacherCollapsed =~ s/&Ograve;/o/g;
			$teacherCollapsed =~ s/&ograve;/o/g;
			$teacherCollapsed =~ s/&Ugrave;/u/g;
			$teacherCollapsed =~ s/&ugrave;/u/g;
			
			my $stringRow = "";
			
			if ($i % 2 == 0) { 
				$stringRow = "<tr id=\"$teacherCollapsed\">";
			}
			else {
				$stringRow = "<tr class=\"alternate\" id=\"$teacherCollapsed\">";
			}
			
			if ($teacherSite eq "" || $teacherSite eq "NULL") {
			
				$stringRow .= "
					<td headers=\"c1\">$teacherName</td>";
			}
			else {
			
				$stringRow .= "
					<td headers=\"c1\"><a href=\"$teacherSite\">$teacherName</a></td>";
			}
			
			my $maskedEmail = &createMaskedEmail($teacherEmail);
			
			$stringRow .= "
					<td headers=\"c2\">$maskedEmail</td>
					<td headers=\"c3\">$teacherPhone</td>
					<td headers=\"c4\">$teacherOffice</td>";
			
			$stringRow .= "
				</tr>";
				
			$tableInternalTeachers .= $stringRow;
			
			$i = $i + 1;
				
		}

		$tableInternalTeachers .= "
			</tbody>
			</table>";
			
		my $tableExternalTeachers = "
			<table summary=\"La tabella presenta l'elenco dei docenti esterni che fanno parte del CCS, presentando nome (con eventuale link al loro sito personale), 
			l'indirizzo email, il numero di telefono ed il numero dell'ufficio  \">
			<caption>Elenco Docenti Interni</caption>";
			
		$tableExternalTeachers .= "
			<thead>
				<tr>
				<th id=\"c1a\" abbr=\"Docente\" scope=\"col\">Docente</th>
				<th id=\"c2a\" abbr=\"email\" scope=\"col\">Email</th>
				<th id=\"c3a\" abbr=\"Telefono\" scope=\"col\">Numero Telefono</th>
				<th id=\"c4a\" abbr=\"Ufficio\" scope=\"col\">Numero Ufficio</th>
				</tr>
			</thead>
			<tbody>";
			
		$idTP = "10";
		$idTG = "121";

		my $teachersID = &getTeachersID($DBIConnection, $idTP, $idTG);

		$i = 0;
		
		while (my $teacher = $teachersID->fetchrow_hashref()) {   

			my $teacherID = $teacher->{'ID'};
			
			my %informations = %{&getTeacherInformations($DBIConnection, $teacherID)};

			my $teacherName = $informations{"Cognome"} . " " . $informations{"Nome"};
			my $teacherEmail = $informations{"Email"};
			my $teacherPhone = $informations{"Telefono"};
			my $teacherOffice = $informations{"Ufficio"};
			my $teacherSite = $informations{"Sito"};
			my $teacherCollapsed = $informations{"Nome"}.$informations{"Cognome"};
			$teacherCollapsed =~ s/ //g;
			encode_entities($teacherCollapsed);
			$teacherCollapsed =~ s/&Agrave;/a/g;
			$teacherCollapsed =~ s/&agrave;/a/g;
			$teacherCollapsed =~ s/&Egrave;/e/g;
			$teacherCollapsed =~ s/&egrave;/e/g;
			$teacherCollapsed =~ s/&Igrave;/i/g;
			$teacherCollapsed =~ s/&igrave;/i/g;
			$teacherCollapsed =~ s/&Ograve;/o/g;
			$teacherCollapsed =~ s/&ograve;/o/g;
			$teacherCollapsed =~ s/&Ugrave;/u/g;
			$teacherCollapsed =~ s/&ugrave;/u/g;
			
			my $stringRow = "";
			
			if ($i % 2 == 0) {
				$stringRow = "<tr id=\"$teacherCollapsed\">";
			}
			else {
				$stringRow = "<tr class=\"alternate\" id=\"$teacherCollapsed\">";
			}

			if ($teacherSite eq "" || $teacherSite eq "NULL") {
			
				$stringRow .= "
					<td headers=\"c1a\">$teacherName</td>";
			}
			else {
			
				$stringRow .= "
					<td headers=\"c1a\"><a href=\"$teacherSite\">$teacherName</a></td>";
			}
			
			my $maskedEmail = &createMaskedEmail($teacherEmail);
			
			$stringRow .= "
					<td headers=\"c2a\">$maskedEmail</td>
					<td headers=\"c3a\">$teacherPhone</td>
					<td headers=\"c4a\">$teacherOffice</td>";
			
			$stringRow .= "
				</tr>";
				
			$tableExternalTeachers .= $stringRow;
			
			$i = $i+1;
		}

		$tableExternalTeachers .= "
			</tbody>
			</table>";
		
		$DBIConnection->disconnect();

		utf8::encode($tableInternalTeachers);
		utf8::encode($tableExternalTeachers);
		
		$pageTeachers =~ s/<teachersTable\/>/$tableInternalTeachers/;
		$pageTeachers =~ s/<externalTeachersTable\/>/$tableExternalTeachers/;
		
		print <<PAGE;
Content-type: text/html\n\n
$pageTeachers

PAGE
	}
	or do {
		
		$tableInternalTeachers = "DB non raggiungbile. Problemi tecnici";
		$tableExternalTeachers = "DB non raggiungbile. Problemi tecnici";
		
		$pageTeachers =~ s/<teachersTable\/>/$tableInternalTeachers/;
		$pageTeachers =~ s/<externalTeachersTable\/>/$tableExternalTeachers/;
		
		print <<PAGE;
Content-type: text/html\n\n
$pageTeachers

PAGE
	
	}



}
