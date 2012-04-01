#!/usr/bin/perl

use XML::LibXML;
use utf8;

require "WorkWithFiles.pl";
require "GlobalVariables.pl";

{
	
	my $pageCCS = &openFile($siteForCGI . "organizzazione/ccsen.html");
	
	my $fileXMLCCS = $fileXML . "CCSAttachedFile.xml";
	
	my $parser = XML::LibXML->new();
	
	my $document = $parser->parse_file($fileXMLCCS);
	my $root = $document->getDocumentElement;
	
	my $ccsList = $root->find("//TableCCS/CCS");
	
	my $stringGlobalPage = "";
	
	foreach my $ccs ($ccsList->get_nodelist) {
		
		my $id = $ccs->findvalue('ID');
		my $date = $ccs->findvalue('Date');
		my $folder = $date;
		$date = substr($date, 8, 2) . "/" . substr($date, 5, 2) . "/" . substr($date, 0, 4);
		my $agenda = $ccs->findvalue('Agenda');
		my $fileReport = $ccs->findvalue('FileReport');
		my $approved = $ccs->findvalue('Approved');
		$folder =~ s/\W//g;
		
		my $stringCCS = "<div class=\"ccs withBorderBottom\">";
		
		if ($approved eq "T") {
			$stringCCS .= "
			<h3>$date</h3>";
		}
		else {
			$stringCCS .= "<h3>$date <span id=\"approvazione\">Waiting Approvement</span></h3>";
		}
		
		my $newPoint = "</li><li>";
		my $godown = "\n";
		my $double = "</li></li>";
		my $single = "</li>";
		my $empty = "<li></li>";
		
		$agenda = "<ol><li xml:lang=\"it\">$agenda</li></ol>";
		$agenda =~ s/$godown/$newPoint/g;
		$agenda =~ s/$empty//g;
		$agenda =~ s/$double/$single/g;
		
		$stringCCS .= "<p><strong>Agenda: </strong><a href=\"" . $siteForCGI . $folderBase . "documenti/verbaliccs/$folder/$fileReport\">Report $date</a> [PDF]</p>$agenda";
		$stringCCS .= "<p><strong>Attachments: </strong>";
		my $attachedFilesList = $root->find("//TableAttachedFiles/AttachedFile[CCSAssociated=$id]");
		
		my $i = 0;
		my @letter = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "Z");
		
		foreach my $attachedFile ($attachedFilesList->get_nodelist) {
			my $fileName = $attachedFile->findvalue('FileName');
			my $file = $attachedFile->findvalue('File');
			my $fileExtension = substr($file, rindex($file, ".") + 1);
			$fileExtension = uc($fileExtension);
			
			$stringCCS .= " &emsp; <a href=\"" . $siteForCGI . $folderBase . "documenti/verbaliccs/$folder/$file\">Attachment $letter[$i]: <span xml:lang=\"it\">$fileName</span></a> [$fileExtension]";
			
			$i = $i + 1;
		}
		
		$stringCCS .= "<p class=\"tornaSu\"><a href=\"#contentsLong\">Move up &#9650;</a></p>";
		
		$stringCCS .= "</p></div>";
		
		
		$stringGlobalPage .= $stringCCS;
		
		
	}
	
	if (index($stringGlobalPage, "ccs") == -1) {
		$stringGlobalPage = "<p>No report inserted</p>";
	}
	
	$stringGlobalPage .= "<p><a href=\"http://lauree.math.unipd.it/laureainformatica/ccsArchivio.html\">Old reports</a> [italian page]</p>";
	
	utf8::encode($stringGlobalPage);
	
	my $srcPath = "src=\"../";
	my $hrefPath = "href=\"../";
	my $newSRC = "src=\"/$folderBase";
	my $newHREF = "href=\"/$folderBase";
	my $linkOrg = "href=\"/$folderBase" . "organizzazione/indexen.html\"";
	my $oldLinkOrg = "href=\"indexen.html\"";
	my $tag = "<reportCCS/>";
	
	$pageCCS =~ s/$oldLinkOrg/$linkOrg/g;
	$pageCCS =~ s/$srcPath/$newSRC/g; 
	$pageCCS =~ s/$hrefPath/$newHREF/g;
	$pageCCS =~ s/<reportCCS\/>/$stringGlobalPage/g;
	
	$pageCCS =~ s/ccs.html/CCS.cgi/g;
	$pageCCS =~ s/Docenti.cgi/Docentien.cgi/g;
	$pageCCS =~ s/RappStudenti.cgi/RappStudentien.cgi/g;
	
	
print <<PAGE;
Content-type: text/html\n\n
$pageCCS
	
PAGE
	
	
}







