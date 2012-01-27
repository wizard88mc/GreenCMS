#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use utf8;


#insieme delle funzioni per la gestione dei seminari

$fileEvents = $fileXML . "EventMailingListContact.xml";
$fileContacts = $fileXML . "MailingListsContactsJoins.xml";

#restituisce l'elenco delle mailing list sotto forma di <option> HTML
sub getMailingListOptions() {
	
	eval {
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileContacts);
		my $root = $document->getDocumentElement;
		
		#recupero l'elenco delle mailing list
		my $listMailingList = $root->findnodes('//TableMailingLists/MailingList');
		
		my $selectOptionHTML = "";
		
		#per ogni mailing list presente
		foreach my $mailingList ($listMailingList->get_nodelist) {
		
			my $mailingListID = $mailingList->findvalue('ID');
			my $mailingListName = $mailingList->findvalue('Name');
			
			#creo <option> dove in value inserisco l'ID della mailing list
			$selectOptionHTML .= "<option value=\"$mailingListID\">$mailingListName</option>";
		
		}
	
		return $selectOptionHTML;
	}
	or do { return ""; }
}

#restituisce elenco mailing list da utilizzare per i checkbox
sub getMailingListCheckbox() {
	
	eval {
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileContacts);
		my $root = $document->getDocumentElement;
		
		#recupero l'elenco delle mailing list
		my $listMailingList = $root->findnodes('//TableMailingLists/MailingList');
		
		my $stringHTML = "";
		
		foreach my $mailingList ($listMailingList->get_nodelist) {
			
			my $id = $mailingList->findvalue('ID');
			my $name = $mailingList->findvalue('Name');
			
			$stringHTML .= "<div><label for=\"\_$id\">$name</label><input type=\"checkbox\" name=\"mailingList\" id=\"_$id\" value=\"$id\" /></div><br />";
			
		}
		
		return $stringHTML;
	}
	or do {
		return "Mailing List non caricate. Riprovare";
	}
}

#restituisce l'elenco dei contatti sotto forma di <option> HTML
sub getContactsOptions() {

	eval {
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileContacts);
		my $root = $document->getDocumentElement;
		
		#recupero l'elenco dei contatti inseriti
		my $listContacts = $root->findnodes('//TableContacts/Contact');
		
		my $selectOptionHTML = "";
		
		#per ogni contatto presente
		foreach my $contact ($listContacts->get_nodelist) {
		
			my $contactID = $contact->findvalue('ID');
			my $contactNameSurname = $contact->findvalue('Name') . " " . $contact->findvalue('Surname');
			
			#creo <option> dove in value inserisco l'ID del contatto
			$selectOptionHTML .= "<option value=\"$contactID\">$contactNameSurname</option>";
		
		}
	
		return $selectOptionHTML;
	}
	or do { return ""; }

}

#restituisce l'elenco dei contatti associati ad una mailing list
sub getContactsMailingListOption() {
	
	eval {
	
		#parametro di ingresso: ID della mailing list
		my $mailingList = $_[0];
		
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileContacts);
		my $root = $document->getDocumentElement;
		
		#recupera l'elenco dei contatti associati a quella mailing list
		my $contactsMailing = $root->findnodes("//TableJoinMailingListsContacts/JoinContactMailingList[IDMailingList = $mailingList]");
		
		my $selectOptionHTML = "";
		
		#per ogni contatto associato
		foreach my $association ($contactsMailing->get_nodelist) {
			
			#recupero ID, nome e cognome
			my $contactID = $association->findvalue('IDContact');
			
			my $contactName = $root->findvalue("//TableContacts/Contact[ID = $contactID]/Name");
			my $contactSurname = $root->findvalue("//TableContacts/Contact[ID = $contactID]/Surname");
			
			my $contactNameSurname = $contactName .  " " . $contactSurname;
			
			#creo <option> dove value è l'ID del contatto
			$selectOptionHTML .= "<option value=\"$contactID\">$contactNameSurname</option>";
			
		}
		
		return $selectOptionHTML;
	}
	or do { return ""; }
}

