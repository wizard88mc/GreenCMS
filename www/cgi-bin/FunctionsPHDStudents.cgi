#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use utf8;

#insieme di funzioni per la gestione dei Dottorandi

$fileXMLPHD = $fileXML . "PHDStudentSupervisor.xml";
$fileForRecovery = $sourcePath . 'pagesSource/xml_files/PHDStudentSupervisor.xml';

#resistuisce elenco supervisori sotto forma di lista <option> HTML
sub getSupervisorList() {
	
	eval {
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileXMLPHD);
		my $root = $document->getDocumentElement;
		my $selectOptionHTML = "";
		
		#recupero elenco supervisori
		my $supervisorList = $root->findnodes("//TableSupervisor/Supervisor");
		
		foreach my $supervisor ($supervisorList->get_nodelist) {
			
			#recupero informazioni
			my $supervisorID = $supervisor->findvalue('ID');
			my $name = $supervisor->findvalue('Name');
			my $surname = $supervisor->findvalue('Surname');
	
			#creo <option> mettendo in value l'ID del supervisore
			$selectOptionHTML .= "<option value=\"$supervisorID\">$name $surname</option>";
			
		}
		
		return $selectOptionHTML;
	}
	or do { return ""; }
	
}

#restituisce elenco cicli sotto forma di <option> HTML
sub getCyclesList() {
	
	eval {
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileXMLPHD);
		my $root = $document->getDocumentElement;
		my $selectOptionHTML = "";
		
		#recupero elenco cicli
		my $cyclesList = $root->findnodes("//TableCycle/Cycle");
		
		foreach my $cycle ($cyclesList->get_nodelist) {
			
			#recupero informazioni
			my $cycleID = $cycle->findvalue('ID');
			my $name = $cycle->findvalue('Name');
			my $begin = $cycle->findvalue('BeginningYear');
			my $end = $cycle->findvalue('EndYear');
	
			#creo <option> mettendo in value l'ID del ciclo
			$selectOptionHTML .= "<option value=\"$cycleID\">$name ($begin - $end)</option>";
			
		}
		
		return $selectOptionHTML;
	}
	or do { return ""; }
	
}

#restituisce l'elenco dei dottorandi sotto forma di <option> HTML
sub getPHDList() {
	
	eval {
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileXMLPHD);
		my $root = $document->getDocumentElement;
		my $selectOptionHTML = "";
		
		#recupera elenco dottorandi
		my $phdList = $root->findnodes("//TablePHDStudent/PHDStudent");
		
		foreach my $phdStudent ($phdList->get_nodelist) {
			
			#recupera informazioni
			my $phdID = $phdStudent->findvalue('ID');
			my $name = $phdStudent->findvalue('Name');
			my $surname = $phdStudent->findvalue('Surname');
	
			#creo <option> mettendo in value l'ID del dottorando
			$selectOptionHTML .= "<option value=\"$phdID\">$name $surname</option>";
			
		}
		
		return $selectOptionHTML;
	}
	or do { return ""; }
	
}

#resituisce il nome e cognome del supervisore
sub getSupervisorName() {
	
	#parametro di ingresso: ID del supervisore
	my $supervisorID = $_[0];
	
	#controllo che ID non sia nullo
	if ($supervisorID ne "") {

		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileXMLPHD);
		my $root = $document->getDocumentElement;
		
		#recupero informazioni e restituisco nome e cognome
		my $supervisorName = $root->findvalue("//TableSupervisor/Supervisor[ID=$supervisorID]/Name");
		my $supervisorSurname = $root->findvalue("//TableSupervisor/Supervisor[ID=$supervisorID]/Surname");
		$supervisorName .= " $supervisorSurname";
		
		return $supervisorName;
	}
	else {
		#ID nullo, al momento dell'inserimento di un dottorando non è stato specificato alcun sueprvisore
		return "";
	}
	
}

#restituisce nome ciclo
sub getCycle() {
	
	#parametro di ingresso: ID del ciclo
	my $cycleID = $_[0];	
	
	#se ID ciclo non è nullo
	if ($cycleID ne "") {
		
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileXMLPHD);
		my $root = $document->getDocumentElement;
		
		#recupero nodo ciclo
		my $cycleNode = $root->find("//TableCycle/Cycle[ID=$cycleID]")->get_node(1);
		
		#recupero informazioni
		my $cycleName = $cycleNode->findvalue("Name");
		my $cycleBegin = $cycleNode->findvalue("BeginningYear");
		my $cycleEnd = $cycleNode->findvalue("EndYear");
		
		my $string = "$cycleName ($cycleBegin - $cycleEnd)";
		
		return $string;
	}
	else {
		#ID ciclo nullo, quando al momento di inserire un nuovo dottorando non viene specificato alcun ciclo
		return "";
	}

}

