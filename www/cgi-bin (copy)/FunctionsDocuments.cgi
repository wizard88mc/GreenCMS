#!/usr/bin/perl

use XML::LibXML;
use File::Basename;
use utf8;

#file contenente tutte le funzioni necessarie alla gestione dei documenti

$fileXML .= "Document.xml";

#funzione che registra un nuovo documento all'interno del file xml
sub insertDocument() {
	
	eval {
		#primo parametro di input il nome del file (es pippo.pdf), 
		#il secondo il nome del file da visualizzare (es Documento stage interno)
		my $filename = $_[0];
		my $textFile = $_[1];
	
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileXML);
		my $root = $document->getDocumentElement;
		
		#recupero un nuovo ID per il documento
		my $newID = 0;
		if ($root->exists("//Document[last()]")) {
			$newID = $root->findvalue("//Document[last()]/ID");
		}
		
		$newID = $newID + 1;
		
		my $newDocument = 
"<Document>
	<ID>$newID</ID>
	<Name>$textFile</Name>
	<FileName>$filename</FileName></Document>";
		
		my $newNode = $parser->parse_balanced_chunk($newDocument);
		#recupero tabella dei documenti
		my $tableDocument = $root->findnodes("//TableDocument")->get_node(1);
		$tableDocument->addChild($newNode);
		
		open(FILE, ">$fileXML") || die("Non riesco ad aprire il file");
		print FILE $document->toString();
		close(FILE);
		
		return 1;
	}
	or do { return 0; }
}

#restituisce l'elenco dei documenti sotto forma di <option> HTML per la visualizzazione all'interno di form
sub getDocumentsOptions() {
	
	eval {
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileXML);
		my $root = $document->getDocumentElement;
		
		my $listDocuments = $root->findnodes("//TableDocument/Document");
		
		my $selectOptionHTML = "";
		
		#aggiungo ogni documento, valore identificativo in value l'ID del documento
		foreach my $document ($listDocuments->get_nodelist) {
		
			my $documentID = $document->findvalue('ID');
			my $documentName = $document->findvalue('Name');
			
			$selectOptionHTML .= "<option value=\"$documentID\">$documentName</option>";
		
		}
	
		return $selectOptionHTML;
	}
	or do { return ""; }
	
}


#funzione per la cancellazione di un documento dal file XML
sub cancelDocument() {
	
	eval {
		my $documentID = $_[0];	
		
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileXML);
		my $root = $document->getDocumentElement;
		
		#prendo il nodo che corrisponde al documento da eliminare
		my $nodeDelete = $root->find("//Document[ID=$documentID]")->get_node(1);
		
		#salvo il nome del file che devo cancellare, da restituire per successiva cancellazione nello script
		my $filename = $nodeDelete->findvalue('FileName');
		
		#recupero il padre del nodo
		my $parent = $nodeDelete->parentNode;
		
		#rimuovo nodo
		$parent->removeChild($nodeDelete);
		
		open(FILE, ">$fileXML") || die("Non riesco ad aprire il file");
		print FILE $document->toString();
		close(FILE);
		
		#ritorno nome del file da cancellare
		return $filename;
	}
}
