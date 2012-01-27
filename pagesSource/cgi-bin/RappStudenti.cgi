#!/usr/bin/perl

use DBI;
use DBD::mysql;
use utf8;

require "GlobalVariables.pl";
require "WorkWithFiles.pl";
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

	#genero alternanza testo giusto testo finto
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
	#apro file html per i rappresentanti degli studenti
	my $pageRappStud = &openFile($siteForCGI . "organizzazione/rappresentantistudenti.html");
	
	#connetto al database www
	my $DBIConnection = &connectDatabase("www");

	#input per avere i rappresentanti degli studenti
	my $idTP = "12";
	my $idTG = "121";

	#recupero ID dei rappresentanti
	my $rappStudentsID = &getTeachersID($DBIConnection, $idTP, $idTG);

	#inizializzo tabella rappresentati con summary e caption
	my $tableRapp = "
		<table summary=\"La tabella presenta l'elenco dei rappresentanti degli studenti per i corsi di Laurea, con il loro nome ed il loro indirizzo email\">
		<caption>Elenco Rappresentanti Studenti</caption>";
	
	#aggiungo head per la tabella
	$tableRapp .= "
		<thead>
			<tr>
			<th id=\"c1\" abbr=\"Nome\" scope=\"col\">Rappresentante</th>
			<th id=\"c2\" abbr=\"email\" scope=\"col\">Email</th>
			</tr>
		</thead>
		<tbody>";

	my $i = 0;
	
	#per ogni rappresentante recuperato
	while (my $representative = $rappStudentsID->fetchrow_hashref()) {   

		#recupero ID
		my $representativeID = $representative->{'ID'};
		
		#recupero informazioni
		my %informations = %{&getTeacherInformations($DBIConnection, $representativeID)};

		#creo Cognome Nome
		my $rappName = $informations{"Cognome"} . " " . $informations{"Nome"};
		my $rappEmail = $informations{"Email"};
		
		my $stringRow = "";
		
		#inizializzo riga con classe alternate o meno
		if ($i % 2 == 0) {
			$stringRow = "<tr>";
		}
		else {
			$stringRow = "<tr class=\"alternate\">";
		}
		
		#aggiungo nome alla riga
		$stringRow .= "
			<td headers=\"c1\">$rappName</td>";
		
		#creo email mascherata
		my $maskedEmail = &createMaskedEmail($rappEmail);
			
		$stringRow .= "
				<td headers=\"c2\">$maskedEmail</td>";
		
		$stringRow .= "
			</tr>";
			
		$tableRapp .= $stringRow;
		
		$i = $i + 1;
			
	}

	#chiudo tabella
	$tableRapp .= "
		</tbody>
		</table>";

	#chiudo connessione
	$DBIConnection->disconnect();
	
	utf8::encode($tableRapp);

	#modifico i path ed i collegamenti
	my $srcPath = "src=\"../";
	my $hrefPath = "href=\"../";
	my $newSRC = "src=\"/$folderBase";
	my $newHREF = "href=\"/$folderBase";
	my $folder = "organizzazione/";
	
	my $ulSecond = index($pageRappStud, "div id=\"contents");
	my $endSecond = index($pageRappStud, "/ul", $ulSecond);
	my $href = index($pageRappStud, "href=\"", $ulSecond);
	
	
	while ($href != -1 && $href < $endSecond) {
		
		my $endLink = index($pageRappStud, "\"", $href + length("href=\""));
		my $link = substr($pageRappStud, $href, $endLink - $href);
		if (index($link, '.cgi') == -1) {
			substr($pageRappStud, $href, length("href=\""), "href=\"/$folderBase" . $folder);
		}
		
		$href = index($pageRappStud, "href=\"", $href + length("href=\"") + 5);
		
	}
	
	$pageRappStud =~ s/$srcPath/$newSRC/g; 
	$pageRappStud =~ s/$hrefPath/$newHREF/g; 
	$pageRappStud =~ s/<rappStudentsTable\/>/$tableRapp/;  
	
	$pageRappStud =~ s/rappresentantistudentien.html/RappStudentien.cgi/g;

print <<PAGE;
Content-type: text/html\n\n
$pageRappStud

PAGE

}
