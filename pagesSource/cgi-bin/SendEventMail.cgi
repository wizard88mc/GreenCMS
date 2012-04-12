#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use utf8;

require "SendMail.cgi";

sub sendEventMail() {
	
	my $signature = "
----------------------------------------------------	
Seminari di Informatica a Padova
http://$address/cgi-bin/Seminari.cgi";
	
	my $eventID = $_[0];
	
	my $parser = XML::LibXML->new();
	
	my $documentEvents = $parser->parse_file($fileEvents);
	my $rootEvents = $documentEvents->getDocumentElement;
	
	my $event = $rootEvents->find("Event[ID = $eventID]")->get_node(1);
	
	#estraggo informazioni dels eminario
	my $eventTitle = $event->find('Title')->get_node(1)->firstChild->toString;
	my $eventDate = $event->findvalue('Date');
	$eventDate = &convertDateFromDBToItalianFormat($eventDate);
	my $eventPlace = $event->find('Place')->get_node(1)->firstChild->toString;
	my $eventTime = $event->findvalue('Time');
	$eventTime = substr($eventTime, 0, 5);
	$eventSpeaker = $event->find('Speaker')->get_node(1)->firstChild->toString;
	
	my $speakerFrom = "";
	if ($event->findvalue('From') ne "") {
	    $speakerFrom = $event->find('From')->get_node(1)->firstChild->toString;
	}
	
	my $eventAbstract = $event->findvalue('Abstract');
	$eventAbstract = &removeLinkTags($eventAbstract);
	
	#costruisco il tempo del messaggio componendolo delle informazioni sul seminario
	my $eventStringMail = <<CONTENT;
=================================================
               AVVISO DI SEMINARIO
=================================================

Data: $eventDate

Ora: $eventTime

Luogo: $eventPlace

Relatore: $eventSpeaker $speakerFrom

Titolo: $eventTitle

Abstract: 
$eventAbstract 

$signature
CONTENT

	utf8::encode($eventStringMail);
	
	my %messageDetails;
	
	$messageDetails{'message'} = $eventStringMail;
	$messageDetails{'email'} = 'seminari_informatica@math.unipd.it';
	$messageDetails{'subject'} = "Avviso Nuovo Seminario: $eventDate [ $eventSpeaker ]"; 
	
	my $count = 0;
	
	my $documentJoins = $parser->parse_file($fileContacts);
	my $rootJoins = $documentJoins->getDocumentElement;

	#estraggo mailing list
	my $eventMailingLists = $rootJoins->find("TableJoinEventsMailingLists/JoinEventMailingList[EventID=$eventID]/MailingListsIDs/MailingListID");
	
	foreach my $eventMailingList ($eventMailingLists->get_nodelist) {
		
		my $eventMailingListID = $eventMailingList->findvalue('.');
	
		#prendo i contatti
		my $usersMailing = $rootJoins->find("TableJoinMailingListsContacts/JoinContactMailingList[IDMailingList=$eventMailingListID]");
		
		#per ogni utente registrato a quella mailing list
		foreach my $userMailing ($usersMailing->get_nodelist) {
			
			#recupero l'ID dell'utente
			my $contactID = $userMailing->findvalue('IDContact');
			
			#recupero l'email del contatto
			my $contactEmail = $rootJoins->findvalue("TableContacts/Contact[ID=$contactID]/Email");
			
			$messageDetails{'emailTo'} = $contactEmail;
			
			#invio email
			my $result = &sendMail(\%messageDetails);
			if ($result eq "") {
				$count = $count + 1;
			}
		}
    }
    
    my $listAdditionalEmail = $rootJoins->findvalue("//TableJoinEventsMailingLists/JoinEventMailingList[EventID=$eventID]/AdditionalsEmails");
    
    if (length($listAdditionalEmail) != 0) {
    	
    	my @mails = split(',', $listAdditionalEmail);
    	
    	foreach my $mail (@mails) {
    		
    		$messageDetails{'emailTo'} = $mail;
    		my $result = &sendMail(\%messageDetails);
    		
    		if ($result eq "") {
				$count = $count + 1;
			}
    	}
    }
    return $count;
}

1;

