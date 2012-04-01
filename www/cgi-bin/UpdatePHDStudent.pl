#!/usr/bin/perl

use XML::LibXML;

require "GlobalVariables.pl";
require "WorkWithFiles.pl";


sub updatePHDStudent() {
	
	my $pageTemplatePHDStudents = &openFile($siteForCGI . "dottorato/templatedottorato.html");
	
	$fileXML .= "PHDStudentSupervisor.xml";
	
	my $parser = XML::LibXML->new();
	
	my $document = $parser->parse_file($fileXML);
	my $root = $document->getDocumentElement;
	
	my $tablePHD = $root->find("//TablePHDStudent")->get_node(1);
	my $tableSupervisor = $root->find("//TableSupervisor")->get_node(1);
	my $tableCycle = $root->find("//TableCycle/Cycle");
	
	my $stringPHDStudents = "";
	
	foreach my $cycle ($tableCyle->get_nodelist) {
		
		my $cycleID = $cycle->findvalue('ID');
		my $cycleName = $cycle->findvalue('Name');
		my $bYear = $cycle->findvalue('BeginningYear');
		my $eYear = $cycle->findvalue('EndYear');
		
		my $stringCycle = "<h3>$cycleName ($bYear -> $eYear)</h3>";
		
		my $phdCorrect = $tablePHD->find("//PHDStudent[Cycle=$cycleID");
		
		foreach my $phd ($phdCorrect->get_nodelist) {
			
			my $phdName = $phd->findvalue('Name');
			my $phdSurname = $phd->findvalue('Surname');
			my $phdWebsite = $phd->findvalue('Website');
			my $phdResearch = $phd->findvalue('ResearchArea');
			my $phdSupervisor = $phd->findvalue('Supervisor');
			
			my $supName = $tableSupervisor->findvalue("//Supervisor[ID=$phdSupervisor]/Name");
			my $supSurname = $tableSupervisor->findvalue("//Supervisor[ID=$phdSupervisor]/Surname");
			my $supWebsite = $tableSupervisor->findvalue("//Supervisor[ID=$phdSupervisor]/Website");
			
			my $stringSup;
			
			if ($supWebsite ne "") {
				$stringSup .= "<dt><a href=\"$supWebsite\">$supName $supSurname</a></dt>";
			}
			else {
				$stringSup .= "<dt>$supName $supSurname</dt>";
			}
			
			my $phdString;
			if ($phdWebsite ne "") {
				$phdString .= "<dt><a href=\"$phdWebsite\">$phdName $phdSurname</a></dt>";	
			}
			else {
				$phdString .= "<dt>$phdName $phdSurname</dt>";
			}
			
			$phdString .=
			 "<dd><strong>Area di Ricerca: </strong>$phdResearch</dd>
			 <dd><strong>Supervisore: </strong>$stringSup</dd>";
			 
			 $stringCycle .= $phdString;
		}
		
		$stringPHDStudent .= $stringCycle;
		
		
	}
	
	$pageTemplatePHDStudents =~ s/<listPHDStudents\/>/$stringPHDStudent/g; 
	
	&createFile($siteForCGI . "dottorato/dottorato.html", $pageTemplatePHDStudents);
	
}
