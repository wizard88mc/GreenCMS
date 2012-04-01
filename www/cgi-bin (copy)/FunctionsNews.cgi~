#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use utf8;
use Time::localtime;
use Date::Calc qw(Add_Delta_Days Delta_Days);

require "GlobalFunctions.cgi";

#insieme di funzioni per la gestione delle news e del feedRSS

$feedRSS = $fileXML . "rssfeed.xml";
$fileXML .= "ActiveNews.xml";

#restituisce l'insieme delle news sotto forma di <option> HTML
sub getNewsListOptions() {
	
	eval {
	
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileXML);
		my $root = $document->getDocumentElement;
		my $selectOptionHTML = "";
		
		#recupera l'insieme delle news
		my $activeNews = $root->findnodes("//ActiveNews");
		
		#per ogni news attiva
		foreach my $news ($activeNews->get_nodelist) {
			
			#recupera informazioni
			my $newsID = $news->findvalue('ID');
			my $newsTitle = $news->findvalue('Title');
			my $newsDate = $news->findvalue('Date');
			#trasforma data in formato gg/mm/aaaa
			$newsDate = &convertDateFromDBToItalian($newsDate);
			my $newsPublisher = $news->findvalue('Publisher');
			
			#crea <option> mettendo in value l'ID della news
			$selectOptionHTML .= "<option value=\"$newsID\">$newsDate - $newsTitle - $newsPublisher</option>";
			
		}
		
		return $selectOptionHTML;
	}
	or do {
		return "";
	}
	
}

#inserisce una nuova news all'interno del file XML
sub insertNews() {
	
	eval {
		#parametri di ingresso: HASH contenente le informazioni della nuova news
		my %details = %{$_[0]};
		
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileXML);
		my $root = $document->getDocumentElement;
		
		#recupero anno, mese e giorno attuali
		my ($currentYear, $currentMonth, $currentDay) = &getCurrentDate();
		
		#creo data attuale in formato corretto per il confronto con quella inserita
		my $currentDate = "$currentYear-$currentMonth-$currentDay";
		
		#modifico data di validità e di scadenza nel formato aaaa-mm-gg
		$details{'validFrom'} = &convertDateFromItalianToDB($details{'validFrom'});
		$details{'expirationDay'} = &convertDateFromItalianToDB($details{'expirationDay'});
		
		if ($details{'validFrom'} eq $currentDate) {
		     #news valida a partire dal giorno attuale
		     #orario di inizio validità quello di inserimento della news
		     my $hour = localtime->hour();
		     if (length($hour) == 1) {
		         $hour = "0$hour";
		     }
		     my $minutes = localtime->min();
		     if (length($minutes) == 1) {
		         $minutes = "0$minutes";
		     }
		     $details{'time'} = "$hour:$minutes:00";
		}
		else {
		     #mostro una news posticipata nel tempo a partire 
		     #dalle 00:00 del giorno corretto
		     $details{'time'} = "00:00:00";
		}
		
		#recupero tabella news attive
		my $tableActiveNews = $root->find('//TableActiveNews')->get_node(1);
		
		#creo ID per il nuovo nodo
		my $newID = $tableActiveNews->findvalue('@IDLastNews');
		$newID = $newID + 1;
		
		#nuovo nodo in formato testo
		my $newNews = 
"<ActiveNews>
	<ID>$newID</ID>
	<Title>$details{'title'}</Title>
	<Date>$details{'validFrom'}</Date>
	<Time>$details{'time'}</Time>
	<Text>$details{'textNews'}</Text>
	<Publisher>$details{'author'}</Publisher>
	<Type>$details{'type'}</Type>
	<Archive>$details{'archive'}</Archive>
	<ExpirationDate>$details{'expirationDay'}</ExpirationDate></ActiveNews>";
		
		my $newNode = $parser->parse_balanced_chunk($newNews);
		#recupero primo nodo per inserire nuova news in testa
		my $firstChild = $root->find("//TableActiveNews/ActiveNews[1]")->get_node(1);
		$tableActiveNews->insertBefore($newNode, $firstChild);
		
		my $IDnode = $tableActiveNews->getAttributeNode('IDLastNews');
		$IDnode->setValue($newID);
		
		open(FILE, ">$fileXML") || die("Non riesco ad aprire il file");
		print FILE $document->toString();
		close(FILE);
		
		# Solo se la news è valida a partire dal giorno attuale
		# la inserisco all'interno del file rssfeed, altrimenti ci penserà
		# il cron al momento opportuno
		
		if (&checkDatesCronologicallyCorrect(
		    &convertDateFromDBToItalian($details{'validFrom'}), &convertDateFromDBToItalian($currentDate)) eq true) {
            $document = $parser->parse_file($feedRSS);
            $root = $document->getDocumentElement;
            
            #creo link alla lettura della news tramite l'ID della nuova news
            my $link = "http://$address/cgi-bin/ReadNews.cgi?newsID=$newID";
            #come descrizione prendo i primi 50 caratteri della news
            my $description = substr(removeLinkTags($details{'textNews'}), 0, 50) . ". . .";
            
            #creo nuovo nodo in formato stringa
            my $itemString =
"<item>
	<title>$details{'title'}</title>
	<link>$link</link>
	<description>$description</description>
	<guid>$link</guid></item>";
		
            my $newItemNode = $parser->parse_balanced_chunk($itemString);
            #recupero radice documento (tag <channel>)
            my $rootChannel = $root->find("//channel")->get_node(1);
            
            #recupero il primo elemento della lista, così metto nuova news in testa
            if ($rootChannel->exists("//item[1]")) {
                my $firstItem = $rootChannel->find("//item[1]")->get_node(1);
            
                $rootChannel->insertBefore($newItemNode, $firstItem);
            }
            else {
                for my $nodeToAdd($newItemNode->childNodes) {
                    $rootChannel->addChild($nodeToAdd);
                }
            }
            
            open(FILE, ">$feedRSS") || die("Non riesco ad aprire il file");
            print FILE $document->toString();
            close(FILE);
		}
		
		return 1;
	}
	or do { return 0; }
	
}