#restituisce informazioni riguardo un dottorando
sub getUserDetails() {
	
	#parametro di ingresso: ID del dottorando
	my $studentID = $_[0];	
	my $parser = XML::LibXML->new();
		
	my $document = $parser->parse_file($fileXMLPHD);
	my $root = $document->getDocumentElement;
	
	#recupero nodo dottorando
	my $studentNode = $root->find("//TablePHDStudent/PHDStudent[ID=$studentID]")->get_node(1);
	
	#HASH contenente le informazioni del dottorando
	my %userDetails;
	
	$userDetails{'name'} = $studentNode->findvalue('Name');
	$userDetails{'surname'} = $studentNode->findvalue('Surname');
	$userDetails{'researchArea'} = $studentNode->findvalue('ResearchArea');
	$userDetails{'website'} = $studentNode->findvalue('Website');
	$userDetails{'supervisor'} = $studentNode->findvalue('Supervisor');
	$userDetails{'cycle'} = $studentNode->findvalue('Cycle');
	$userDetails{'lang'} = $studentNode->findvalue('ResearchArea/@language');
	
	#restituisco HASH
	return %userDetails;
	
}

sub getCycleDetails() {

	#parametro: ID del ciclo
	my $cycleID = $_[0];
	my $parser = XML::LibXML->new();
	
	my $document = $parser->parse_file($fileXMLPHD);
	my $root = $document->getDocumentElement;
	
	#recupero nodo ciclo
	my $cycleNode = $root->find("//TableCycle/Cycle[ID=$cycleID]")->get_node(1) or die "$!";
	
	my %cycleDetails;
	
	$cycleDetails{'name'} = $cycleNode->findvalue('Name');
	$cycleDetails{'bYear'} = $cycleNode->findvalue('BeginningYear');
	$cycleDetails{'eYear'} = $cycleNode->findvalue('EndYear');
	
	return %cycleDetails;
	
}

#restituisce hash contenente le informazioni di un supervisore
sub getSupervisorDetails() {
	
	#parametro: ID del supervisore	
	my $supervisorID = $_[0];
	my $parser = XML::LibXML->new();
	
	my $document = $parser->parse_file($fileXMLPHD);
	my $root = $document->getDocumentElement;
	
	#recupero nodo supervisore
	my $supervisorNode = $root->find("//TableSupervisor/Supervisor[ID=$supervisorID]")->get_node(1);
	
	my %supervisorDetails;
	
	$supervisorDetails{'name'} = $supervisorNode->findvalue('Name');
	$supervisorDetails{'surname'} = $supervisorNode->findvalue('Surname');
	$supervisorDetails{'website'} = $supervisorNode->findvalue('Website');
	
	return %supervisorDetails;
	
}


#restituisce supervisori sotto forma di HASH
sub getSupervisorHash() {

	my $parser = XML::LibXML->new();
		
	my $document = $parser->parse_file($fileXMLPHD);
	my $root = $document->getDocumentElement;

	#recupero insieme supervisori
	my $supervisorsList = $root->find("//TableSupervisor/Supervisor");
	
	my %supervisorHash = ();
	
	#per ogni supervisore
	foreach $supervisor ($supervisorsList->get_nodelist) {
		
		#recupero informazioni
		my $name = $supervisor->findvalue('Name');
		my $surname = $supervisor->findvalue('Surname');
		my $id = $supervisor->findvalue('ID');
		
		$name .= " $surname";
		#chiave hash: ID supervisore, valore: nome cognome
		$supervisorHash{$id} = $name;
	}

	return %supervisorHash;
	
}

#restituisce l'insieme dei cicli sotto forma di HASH
sub getCycleHash() {

	my $parser = XML::LibXML->new();
		
	my $document = $parser->parse_file($fileXMLPHD);
	my $root = $document->getDocumentElement;

	#recupero insieme cicli
	my $cycleList = $root->find("//TableCycle/Cycle");
	
	#hash dei cicli
	my %cycleHash = ();
	
	#per ogni ciclo
	foreach $cycle ($cycleList->get_nodelist) {
		
		#recupero informazioni
		my $name = $cycle->findvalue('Name');
		my $beginning = $cycle->findvalue('BeginningYear');
		my $end = $cycle->findvalue('EndYear');
		my $id = $cycle->findvalue('ID');
		
		$name .= " ($beginning - $end)";
		#chiave HASH: ID ciclo, valore: nome cilo + anno inizio + anno fine
		$cycleHash{$id} = $name;
	}

	return %cycleHash;
	
}

