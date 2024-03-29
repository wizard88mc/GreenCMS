#!/usr/bin/perl

use utf8;
use XML::LibXML;

sub updatePHDStudent() {

	
	my $pageTemplatePHDStudents = &openFile($siteForCGI . "dottorato/dottoratotemplate.html") or die "$!";
	
	my $phdStudents = $fileXML . "PHDStudentSupervisor.xml";
	
	my $parser = XML::LibXML->new();
	
	my $document = $parser->parse_file($phdStudents);
	my $root = $document->getDocumentElement;
	
	my $tablePHD = $root->find("//TablePHDStudent")->get_node(1);
	my $tableSupervisor = $root->find("//TableSupervisor")->get_node(1);
	my $tableCycle = $root->find("//TableCycle/Cycle");
	
	my $stringPHDStudents = "";
	
	foreach my $cycle ($tableCycle->get_nodelist) {
		
		my $cycleID = $cycle->findvalue('ID');
		my $cycleName = $cycle->findvalue('Name');
		my $bYear = $cycle->findvalue('BeginningYear');
		my $eYear = $cycle->findvalue('EndYear');
		
		my $stringCycle = "<h3>$cycleName ($bYear &rarr; $eYear)</h3><dl>";
		
		my $phdCorrect = $tablePHD->find("//PHDStudent[Cycle=$cycleID]");
		
		foreach my $phd ($phdCorrect->get_nodelist) {
			
			my $phdName = $phd->findvalue('Name');
			my $phdSurname = $phd->findvalue('Surname');
			my $phdWebsite = $phd->findvalue('Website');
			my $phdResearch = $phd->findvalue('ResearchArea');
			my $researchLanguage = $phd->findvalue('ResearchArea/@language');
			my $phdSupervisor = $phd->findvalue('Supervisor');
			
			my $supName = $tableSupervisor->findvalue("//Supervisor[ID=$phdSupervisor]/Name");
			my $supSurname = $tableSupervisor->findvalue("//Supervisor[ID=$phdSupervisor]/Surname");
			my $supWebsite = $tableSupervisor->findvalue("//Supervisor[ID=$phdSupervisor]/Website");
			
			my $stringSup = "";
			
			if ($supWebsite ne "") {
				$stringSup .= "<span><a href=\"http://$supWebsite\">$supName $supSurname</a></span>";
			}
			else {
				$stringSup .= "$supName $supSurname";
			}
			
			my $phdString = "";
			if ($phdWebsite ne "") {
				$phdString .= "<dt><span><a href=\"http://$phdWebsite\">$phdName $phdSurname</a></span></dt>";	
			}
			else {
				$phdString .= "<dt>$phdName $phdSurname</dt>";
			}
			
			if ($researchLanguage eq "en") {
			
				$phdString .= "<dd><span><strong>Area di Ricerca: </strong><span xml:lang=\"en\">$phdResearch</span></span></dd>";
			}
			else {
				$phdString .= "<dd><span><strong>Area di Ricerca: </strong>$phdResearch</span></dd>";
			}
			
			$phdString .= "<dd><span><strong>Supervisore: </strong>$stringSup</span></dd>";
			 
			 $stringCycle .= $phdString;
		}
		
		$stringCycle .= "</dl>";
		$stringPHDStudents = $stringCycle . $stringPHDStudents;
		
	}
	
	utf8::encode($stringPHDStudents);
	
	$pageTemplatePHDStudents =~ s/<listPHDStudents\/>/$stringPHDStudents/;
	
	#unlink("../dottorato/dottorato.html");
	my $page = $siteForCGI . "dottorato/index.html";
	unlink($page);
	
	&createFile($page, $pageTemplatePHDStudents);
	system("chgrp www-data $page");
	
}

1;