#resituisce l'elenco dei seminari registrati sotto forma di <option> HTML
sub getSeminarOption() {
	
	eval {
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileEvents);
		my $root = $document->getDocumentElement;
		
		#recupero l'elenco dei seminari
		my $events = $root->findnodes("//Event");
		
		my $selectOptionHTML = "";
		
		foreach my $event ($events->get_nodelist) {
			
			#recupero ID, Titolo, Data e Relatore
			my $eventID = $event->findvalue('ID');
			my $eventTitle = $event->findvalue('Title');
			my $eventDate = $event->findvalue('Date');
			my $eventSpeaker = $event->findvalue('Speaker');
			
			#metto data nel formato gg/mm/aaaa
			my $eventDate = substr($eventDate, 8, 2) . "/" . substr($eventDate, 5, 2) . "/" . substr($eventDate, 0, 4);
			
			#creo <option>, dove in value inserisco l'ID del seminario
			$selectOptionHTML .= "<option value=\"$eventID\">$eventDate - $eventTitle - $eventSpeaker</option>";
			
			
		}
		
		
		return $selectOptionHTML;
	}
	or do { return ""; }
	
}

#restituisce il nome di una mailing list
sub getMailingListName() {

	#parametro di ingresso: ID della mailing list
	$mailingListID = $_[0];
	
	my $parser = XML::LibXML->new();
	my $document = $parser->parse_file($fileContacts);
	my $root = $document->getDocumentElement;
	
	#recupero nome della mailing list
	my $mailingList = $root->findvalue("//TableMailingLists/MailingList[ID = $mailingListID]/Name");

	return $mailingList;

}

#inserisce un nuovo seminario nel file XML
sub insertNewSeminary() {

#	eval {
	
		my %details = %{$_[0]};
		
		my $parser = XML::LibXML->new();
		
		my $documentEvents = $parser->parse_file($fileEvents) or die "$!";
		my $rootEvents = $documentEvents->getDocumentElement;
		
		my $documentContacts = $parser->parse_file($fileContacts);
		my $rootContacts = $documentContacts->getDocumentElement;
		
		#crea ID per il nuovo nodo
		my $newID = 0;
		
		if ($rootEvents->exists('Event[1]')) {
			$newID = $rootEvents->findvalue('Event[1]/ID');
		}
		
		$newID = $newID + 1;
		
		if ($details{'lang'} eq "") {
			$details{'lang'} = "it";
		}
		
		my $listMailing = @{$details{'mailingList'}}[0];
		
		my @mailingList = split(' ', $listMailing);
		
		my $mailingListsString = "<MailingListsIDs>";
		
		foreach my $mailing (@mailingList) {
			$mailingListsString .= "<MailingListID>$mailing</MailingListID>";
		}
		$mailingListsString .= "</MailingListsIDs>";
		
		
		my $title = $details{'title'};
		#converte data nel formato XML aaaa-mm-gg
		my $date = substr($details{'date'}, 6) . "-" . substr($details{'date'}, 3, 2) . "-" . substr($details{'date'}, 0, 2);
		#converte orario nel formato XML hh:mm:ss
		my $time = $details{'time'} . ":00";
		my $place = $details{'place'};
		my $speaker = $details{'speaker'};
		my $from = $details{'affiliazione'};
		my $speakerCV = $details{'speakerCV'};
		my $abstract = $details{'abstract'};
		
		if ($from ne "") {
			$from = "<From>$from</From>";
		}
		else {
			$from = "<From/>";
		}
		
		#creo il nodo in formato stringa
		my $newEvent = "
<Event language=\"$details{'lang'}\">
	<ID>$newID</ID>
	<Title>$title</Title>
	<Date>$date</Date>
	<Time>$time</Time>
	<Place>$place</Place>
	<Speaker>$speaker</Speaker>
	$from
	<SpeakerCV>$speakerCV</SpeakerCV>
	<Abstract>$abstract</Abstract>
</Event>";
		
		my $newChild = $parser->parse_balanced_chunk($newEvent);
		
		#recupero primo evento, perchè voglio inserire nuovo evento in testa
		
		if ($rootEvents->exists("Event[1]")) {
			my $firstChild = $rootEvents->findnodes("Event[1]")->get_node(1);
			$rootEvents->insertBefore($newChild, $firstChild);
		}
		else {
		    for my $node ($newChild->childNodes) {
			$rootEvents->addChild($node);
		    }
		}
		
		my $nodeJoin = "
		<JoinEventMailingList>
			<EventID>$newID</EventID>
			$mailingListsString
			<AdditionalsEmails>$details{'additionalMails'}</AdditionalsEmails>
		</JoinEventMailingList>";
		
		my $newNode = $parser->parse_balanced_chunk($nodeJoin);
		
		my $tableJoins = $rootContacts->find("TableJoinEventsMailingLists")->get_node(1);
		for my $node ($newNode->childNodes) {
		    $tableJoins->addChild($node);
		}
		
		open(FILE, ">$fileEvents") || die("Non riesco ad aprire il file");
		print FILE $documentEvents->toString();
		close(FILE);
		
		open(FILE, ">$fileContacts") || die("Non riesco ad aprire $fileContacts");
		print FILE $documentContacts->toString();
		close(FILE);
	
		return $newID;
#	}
#	or do {
#		return 0;
#	}
}