#elimina news da file XML
sub deleteNews() {
	
	#eval {
		#parametro di ingresso: ID della news
		$newsID	= $_[0];
		
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileXML);
		my $root = $document->getDocumentElement;
		
		#recupero nodo news da eliminare e rimuovo
		my $newsNode = $root->find("//TableActiveNews/ActiveNews[ID=$newsID]")->get_node(1);
		
		my $newsTitle = $newsNode->findvalue('Title');
		my $newsActivationDate = $newsNode->findvalue('Date');
		
		my $parent = $newsNode->parentNode;
		$parent->removeChild($newsNode);
		
		open(FILE, ">$fileXML") || die("Non riesco ad aprire il file");
		print FILE $document->toString();
		close(FILE);
		
		my ($currentYear, $currentMonth, $currentDay) = &getCurrentDate();
		my $currentDate = "$currentDay-$currentMonth-$currentYear";
		
		if (&checkDatesCronologicallyCorrect(
		    &convertDateFromDBToItalian($newsActivationDate), $currentDate) eq true) {
		
            my $documentRSS = $parser->parse_file($feedRSS);
            my $rootRSS = $documentRSS->getDocumentElement;
            
            my $feedNode = $rootRSS->find("//item[title=\"$newsTitle\"]")->get_node(1);
            
            my $parent = $feedNode->parentNode;
            $parent->removeChild($feedNode);
            
            open(FILE, ">$feedRSS") || die("Non riesco ad aprire il file");
            print FILE $documentRSS->toString();
            close(FILE);
		    }
		
		return 1;
	#}
	#or do { return 0; }
	
}

#restituisce i dettagli di una news
sub getNewsDetails() {
	
	#parametri di ingresso: ID della news
	my $newsID = $_[0];	
	
	my $parser = XML::LibXML->new();
	
	my $document = $parser->parse_file($fileXML);
	my $root = $document->getDocumentElement;
	
	#recupero nodo della news
	my $newsNode = $root->find("//ActiveNews[ID=$newsID]")->get_node(1);

	#recupero informazioni e le inserisco nell'HASH input
	my %details;
	
	$details{'title'} = $newsNode->findvalue('Title');
	$details{'textNews'} = $newsNode->findvalue('Text');
	$details{'publisher'} = $newsNode->findvalue('Publisher');
	$details{'validFrom'} = &convertDateFromDBToItalian($newsNode->findvalue('Date'));
	$details{'expiration'} = &convertDateFromDBToItalian($newsNode->findvalue('ExpirationDate'));
	$details{'type'} = $newsNode->findvalue('Type');
	$details{'archive'} = $newsNode->findvalue('Archive');
	
	#ritorno HASH
	return %details;
}

