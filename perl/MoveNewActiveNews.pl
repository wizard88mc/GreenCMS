#!/usr/bin/perl

use XML::LibXML;
use Date::Calc qw(Today Delta_Days);
use Time::localtime;

#questa funzione inserire una news diventata attiva all'interno del file rss feed
sub moveNewActiveNews() {
    
    $fileActiveNews = $sitePath . "xml_files/ActiveNews.xml";
    $fileRSSFeed = $sitePath . "xml_files/rssfeed.xml";
    
    my $parser = XML::LibXML->new();
    my $documentActive = $parser->parse_file($fileActiveNews);
    my $documentRSS = $parser->parse_file($fileRSSFeed);
    
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
	        
	    my $activationDate = $activeNews->findvalue('Date');
	    
	    my ($activationDay, $activationMonth, $activationYear) = 
	                                &getDateComponentsFromDBDate($activationDate);
	    
	    my $deltaDays = Delta_Days($actualYear, $actualMonth, $actualDay, 
	                                $activationYear, $activationMonth, $activationDay);
	    
	    #la news da oggi inizia ad essere attiva, inserisco nuovo nodo rss feed
	    if ($deltaDays == 0) {
	        
	        my $newsTitle = $activeNews->findvalue('Title');
	        my $newsID = $activeNews->findvalue('ID');
	        my $newsText = $activeNews->findvalue('Text');
	        
	        #creo link alla lettura della news tramite l'ID della nuova news
            my $link = "http://$address/cgi-bin/ReadNews.cgi?newsID=$newsID";
            #come descrizione prendo i primi 50 caratteri della news
            $newsText = substr($newsText, 0, 50) . ". . .";
            
            #creo nuovo nodo in formato stringa
            my $itemString = 
"<item>
	<title>$newsTitle</title>
	<link>$link</link>
	<description>$newsText</description>
	<guid>$link</guid></item>";
		
            my $newItemNode = $parser->parse_balanced_chunk($itemString);
            #recupero radice documento (tag <channel>)
            my $rootChannel = $rootRSS->find("//channel")->get_node(1);
            
            #recupero il primo elemento della lista, così metto nuova news in testa
            if ($rootChannel->exists("//item[1]")) {
                my $firstItem = $rootChannel->find("//item[1]")->get_node(1);
            
                $rootChannel->insertBefore($newItemNode, $firstItem);
            }
            else {
                $rootChannel->addChild($newItemNode);
            }
            
            open(FILE, ">$fileRSSFeed") || die("Non riesco ad aprire il file");
            print FILE $documentRSS->toString();
            close(FILE);
        }
	        
    }
	    
}
	
1;