#inserisce nuova mailing list nel file XML
sub insertNewMailingList() {

	eval {
		#parametro di ingresso: nome della mailing list
		my $mailingListName = $_[0];
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileContacts);
		my $root = $document->getDocumentElement;
		
		#verifico se il nome inserito non è già presente, in caso positivo ritorno messaggio errore
		if ($root->exists("//TableMailingLists/MailingList[Name = \"$mailingListName\"]")) {
			return 0;
		}
		else {
			
			#creo ID per nuovo nodo
			my $newID = 0;
			if ($root->exists('//TableMailingLists/MailingList[last()]')) {
				
				$newID = $root->findvalue('//TableMailingLists/MailingList[last()]/ID');
			}
			$newID = $newID + 1;
			
			my $tableMailingList = $root->find('//TableMailingLists')->get_node(1);
			
			#creo nodo formato stringa
			my $newMailingList = "
			<MailingList>
				<ID>$newID</ID>
				<Name>$mailingListName</Name>
			</MailingList>";
			
			my $newChild = $parser->parse_balanced_chunk($newMailingList);
			
			for my $node ($newChild->childNodes) {
			    $tableMailingList->addChild($node);
			}
			
			open(FILE, ">$fileContacts") || die("Non riesco ad aprire il file");
			print FILE $document->toString();
			close(FILE);
			
			return 1;
		}
	}
	or do {
		return 0;	
	}
}

#cancella mailing list da file XML
sub deleteMailingList() {
	
	eval {
		#parametro di ingresso: ID della mailing list
		my $mailingListID = $_[0];
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileContacts);
		my $root = $document->getDocumentElement;
	
		#recupero nodo mailing list e lo cancello
		my $mailingList = $root->find("TableMailingLists/MailingList[ID = $mailingListID]")->get_node(1);
		my $parent = $mailingList->parentNode;
		$parent->removeChild($mailingList);
		
		#elimino tutte le associazioni tra mailing list e contatti
		$mailingList = $root->findnodes("//TableJoinMailingListsContacts/JoinContactMailingList[IDMailingList = $mailingListID]");
		foreach $association ($mailingList->get_nodelist) {
			$parent = $association->parentNode;
			$parent->removeChild($association);
		}
		
		open(FILE, ">$fileContacts") || die("Non riesco ad aprire il file");
		print FILE $document->toString();
		close(FILE);
		
		return 1;
		
	}
	or do { return 0; }
	
}

