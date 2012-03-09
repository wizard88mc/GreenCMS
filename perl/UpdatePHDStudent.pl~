#!/usr/bin/perl

use XML::LibXML;

require "GlobalVariables.pl";
require "WorkWithFiles.pl";
require "ExtractXML.pl";

#funzione che permette l'aggioranmento della pagina dei dottorandi
sub updatePHDStudent() {
	
	#recupero testo della pagina di template
	my $pageTemplatePHDStudents = &openFile($sitePath . "dottorato/index.html") or die "$!";
	
	my $fileXMLPHD = $sitePath . "xml_files/PHDStudentSupervisor.xml";
	
	my $root = &extractXML($fileXMLPHD);
	
	#recupero dal file XML le tabelle dei dottorandi, dei supervisori e dei cicli di dottorato
	my $tablePHD = $root->find("//TablePHDStudent")->get_node(1);
	my $tableSupervisor = $root->find("//TableSupervisor")->get_node(1);
	my $tableCycle = $root->find("//TableCycle/Cycle");
	
	my $stringPHDStudents = "";
	
	#per ogni ciclo di dottorato
	foreach my $cycle ($tableCycle->get_nodelist) {
		
		#recupero ID del ciclo, il suo nome (es XVII ciclo), il suo anno di inizio e quello di fine
		my $cycleID = $cycle->findvalue('ID');
		my $cycleName = $cycle->findvalue('Name');
		my $bYear = $cycle->findvalue('BeginningYear');
		my $eYear = $cycle->findvalue('EndYear');
		
		#costruisco stringa costruzione dottorato
		my $stringCycle = "<h3>$cycleName ($bYear &rarr; $eYear)</h3><dl>";
		
		#recupero dottorandi che appartengono a quel ciclo
		my $phdCorrect = $tablePHD->find("//PHDStudent[Cycle=$cycleID]");
		
		foreach my $phd ($phdCorrect->get_nodelist) {
			
			#recupero nome, cognome, sito internet, area di ricerca e supervisore
			my $phdName = $phd->findvalue('Name');
			my $phdSurname = $phd->findvalue('Surname');
			my $phdWebsite = $phd->findvalue('Website');
			my $phdResearch = $phd->findvalue('ResearchArea');
			my $phdSupervisor = $phd->findvalue('Supervisor');
			my $lang = $phd->findvalue('ResearchArea/@language');
			
			#recupero nome cognome e sito internet del supervisore del dottorando
			my $supName = $tableSupervisor->findvalue("//Supervisor[ID=$phdSupervisor]/Name");
			my $supSurname = $tableSupervisor->findvalue("//Supervisor[ID=$phdSupervisor]/Surname");
			my $supWebsite = $tableSupervisor->findvalue("//Supervisor[ID=$phdSupervisor]/Website");
			
			my $stringSup;
			
			#creo stringa del dottorando, distinguendo se ho il sito internet memorizzato o meno
			if ($supWebsite ne "") {
				$stringSup .= "<span><a href=\"http://$supWebsite\">$supName $supSurname</a></span>";
			}
			else {
				$stringSup .= "<span>$supName $supSurname</span>";
			}
			
			my $phdString; 
			#differenzio caso se è presente sito del dottorando o meno
			if ($phdWebsite ne "") {
				$phdString .= "<dt><span><a href=\"http://$phdWebsite\">$phdName $phdSurname</a></span></dt>";	
			}
			else {
				$phdString .= "<dt>$phdName $phdSurname</dt>";
			}
			
			if ($lang eq "it") {
				$phdString .= "<dd><span><strong>Area di Ricerca: </strong>$phdResearch</span></dd>";
			}
			else {
				$phdString .= "<dd><span><strong>Area di Ricerca: </strong><span xml:lang=\"en\">$phdResearch</span></span></dd>";
			}
			
			$phdString .= "<dd><span><strong>Supervisore: </strong>$stringSup</span></dd>";
			 
			 #aggiungo stringa del dottorato alla stringa del ciclo
			 $stringCycle .= $phdString;
		}
		
		$stringCycle .= "</dl>";
		#aggiungo stringa ciclo a stringa globale
		$stringPHDStudents .= $stringCycle;
		
		
	}
	
	#sostituisco al tag fittizio la stringa creata
	$pageTemplatePHDStudents =~ s/<listPHDStudents\/>/$stringPHDStudents/g;
	
	#unlink("../dottorato/dottorato.html");
	my $page = $sitePath . "dottorato/index.html";
	
	rename("$page", $sitePath . "dottorato/dottoratotemplate.html") or die "$!";
	
	open FILE, ">$page" or die "$!";
	print FILE "$pageTemplatePHDStudents";
	close (FILE);
	
	chmod(0775, $page);
	
	my $cmd = "chgrp www-data $page";
	system($cmd);
	
}

1;
