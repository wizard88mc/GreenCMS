#!/usr/bin/perl

use XML::LibXML;
use utf8;


sub updatePHDStudentEn() {
	
	my $pageTemplatePHDStudents = &openFile($siteForCGI . "dottorato/dottoratotemplateen.html") or die "$!";
	
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
			
			my $stringSup;
			
			if ($supWebsite ne "") {
				$stringSup .= "<span><a href=\"http://$supWebsite\" xml:lang=\"it\">$supName $supSurname</a></span>";
			}
			else {
				$stringSup .= "<span xml:lang=\"it\">$supName $supSurname</span>";
			}
			
			my $phdString;
			if ($phdWebsite ne "") {
				$phdString .= "<dt><span><a href=\"http://$phdWebsite\" xml:lang=\"it\">$phdName $phdSurname</a></span></dt>";	
			}
			else {
				$phdString .= "<dt xml:lang=\"it\">$phdName $phdSurname</dt>";
			}
			
			if ($researchLanguage eq "en") {
			
				$phdString .= "<dd><span><strong>Research Area: </strong>$phdResearch</span></dd>";
			}
			else {
				$phdString .= "<dd><span><strong>Research Area: </strong><span xml:lang=\"it\">$phdResearch</span></span></dd>";
			}
			
			$phdString .= "<dd><span><strong>Supervisor: </strong>$stringSup</span></dd>";
			 
			 $stringCycle .= $phdString;
		}
		
		$stringCycle .= "</dl>";
		$stringPHDStudents .= $stringCycle;
		
		
	}
	
	utf8::encode($stringPHDStudents);
	
	$pageTemplatePHDStudents =~ s/<listPHDStudents\/>/$stringPHDStudents/g; 
	
	#unlink("../dottorato/dottorato.html");
	my $page = $siteForCGI . "dottorato/indexen.html";
	unlink($page);
	
	&createFile($page, $pageTemplatePHDStudents);
	system("chgrp www-data $page");
	
}

1;