#elimina contatto da file XMl
sub deleteContact() {
	
	eval {
		#parametro di ingresso: ID del contatto
		my $contactID = $_[0];
		
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileContacts);
		my $root = $document->getDocumentElement;
	
		#recupero nodo e lo cancello dalla tabella dei contatti
		my $contact = $root->find("TableContacts/Contact[ID = $contactID]")->get_node(1);
		my $parent = $contact->parentNode;
		$parent->removeChild($contact);
		
		#recupero le eventuali associazioni contatto - mailing list e le elimino
		$contactMailingList = $root->findnodes("//TableJoinMailingListsContacts/JoinContactMailingList[IDContact = $contactID]");
		foreach $association ($contactMailingList->get_nodelist) {
			$parent = $association->parentNode;
			$parent->removeChild($association);
		}
		
		open(FILE, ">$fileContacts") || die("Non riesco ad aprire il file");
		print FILE $document->toString();
		close(FILE);
	}
	or do { return 0; }

}

#cancella seminario da file XML
sub deleteSeminar() {
	
	eval {
		#parametro di ingresso: ID del seminario
		my $seminarID = $_[0];	
		
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileEvents);
		my $root = $document->getDocumentElement;
		
		my $documentContacts = $parser->parse_file($fileContacts);
		my $rootContacts = $documentContacts->getDocumentElement;
		
		#recupero nodo del seminario e lo elimino
		my $seminar = $root->find("Event[ID=$seminarID]")->get_node(1);
		my $parent = $seminar->parentNode;
		$parent->removeChild($seminar);
		
		my $seminarJoin = $rootContacts->find("TableJoinEventsMailingLists/JoinEventMailingList[EventID=$seminarID]")->get_node(1);
		my $joinParent = $seminarJoin->parentNode;
		$joinParent->removeChild($seminarJoin);
		
		open(FILE, ">$fileEvents") || die("Non riesco ad aprire il file");
		print FILE $document->toString();
		close(FILE);
		
		open(FILE, ">$fileContacts") || die("Non riesco ad aprire il file");
		print FILE $documentContacts->toString();
		close(FILE);
		
		return 1;
	}
	or do {	return 0; }
	
}

#elimina associazione contatto - mailing list
sub deleteAssociation() {
	
	eval {
		#parametri di ingresso: ID del contatto, ID della mailing list
		my $contactID =$_[0];
		my $mailingListID = $_[1];
		
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileContacts);
		my $root = $document->getDocumentElement;
		
		#recupero nodo che rappresenta associazione
		my $association = $root->find("TableJoinMailingListsContacts/JoinContactMailingList[IDMailingList=$mailingListID and IDContact=$contactID]")->get_node(1);
		my $parent = $association->parentNode;
		$parent->removeChild($association);
		
		open(FILE, ">$fileContacts") || die("Non riesco ad aprire il file");
		print FILE $document->toString();
		close(FILE);
		
		return 1;
	}
	or do { return 0; }
	
}

#inserisce nuovo contatto nel file XML
sub insertNewContact() {

	eval {
		#parametri di ingresso: nome contatto, cognome contatto, indirizzo email, ID mailing list associata
		my $name = $_[0];
		my $surname = $_[1];
		my $email = $_[2];
		my $mailingListID = $_[3];
		
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileContacts);
		my $root = $document->getDocumentElement;
		
		#crea ID per nuovo contatto
		my $newID = 0;
		
		if ($root->exists("TableContacts/Contact[last()]")) {
			
			$newID = $root->findvalue("TableContacts/Contact[last()]/ID");
		}
		$newID = $newID + 1;
		
		my $tableContact = $root->find('TableContacts')->get_node(1);
		
		#crea nodo in formato stringa
		my $newContact = "
		<Contact>
			<ID>$newID</ID>
			<Name>$name</Name>
			<Surname>$surname</Surname>
			<Email>$email</Email></Contact>";
		
		my $newChild = $parser->parse_balanced_chunk($newContact);
		for my $node ($newNode->childNodes) {
		    $tableContact->addChild($node);
		}
		
		open(FILE, ">$fileContacts") || die("Non riesco ad aprire il file");
		print FILE $document->toString();
		close(FILE);
		
		return 1;
	}
	or do  { return 0; }

}