#modifica le informazioni di una determinata news
sub editNews() {
	
	eval {
		#parametri di ingresso: HASH contenente le infromazioni della news
		my %details = %{$_[0]};
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileXML);
		my $root = $document->getDocumentElement;
		
		#recuper vecchio nodo della news da sostituire
		my $oldNode = $root->find("//ActiveNews[ID=$details{'idEditNews'}]")->get_node(1);
		my $oldTitle = $oldNode->findvalue('Title');
		my $oldText = $oldNode->findvalue('Text');
		my $oldDate = $oldNode->findvalue('Date');
		
		#recupero data, ora e scadenza (che non possono essere modificate)
		$details{'validFrom'} = &convertDateFromItalianToDB($details{'validFrom'});
		$details{'expirationDay'} = &convertDateFromItalianToDB($details{'expirationDay'});
		
		my ($currentYear, $currentMonth, $currentDay) = &getCurrentDate();
		
		my $today = "$currentYear-$currentMonth-$currentDay";
		my $newsTime = $oldNode->findvalue('Time');
		
		if ($today ne $details{'validFrom'}) {
		    $newsTime = "00:00:00";
		}
		
		#creo nuovo nodo formato stringa
		my $newsNode =
"<ActiveNews>
	<ID>$details{'idEditNews'}</ID>
	<Title>$details{'title'}</Title>
	<Date>$details{'validFrom'}</Date>
	<Time>$newsTime</Time>
	<Text>$details{'textNews'}</Text>
	<Publisher>$details{'publisher'}</Publisher>
	<Type>$details{'type'}</Type>
	<Archive>$details{'archive'}</Archive>
	<ExpirationDate>$details{'expirationDay'}</ExpirationDate></ActiveNews>";
		
		my $newNode = $parser->parse_balanced_chunk($newsNode);
		
		$parent = $oldNode->parentNode;
		$parent->replaceChild($newNode, $oldNode);
		
		open(FILE, ">$fileXML") || die("Non riesco ad aprire il file");
		print FILE $document->toString();
		close(FILE);
		
		my ($newsDay, $newsMonth, $newsYear) = getDateComponentsFromDBDate($details{'validFrom'});
		my ($oldDay, $oldMonth, $oldYear) = getDateComponentsFromDBDate($oldDate);
		
		# Se il nuovo giorno di validità è maggiore rispetto a quello attuale 
		# elimino la news dall'rssfeed
		if (Delta_Days($currentYear, $currentMonth, $currentDay, 
		    $newsYear, $newsMonth, $newsDay) > 0 and
		    Delta_Days($oldYear, $oldMonth, $oldDay, 
		        $currentYear, $currentMonth, $currentDay) > 0) {
		    
		    $document = $parser->parse_file($feedRSS);
            $root = $document->getDocumentElement;
            
            $nodeNews = $root->find("//item[title=\"$oldTitle\"]")->get_node(1);
            
            $parentNodeNews = $nodeNews->parentNode;
            $parentNodeNews->removeChild($nodeNews);
            
            open(FILE, ">$feedRSS") || die("Non riesco ad aprire il file");
            print FILE $document->toString();
            close(FILE);
		}
		# Se non ho cancellato la news, se il titolo o il testo sono cambiati 
		# aggiorno anche nell'rssfeed
		else {
		    
		    # Se la nuova data è minore di quella di oggi e quella vecchia della 
		    # news è maggiore di quella di oggi devo aggiungere news nell'rssfeed 
		    # perchè vuol dire che prima non c'era
		    if (Delta_Days($newsYear, $newsMonth, $newsDay, 
		            $currentYear, $currentMonth, $currentDay) >= 0 and 
		         Delta_Days($currentYear, $currentMonth, $currentDay, 
		             $oldYear, $oldMonth, $oldDay) > 0) {
		    
		        $document = $parser->parse_file($feedRSS);
                $root = $document->getDocumentElement;
                
                $oldNode = $root->find("//item[title=\"$details{'title'}\"]")->get_node(1);
		        
		        #creo link alla lettura della news tramite l'ID della nuova news
		        my $link = "http://$address/cgi-bin/ReadNews.cgi?newsID=$details{'idEditNews'}";
		        #come descrizione prendo i primi 50 caratteri della news
                my $description = substr(removeLinkTags($details{'textNews'}), 0, 50) . ". . .";
		        
		        my $newNodeString =
"<item>
    <title>$details{'title'}</title>
    <link>$link</link>
    <description>$description</description>
    <guid>$link</guid></item>";
    
                my $newNode = $parser->parse_balanced_chunk($newNodeString);
                
                #recupero radice documento (tag <channel>)
                my $rootChannel = $root->find("//channel")->get_node(1);
                
                #recupero il primo elemento della lista, così metto nuova news in testa
                if ($rootChannel->exists("//item[1]")) {
                    my $firstItem = $rootChannel->find("//item[1]")->get_node(1);
                
                    $rootChannel->insertBefore($newNode, $firstItem);
                }
                else {
                    for my $nodeToAdd($newNode->childNodes) {
                        $rootChannel->addChild($nodeToAdd);
                    }
                }
                
                open(FILE, ">$feedRSS") || die("Non riesco ad aprire il file");
                print FILE $document->toString();
                close(FILE);
		             }
		             
		    else {
		    if ($details{'title'} ne $oldTitle or 
		        $details{'textNews'} ne $oldText
		        ) {
		    
                $document = $parser->parse_file($feedRSS);
                $root = $document->getDocumentElement;
                
                $oldNode = $root->find("//item[title=\"$oldTitle\"]")->get_node(1);
		        
		        #creo link alla lettura della news tramite l'ID della nuova news
		        my $link = "http://$address/cgi-bin/ReadNews.cgi?newsID=$details{'idEditNews'}";
		        #come descrizione prendo i primi 50 caratteri della news
                my $description = substr(removeLinkTags($details{'textNews'}), 0, 50) . ". . .";
		        
		        my $newNodeString =
"<item>
    <title>$details{'title'}</title>
    <link>$link</link>
    <description>$description</description>
    <guid>$link</guid></item>";
    
                my $newNodeSubstitute = $parser->parse_balanced_chunk($newNodeString);
                
                my $parentNode = $oldNode->parentNode;
                $parentNode->replaceChild($newNodeSubstitute, $oldNode);
		    
                open(FILE, ">$feedRSS") || die("Non riesco ad aprire il file");
                print FILE $document->toString();
                close(FILE);
                }
            }
		}
		
		return 1;
	}
	or do { return 0; }
	
}

