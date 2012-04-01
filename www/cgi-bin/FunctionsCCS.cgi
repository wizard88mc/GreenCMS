#!/usr/bin/perl

use XML::LibXML;
use File::Basename;
use utf8;

#insieme di funzioni per la gestione delle operazioni riguardanti il CCS

$fileXML .= "CCSAttachedFile.xml";

#inserimento di un nuovo CCS nel file XMl
sub insertNewCCS() {
	
	eval {
		#parametri di ingresso: data del CCS, ordine del giorno, nome del file del verbale (es Verbale.pdf)
		my $dateBad = $_[0];
		my $agenda = $_[1];
		my $filename = $_[2];
		
		#$fileXML .= "CCSAttachedFile.xml";
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileXML);
		my $root = $document->getDocumentElement;
		
		#converto la data nel formato corretto XML, quindi aaaa-mm-gg
		my $date = substr($dateBad, 6) . "-" . substr($dateBad, 3, 2) . "-" . substr($dateBad, 0, 2);
		
		my $newID = 0;
		#calcolo ID per il nuovo CCS
		if ($root->exists("//TableCCS/CCS[1]")) {
		    $newID = $root->findvalue("//TableCCS/CCS[1]/ID");
		}
		$newID = $newID + 1;
		
		#creo nodo in formato stringa
		my $newCCS = 
"<CCS>
	<ID>$newID</ID>
	<Date>$date</Date>
	<Agenda>$agenda</Agenda>
	<FileReport>$filename</FileReport>
	<Approved>F</Approved></CCS>";
		
		my $newNode = $parser->parse_balanced_chunk($newCCS);
		my $tableCCS = $root->find("//TableCCS")->get_node(1);
		
		#recupero il primo nodo figlio di TableCCS, perchè voglio inserire il nuovo CCS in testa
		#in modo da poterli visualizzare in ordine decrescente rispetto alla data
		if ($root->exists("//TableCCS/CCS[1]") ) {
			
			my $firstChild = $root->find("//TableCCS/CCS[1]")->get_node(1);
			$tableCCS->insertBefore($newNode, $firstChild);
		}
		else {
			$tableCCS->addChild($newNode);	
		}
		
		open(FILE, ">$fileXML") || die("Non riesco ad aprire il file");
		print FILE $document->toString();
		close(FILE);
		
		return $newID;
		#return 0;
	}
	or do {
		return 0;
	}
}

#inserisce un nuovo allegato ad un determinato CCS
sub insertAttachment() {
	
	eval {
		#parametri di ingresso: testo di presentazione del file, 
		#nome del file con estensione, ID del ccs a cui si vuole associare il file
		my $textFileName = $_[0];  
		my $fileName = $_[1];  
		my $CCSID = $_[2];  
		
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileXML);
		my $root = $document->getDocumentElement;
		
		my $newID = 0;
		#calcolo ID per il nuovo allegato
		if ($root->exists("//AttachedFiles[last()]")) {
			$newID = $root->findvalue("//AttachedFiles[last()]/ID");
		}
		
		$newID = $newID + 1;
		
		#creo nodo formato stringa
		my $newAttachment = 
"<AttachedFile>
	<ID>$newID</ID>
	<FileName>$textFileName</FileName>
	<File>$fileName</File>
	<CCSAssociated>$CCSID</CCSAssociated></AttachedFile>";
		
		my $newNode = $parser->parse_balanced_chunk($newAttachment);
		my $tableAttachments = $root->findnodes("//TableAttachedFiles")->get_node(1);
		$tableAttachments->addChild($newNode);
		
		#recupero data del ccs, per restituire la cartella dove andrà inserito l'allegato
		my $folderCCS = $root->findvalue("//TableCCS/CCS[ID=$CCSID]/Date");
		#elimino i - dalla data
		$folderCCS =~ s/-//g;
		
		open(FILE, ">$fileXML") || die("Non riesco ad aprire il file");
		print FILE $document->toString();
		close(FILE);
		
		return $folderCCS;
	}
	or do {
		return 0;
	}
	
}

#restituisce l'elenco dei CCS da approvare sotto forma di <option> HTML
sub getCCSToApprove() {
	
	eval {
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileXML);
		my $root = $document->getDocumentElement;
		
		#recupero la lista dei CCS non ancora approvati, quindi con Approved=F
		my $listCCS = $root->find("//TableCCS/CCS[Approved=\"F\"]");
		
		my $selectOptionHTML = "";
		
		#per ogni CCS non ancora approvato
		foreach my $ccs ($listCCS->get_nodelist) {
		
			my $ccsID = $ccs->findvalue('ID');
			my $ccsDate = $ccs->findvalue('Date');
			
			#pongo data in formato gg/mm/aaaa
			my $ccsDate = substr($ccsDate, 8, 2) . "/" . substr($ccsDate, 5, 2) . "/" . substr($ccsDate, 0, 4);
			
			#aggiungo <option>, dove value è l'ID del CCS
			$selectOptionHTML .= "<option value=\"$ccsID\">$ccsDate</option>";
		
		}
	
		return $selectOptionHTML;
	}
	
	or do {
		
		return "";
	}
	
	
}

#funzione che rende approvato un CCS
sub approveCCSXML() {
	
	eval {
		#parametro di ingresso: ID del CCS approvato
		my $ccsID = $_[0];
		
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileXML);
		my $root = $document->getDocumentElement;
		
		#recupera nodo corrispondente al CCS
		my $ccs = $root->findnodes("//TableCCS/CCS[ID=$ccsID]")->get_node(1);
		
		#avendo possibilità solamente di sostituire un nodo con un altro nodo, 
		#recupero le informazioni del CCS e le inserisco nel nuovo nodo, che 
		#sostituirà quello vecchio con flag Approved a T
		my $ccsDate = $ccs->findvalue('Date');
		my $ccsAgenda = $ccs->find('Agenda')->get_node(1)->firstChild->toString;
		my $ccsFileReport = $ccs->findvalue('FileReport');
		
		#creo nodo in formato stringa
		my $newCCS = 
"<CCS>
	<ID>$ccsID</ID>
	<Date>$ccsDate</Date>
	<Agenda>$ccsAgenda</Agenda>
	<FileReport>$ccsFileReport</FileReport>
	<Approved>T</Approved></CCS>";
			
		my $newNode = $parser->parse_balanced_chunk($newCCS);
		my $parent = $ccs->parentNode;
		#sostituisco nodo vecchio con nodo nuovo
		$parent->replaceChild($newNode, $ccs);
		
		open(FILE, ">$fileXML") || die("Non riesco ad aprire il file");
		print FILE $document->toString();
		close(FILE);
		
		$ccsDate =~ s/-//g;
		
		#restituisco data in formato aaaammgg per permettere allo script di 
		#completare il lavoro eliminando il file .htaccess dalla cartella
		return $ccsDate;
	}
	or do {
		return "";
	}
	
}


1;