#inserisce nuovo dottorando all'interno del file XML
sub insertNewPHDStudent() {
	
	eval {
		#parametro di ingresso: HASH contenente informazioni 
		my %details = %{$_[0]};
		
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileXMLPHD);
		my $root = $document->getDocumentElement;
		
		#creo ID per il nuovo nodo
		my $newID = 0;
		if ($root->exists("//TablePHDStudent/PHDStudent[last()]")) {
			$newID = $root->findvalue("//TablePHDStudent/PHDStudent[last()]/ID");
		}
		
		$newID = $newID + 1;
		
		#pongo a 0 ID del supervisore nel caso sia assente pe compatibilità con file XML
		if ($details{'supervisor'} eq "") {
			$details{'supervisor'} = 0;
		}
		#pongo a 0 ID del ciclo nel caso sia assente pe compatibilità con file XML
		if ($details{'cycle'} eq "") {
			$details{'cycle'} = 0;
		}
		
		if ($details{'lang'} eq "") {
			$details{'lang'} = "it";
		}
		
		my $tablePHD = ($root->find("//TablePHDStudent"))->get_node(1);
		
		#nuovo nodo formato stringa
		my $newStringNode = 
"<PHDStudent>
	<ID>$newID</ID>
	<Name>$details{'name'}</Name>
	<Surname>$details{'surname'}</Surname>
	<ResearchArea language=\"$details{'lang'}\">$details{'researchArea'}</ResearchArea>
	<Website>$details{'website'}</Website>
	<Supervisor>$details{'supervisor'}</Supervisor>
	<Cycle>$details{'cycle'}</Cycle></PHDStudent>";
			
		my $newNode = $parser->parse_balanced_chunk($newStringNode);
		$tablePHD->addChild($newNode);
		
		open(FILE, ">$fileXMLPHD") || die ("Non riesco ad aprire il file");
		print FILE $document->toString();
		close(FILE);
	
		return 1;
	}
	or do { return 0; }
}

#inserisce nuovo supervisore nel file XML
sub insertNewSupervisor() {
	
	eval {
		#parametro in ingresso: HASH contenente informazioni supervisore
		my %input = %{$_[0]};
		
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileXMLPHD);
		my $root = $document->getDocumentElement;
	
		#creo ID nuovo supervisore	
		my $newID = 0;
		if ($root->exists("//TableSupervisor/Supervisor[last()]")) {
			$newID = $root->findvalue("//TableSupervisor/Supervisor[last()]/ID");
		}
		
		$newID = $newID + 1;
		
		#creo nodo formato stringa
		my $newStringNode = 
"<Supervisor>
	<ID>$newID</ID>
	<Name>$input{'name'}</Name>
	<Surname>$input{'surname'}</Surname>
	<Website>$input{'website'}</Website></Supervisor>";
			
		my $newNode = $parser->parse_balanced_chunk($newStringNode);
		my $tableSupervisor = ($root->find("//TableSupervisor"))->get_node(1);
		
		$tableSupervisor->addChild($newNode);
		
		open(FILE, ">$fileXMLPHD") || die("Non riesco ad aprire il file");
		print FILE $document->toString();
		close(FILE);
		
		return 1;
	}
	or do { return 0; } 
	
}

#inserisce nuovo ciclo nel file XML
sub insertNewCycle() {
	
	eval {
		#parametro in ingresso: HASH contenente informazioni ciclo
		my %input = %{$_[0]};
		
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileXMLPHD);
		my $root = $document->getDocumentElement;
		
		#creo ID nuovo nodo
		my $newID = $root->findvalue("//TableCycle/Cycle[last()]/ID");
		if ($newID eq "") {
			$newID = 0;
		}
		$newID = $newID + 1;
		
		#nuovo nodo formato stringa
		my $newStringNode = 
"<Cycle>
	<ID>$newID</ID>
	<Name>$input{'name'}</Name>
	<BeginningYear>$input{'byear'}</BeginningYear>
	<EndYear>$input{'eyear'}</EndYear></Cycle>";
			
		my $newNode = $parser->parse_balanced_chunk($newStringNode);
		my $tableCycle = $root->find("//TableCycle")->get_node(1);
		
		$tableCycle->addChild($newNode);
		
		open(FILE, ">$fileXMLPHD") || die("Non riesco ad aprire il file");
		print FILE $document->toString();
		close(FILE);
		
		return 1;
	}
	or do { return 0; }
		
}

