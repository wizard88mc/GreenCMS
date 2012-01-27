#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use utf8;
use Time::localtime;
use Date::Calc qw(Add_Delta_Days);

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
		my $actualYear = localtime->year() + 1900;
		my $actualMonth = localtime->mon() + 1;
		my $actualDay = localtime->mday();
		
		#se il mese restituito è a una cifra, ci aggiungo in testa lo 0 permetterlo nel formato XML corretto
		if (length($actualMonth) == 1) {
			$actualMonth = "0$actualMonth";	
		}
		if (length($actualDay) == 1) {
			$actualDay = "0$actualDay";	
		}
		
		#creo data attuale in formato corretto per il confronto con quella inserita
		$actualDate = "$actualYear-$actualMonth-$actualDay";
		
		#modifico data di validità e di scadenza nel formato aaaa-mm-gg
		$details{'validFrom'} = &convertDateFromItalianToDB($details{'validFrom'});
		$details{'expirationDay'} = &convertDateFromItalianToDB($details{'expirationDay'});
		
		if ($details{'validFrom'} eq $actualDate) {
		     #come orario della news metto quello attuale
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
		     #mostro una news posticipata nel tempo a partire dalle 08:00
		     $details{'time'} = "08:00:00";
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
		
		if ($details{'validFrom'} == $actualDate) {
		#lavoro su file rssfeed
		$document = $parser->parse_file($feedRSS);
		$root = $document->getDocumentElement;
		
		#creo link alla lettura della news tramite l'ID della nuova news
		my $link = "http://$address/cgi-bin/ReadNews.cgi?newsID=$newID";
		#come descrizione prendo i primi 50 caratteri della news
		my $description = substr($details{'textNews'}, 0, 50) . ". . .";
		
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
			$rootChannel->addChild($newItemNode);
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
	
	eval {
		#parametro di ingresso: ID della news
		$newsID	= $_[0];
		
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileXML);
		my $root = $document->getDocumentElement;
		
		#recupero nodo news da eliminare e rimuovo
		my $newsNode = $root->find("//TableActiveNews/ActiveNews[ID=$newsID]")->get_node(1);
		
		my $newsTitle = $newsNode->findvalue('Title');
		
		my $parent = $newsNode->parentNode;
		$parent->removeChild($newsNode);
		
		open(FILE, ">$fileXML") || die("Non riesco ad aprire il file");
		print FILE $document->toString();
		close(FILE);
		
		$document = $parser->parse_file($feedRSS);
		$root = $document->getDocumentElement;
		
		my $feedNode = $root->find("//item[title=\"$newsTitle\"]")->get_node(1);
		
		$parent = $feedNode->parentNode;
		$parent->removeChild($feedNode);
		
		open(FILE, ">$feedRSS") || die("Non riesco ad aprire il file");
		print FILE $document->toString();
		close(FILE);
		
		return 1;
	}
	or do { return 0; }
	
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
		
		#recupero data, ora e scadenza (che non possono essere modificate)
		$details{'validFrom'} = &convertDateFromItalianToDB($details{'validFrom'});
		$details{'expirationDay'} = &convertDateFromItalianToDB($details{'expirationDay'});
		
		my $actualYear = localtime->year() + 1900;
		my $actualMonth = localtime->mon() + 1;
		my $actualDay = localtime->mday();
		
		#se il mese restituito è a una cifra, ci aggiungo in testa lo 0 permetterlo nel formato XML corretto
		if (length($actualMonth) == 1) {
			$actualMonth = "0$actualMonth";	
		}
		if (length($actualDay) == 1) {
			$actualDay = "0$actualDay";	
		}
		
		my $today = "$actualYear - $actualMonth - $actualDay";
		my $newsTime = $oldNode->findvalue('Time');
		
		if ($today != $details{'validFrom'}) {
		    $newsTime = "08:00:00";
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
		
		return 1;
	}
	or do { return 0; }
	
}

