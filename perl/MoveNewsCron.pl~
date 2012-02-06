#/usr/bin/perl 

use XML::LibXML;
use Date::Calc qw(Today Delta_Days);
use Time::localtime;

require "/etc/apache2/informatica_dev/perl/GlobalVariables.pl";
require "/etc/apache2/informatica_dev/perl/ExtractXML.pl";


#metodo che sposta news scadute nell'apposito file e le elimina da ActiveNews.xml
sub moveNewsCron() {

	my $fileActiveNews = $sitePath . "xml_files/ActiveNews.xml";
	my $rssfeedFile = $sitePath . "xml_files/rssfeed.xml";
	
	my $parserActive = XML::LibXML->new();
	my $documentActive = $parserActive->parse_file($fileActiveNews);
	my $parserRSS = XML::LibXML->new();
	my $documentRSS = $parserRSS->parse_file($rssfeedFile);
	
	#estraggo la radice del file XML
	my $rootActive = $documentActive->getDocumentElement;
	my $rootRSS = $documentRSS->getDocumentElement;
	
	my $tableActiveNews = $rootActive->find("//TableActiveNews/ActiveNews");
	
	my $actualYear = localtime->year() + 1900;
	my $actualMonth = localtime->mon() + 1;
	if (length($actualMonth) == 1) {
		$actualMonth = "0$actualMonth";
	}
	my $actualDay = localtime->mday();
	if (length($actualDay) == 1) {
		$actualDay = "0$actualDay";
	}
	
	foreach my $activeNews ($tableActiveNews->get_nodelist) {
		
		my $title = $activeNews->findvalue('Title');
		my $expirationDate = $activeNews->findvalue('ExpirationDate');
		
		my ($expirationDay, $expirationMonth, $expirationYear) = 
		            &getDateComponentsFromDBDate($expirationDate);
		
		my $delta = Delta_Days($actualYear, $actualMonth, $actualDay, $expirationYear, $expirationMonth, $expirationDay);
		
		if ($delta < 0) {
			
			my $archive = $activeNews->findvalue('Archive');
			
			if ($archive eq "T") {
				
				my $fileExpiredNews = $sitePath . "xml_files/ExpiredNews.xml";
				
				my $parserExpired = XML::LibXML->new();
				my $documentExpired = $parserExpired->parse_file($fileExpiredNews);
	
				#estraggo la radice del file XML
				my $rootExpired = $documentExpired->getDocumentElement; 
				
				my $id = $activeNews->findvalue('ID');
				my $date = $activeNews->findvalue('Date');
				my $time = $activeNews->findvalue('Time');
				my $text = $activeNews->findvalue('Text');
				my $publisher = $activeNews->findvalue('Publisher');
				my $type = $activeNews->findvalue('Type');
				
				my $newNodeString = " 
<ExpiredNews>
	<ID>$id</ID>
	<Title>$title</Title>
	<Date>$date</Date>
	<Time>$time</Time>
	<Text>$text</Text>
	<Publisher>$publisher</Publisher>
	<Type>$type</Type></ExpiredNews>";
				
				my $newNode = $parserExpired->parse_balanced_chunk($newNodeString);
				
				my $tableExpiredNews = $rootExpired->find("//TableExpiredNews")->get_node(1);
				
				my $firstNode = $tableExpiredNews->findnodes("ExpiredNews[1]")->get_node(1);
				
				$tableExpiredNews->insertBefore($newNode, $firstNode);
				
				open(FILE, ">$fileExpiredNews") || die("Non riesco ad aprire il file");
				print FILE $documentExpired->toString();
				close(FILE);
				
			}
			else {
			    
			    if ($rootRSS->exists("//item[title=\"$title\"]")) {
                    my $newsRSS = $rootRSS->find("//item[title=\"$title\"]")->get_node(1);
                    my $parentRSS = $newsRSS->parentNode;
                    $parentRSS->removeChild($newsRSS);
			    }
			}
			my $parent = $activeNews->parentNode;
			$parent->removeChild($activeNews);
			
			open(FILE, ">$rssfeedFile") || die("Non riesco ad aprire file rssfeed.xml");
			print FILE $documentRSS->toString();
			close(FILE);
			
			open(FILE, ">$fileActiveNews") || die("Non riesco ad aprire il file");
			print FILE $documentActive->toString();
			close(FILE);
			
			
		}
	}



}

1;