#modifica informazioni dottorando nel file XML
sub modifyPHDStudent() {
	
	eval {
		#parametro in ingresso: HASH contenente nuove informazioni dottorando
		my %details = %{$_[0]}; 	
		
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileXMLPHD);
		my $root = $document->getDocumentElement;
		
		#pongo a 0 ID del supervisore nel caso sia assente pe compatibilità con file XML
		if ($details{'supervisor'} eq "") {
			$details{'supervisor'} = 0;
		}
		#pongo a 0 ID del ciclo nel caso sia assente pe compatibilità con file XML
		if ($details{'cycle'} eq "") {
			$details{'cycle'} = 0;
		}
		
		if ($details{'lang'} eq "") {
			$details{'lang'} = "it";
		}
		
		my $studentID = $details{'idStudent'};
		
		#recupera nodo con vecchie informazioni dottorando
		my $oldNode = $root->find("//TablePHDStudent/PHDStudent[ID=$studentID]")->get_node(1);
		my $parent = $oldNode->parentNode;
		
		#nuovo nodo formato stringa
		my $newNodeString = 
"<PHDStudent>
	<ID>$studentID</ID>
	<Name>$details{'name'}</Name>
	<Surname>$details{'surname'}</Surname>
	<ResearchArea language=\"$details{'lang'}\">$details{'researchArea'}</ResearchArea>
	<Website>$details{'website'}</Website>
	<Supervisor>$details{'supervisor'}</Supervisor>
	<Cycle>$details{'cycle'}</Cycle></PHDStudent>";
			
		my $newNode = $parser->parse_balanced_chunk($newNodeString);
		
		#sostituisce nodo
		$parent->replaceChild($newNode, $oldNode);
		
		open(FILE, ">$fileXMLPHD") || die("Non riesco ad aprire il file");
		print FILE $document->toString();
		close(FILE);
		
		return 1;
	}
	or do { return 0; }
	
}

#modifica informazioni di un ciclo di dottorato
sub editCycle() {

	eval {
		#parametro di ingresso: HASH contenente infromazioni ciclo
		my %details = %{$_[0]};
	
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileXMLPHD);
		my $root = $document->getDocumentElement;
		
		my $oldNode = $root->find("//TableCycle/Cycle[ID=$details{'cycleID'}]")->get_node(1) or die "$!";
		my $parent = $oldNode->parentNode;
		
		my $newNodeString = 
		"<Cycle>
			<ID>$details{'cycleID'}</ID>
			<Name>$details{'name'}</Name>
			<BeginningYear>$details{'bYear'}</BeginningYear>
			<EndYear>$details{'eYear'}</EndYear></Cycle>";
			
		my $newNode = $parser->parse_balanced_chunk($newNodeString);
		
		$parent->replaceChild($newNode, $oldNode);
	
		open(FILE, ">$fileXMLPHD") || die("Non riesco ad aprire il file");
		print FILE $document->toString();
		close(FILE);
		
		return 1;
	}
	or do { return 0; }		

}

#modifica informazioni supervisore
sub editSupervisor() {
	
	eval {
		#parametro di ingresso: HASH contenente nuove informazioni supervisore
		my %details = %{$_[0]};
		
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileXMLPHD);
		my $root = $document->getDocumentElement;
		
		my $oldNode = $root->find("//TableSupervisor/Supervisor[ID=$details{'supervisorID'}]")->get_node(1);
		my $parent = $oldNode->parentNode;
	
		my $newNodeString = 
		"<Supervisor>
		<ID>$details{'supervisorID'}</ID>
		<Name>$details{'name'}</Name>
		<Surname>$details{'surname'}</Surname>
		<Website>$details{'website'}</Website></Supervisor>";
		
		my $newNode = $parser->parse_balanced_chunk($newNodeString);
		
		$parent->replaceChild($newNode, $oldNode);
	
		open(FILE, ">$fileXMLPHD") || die("Non riesco ad aprire il file");
		print FILE $document->toString();
		close(FILE);
	
		return 1;
	}
	or do { return 0; }
	
}


#elimina dottorando da file XML
sub deletePHDStudent() {
	
	eval {
		#parametro di ingresso: ID del dottorando
		my $idPHD = $_[0];
	
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileXMLPHD);
		my $root = $document->getDocumentElement;
		
		#recupera nodo del dottorando
		my $nodePHD = $root->find("//TablePHDStudent/PHDStudent[ID=$idPHD]")->get_node(1);
		my $parent = $nodePHD->parentNode;
		
		$parent->removeChild($nodePHD);
		
		open(FILE, ">$fileXMLPHD") || die("Non riesco ad aprire il file");
		print FILE $document->toString();
		close(FILE);
		
		return 1;
	}
	or do { return 0; }
	
}

sub moveXMLFile() {
 
    my $command = "cp --preserve $fileXMLPHD $fileForRecovery";
	system($command);
	
	$command = "chmod 777 $fileForRecovery";
	system($command);
    
}