#crea associazione contatto - mailing list
sub associateContactMailingList() {

	eval {
		#parametri di ingresso: ID del contatto, ID mailing list
		my $contactID = $_[0];
		my $mailingListID = $_[1];
	
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileContacts);
		my $root = $document->getDocumentElement;
		
		my $tableUserMailingList = ($root->find('TableJoinMailingListsContacts'))->get_node(1);
		
		my $updated = 0;
		
		#verifica che non sia già presente l'associazione
		my $nodePresent = $root->exists("TableJoinMailingListsContacts/JoinContactMailingList[IDMailingList=$mailingListID and IDContact=$contactID]");
		
		#inserisce solo se associazione non ancora presente
		if ($nodePresent == 0) {
			
			#creo nodo formato testo
			my $newAssociation = "
		<JoinContactMailingList>
			<IDMailingList>$mailingListID</IDMailingList>
			<IDContact>$contactID</IDContact></JoinContactMailingList>";
			
			my $newChild = $parser->parse_balanced_chunk($newAssociation);
			for my $node ($newNode->childNodes) {
			    $tableUserMailingList->addChild($node);
			}
			
		}
		
		open(FILE, ">$fileContacts") || die("Non riesco ad aprire il file");
		print FILE $document->toString();
		close(FILE);
	
		#ritorno 0 o 1 per indicare inserimento o meno (1 sì, 0 no)
		return $updated;
	}
	or do {
		return 0;
	}
}

#modifica le informazioni di un contatto
sub modifyContact() {

	eval {
		#parametri di ingresso: ID del contatto, Nome, Cognome, indirizzo email 
		my $contactID = $_[0];
		my $contactName = $_[1];
		my $contactSurname = $_[2];
		my $contactEmail = $_[3];
		
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileContacts);
		my $root = $document->getDocumentElement;
	
		#crea nodo in formato stringa
		my $stringNewNode = "
		<Contact>
			<ID>$contactID</ID>
			<Name>$contactName</Name>
			<Surname>$contactSurname</Surname>
			<Email>$contactEmail</Email></Contact>";
			
		my $newNode = $parser->parse_balanced_chunk($stringNewNode);
		#recupera il vecchio nodo da sostituire di quel contatto
		my $oldNode = $root->find("TableContacts/Contact[ID=$contactID]")->get_node(1);
		my $parent = $oldNode->parentNode;
		
		#sostituisce i due nodi
		$parent->replaceChild($newNode, $oldNode);
	
		open(FILE, ">$fileContacts") || die("Non riesco ad aprire il file");
		print FILE $document->toString();
		close(FILE);
		
		return 1;
	}
	or do  { return 0; }
}

#restituisce le informazioni di un contatto (Nome, Cognome, Indirizzo email sotto forma di HASH
sub getContactInformations() {

	#parametri di ingresso: ID del contatto
	my $contactID = $_[0];
	
	my $parser = XML::LibXML->new();
	
	my $document = $parser->parse_file($fileContacts);
	my $root = $document->getDocumentElement;

	#recupera nodo del contatto
	my $contactInformations = $root->find("TableContacts/Contact[ID=$contactID]")->get_node(1);
	
	#recupera informazioni e le inserisce in un HASH
	my $name = $contactInformations->findvalue('Name');
	my $surname = $contactInformations->findvalue('Surname');
	my $email = $contactInformations->findvalue('Email');
	
	return ("name" => "$name", "surname" => "$surname", "email" => "$email");

}

1;
