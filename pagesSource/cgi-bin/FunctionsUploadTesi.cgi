#!/usr/bin/perl


use DBI;
use DBD::mysql;
use XML::LibXML;
use HTML::Entities;
use File::Basename;
use utf8;

require "InsertThesisPageArchive.cgi";
require "ConnectDatabase.pl";
require "GetTeachersID.pl";
require "GetTeacherInformations.pl";

$archiveXML = $fileXML . "ArchiveThesis.xml";
$fileXML .= "Thesis.xml";
$fileForRecovery = $sourcePath . 'pagesSource/xml_files/ArchiveThesis.xml';


#funzione per l'inserimento di una nuova tesi
sub insertNewTesi() {
	
	my %input = %{$_[0]};
	my $parser = XML::LibXML->new();
	
	my $document = $parser->parse_file($fileXML) or die "$!";
	my $root = $document->getDocumentElement;

	my $tableThesis	= $root->find("//TableThesis")->get_node(1) or die "$!";
	
	#nel caso in cui sia già stata inserita la tesi, elimino il vecchio nodo per sostituirlo
	#con quello con i nuovi dati inseriti
	if ($tableThesis->exists("Thesis[Matricola=$input{'matricola'}]")) {
		
		my $oldNode = $tableThesis->find("Thesis[Matricola=$input{'matricola'}]")->get_node(1);
		my $parent = $oldNode->parentNode;
		
		$parent->removeChild($oldNode);
		
	}
	
	if ($input{'lang'} eq "") {
		$input{'lang'} = "it";
	}
	
	#creo nuovo nodo per la tesi in formato stringa
	my $newThesisString = 
	"<Thesis lang=\"$input{'lang'}\">
    <Name>$input{'name'}</Name>
    <Surname>$input{'surname'}</Surname>
    <Matricola>$input{'matricola'}</Matricola>
    <Relatore>$input{'relatore'}</Relatore>
    <Title>$input{'titleTesi'}</Title>
    <FileName>$input{'fileTesi'}</FileName>
    <Abstract>$input{'abstract'}</Abstract>
    <TipoLaurea>$input{'laurea'}</TipoLaurea></Thesis>";
	
	#converto nuovo nodo 
	my $newNode = $parser->parse_balanced_chunk($newThesisString) or die "$!";
	
	#aggiungo nuovo nodo
	for my $nodeToAdd($newNode->childNodes) {
	    $tableThesis->addChild($nodeToAdd);
	}
	
	#scrivo file XML
	open(FILE, ">$fileXML") or die("Non riesco ad aprire il file");
	print FILE $document->toString();
	close(FILE);
	
}


#funzione utilizzata per verificare che i dati inseriti per la presentazione corrispondano ad una 
#tesi inserita precedenetemente
sub checkMatricola() {
	
	my $parser = XML::LibXML->new();
	
	my $document = $parser->parse_file($fileXML);
	my $root = $document->getDocumentElement;

	my $matricola = $_[0];
	my $name = $_[1];
	my $surname = $_[2];

	#cerco valore fittizio..se viene ritornato valore nullo vuol dire che non esiste nodo
	my $checkOK = $root->findvalue("//TableThesis/Thesis[Matricola=$matricola and Name=\"$name\" and Surname=\"$surname\"]/TipoLaurea");	
	
	if ($checkOK eq "") {
		return "Dati inseriti non corrispondo a nessuna Tesi inserita";
	}
	else {
		return "";
	}
}

#restituisce l'elenco delle tesi sotto forma di <option> HTML per la visualizzazione in una form
sub getThesisList() {
	
	my $parser = XML::LibXML->new();
	
	my $document = $parser->parse_file($fileXML);
	my $root = $document->getDocumentElement;
	
	my $thesisList = $root->find("//TableThesis/Thesis");
	
	my $thesisOptions = "";
	
	#per ogni tesi creo opzione dove valore identificativo è il nome del file della tesi (diverso per tutti)
	foreach my $thesis ($thesisList->get_nodelist) {
		
		my $matricola = $thesis->findvalue('Matricola');
		my $name = $thesis->findvalue('Name');
		my $surname = $thesis->findvalue('Surname');
		my $fileName = $thesis->findvalue('FileName');
		my $type = $thesis->findvalue('TipoLaurea');
		
		my $thesisOptions .= "<option value=\"$fileName\">$matricola - $name $surname ($type)</option>";
		
	}
	
	return $thesisOptions;
	
}

#archivia tesi di una sessione da Thesis.xml a 
sub archiveThesis() {
	
	#parametri: mese e anno sessione di laurea
	my $month = $_[0];
	my $year = $_[1];
	
	my @monthIt = ("Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre");
	my @monthEn = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December");
	
	my $parser = XML::LibXML->new();
	
	my $documentThesis = $parser->parse_file($fileXML) or die "$!";
	my $root = $documentThesis->getDocumentElement;
	
	
	my $documentArchive = $parser->parse_file($archiveXML);
	my $rootArchive = $documentArchive->getDocumentElement;
	
	my $stringNewArchive = "<ArchiveThesis MonthSession=\"$month\" Year=\"$year\">";
	
	my $tableArchive = $rootArchive->find('//TableArchiveThesis')->get_node(1);
	
	my $listThesis = $root->find("//TableThesis/Thesis");
	
	my $stringIt = "<h3>$monthIt[$month - 1] $year</h3>";
	my $stringEn = "<h3>$monthEn[$month - 1] $year</h3>";
	
	foreach my $thesis ($listThesis->get_nodelist) {
	
		my $name = $thesis->find('Name')->get_node(1)->firstChild->toString;
		my $surname = $thesis->find('Surname')->get_node(1)->firstChild->toString;
		my $matricola = $thesis->findvalue('Matricola');
		my $title = $thesis->find('Title')->get_node(1)->firstChild->toString;
		my $abstract = $thesis->find('Abstract')->get_node(1)->firstChild->toString;
		my $matricola = $thesis->findvalue('Matricola');
		my $relatore = $thesis->find('Relatore')->get_node(1)->firstChild->toString;
		my $lang = $thesis->findvalue('@lang');
		
		my $newNodeString = "
	<Thesis lang=\"$lang\">
		<Name>$name</Name>
		<Surname>$surname</Surname>
		<Matricola>$matricola</Matricola>
		<Relatore>$relatore</Relatore>
		<Title>$title</Title>
		<Abstract>$abstract</Abstract></Thesis>";
		
		my $parent = $thesis->parentNode;
		$parent->removeChild($thesis);
		
		$stringNewArchive .= $newNodeString;
		
		
		if ($lang eq "it") {
			
			$stringIt .= "<h4>$title - $name $surname - $matricola - Relatore: $relatore</h4><p class=\"withBorderBottom\">$abstract</p>";
			$stringEn .= "<h4 xml:lang=\"it\">$title - $name $surname - $matricola - Relatore $relatore</h4><p class=\"withBorderBottom\" xml:lang=\"it\">$abstract</p>";
		}
		else {
			$stringIt .= "<h4><span xml:lang=\"en\">$title</span> - $name $surname- $matricola - Relatore: $relatore </h4><p class=\"withBorderBottom\" xml:lang=\"en\">$abstract</p>";
			$stringEn .= "<h4>$title - <span xml:lang=\"it\">$name $surname</span> - $matricola - Supervisor: $relatore</h4><p class=\"withBorderBottom\">$abstract</p>";
		}
	}
	
	$stringNewArchive .= "
	</ArchiveThesis>";
	
	my $newNode = $parser->parse_balanced_chunk($stringNewArchive);	
	
	my $firstNode = $tableArchive->find('//ArchiveThesis[1]')->get_node(1);
	
	$tableArchive->insertBefore($newNode, $firstNode);
	
	#scrivo file XML
	open(FILE, ">$fileXML") or die "$!";
	print FILE $documentThesis->toString();
	close(FILE);
	
	#scrivo file XML
	open(FILE, ">$archiveXML") or die "$!";
	print FILE $documentArchive->toString();
	close(FILE);
	
	my $command = "cp --preserve $archiveXML $fileForRecovery";
	system($command);
	
	$command = "chmod 777 $fileForRecovery";
	system($command);
	
	utf8::encode($stringIt);
	utf8::encode($stringEn);
	
	&insertThesisPageArchive($stringIt, $stringEn);
	
	return "ok";
	
}

sub getOptionsRelatore() {
    
    my $optionsSelect = '<optgroup label="Docenti Interni">';
    
    my $DBIConnection = &connectDatabase("www") or die "$!";

    # identificativi per docente interno
    my $idTP = "2";
    my $idTG = "121";

    my $teachersID = &getTeachersID($DBIConnection, $idTP, $idTG) or die "$!";
    
    while (my $teacher = $teachersID->fetchrow_hashref()) {
        
        my $teacherID = $teacher->{'ID'};
        my $nameSurnameQuery = "SELECT Persona.VARCHAR02 as Cognome, Persona.VARCHAR03 as Nome
FROM Persona
WHERE Persona.ID = $teacherID; ";
        
       my $queryHandle = $DBIConnection->prepare($nameSurnameQuery);
        $queryHandle->execute();
	
        my ($surname, $name) = $queryHandle->fetchrow_array();
        
        my $teacherName = $surname . ' ' . $name;
        my $teacherValue = $name . ' ' . $surname;
        
        $optionsSelect .= "<option value=\"$teacherValue\">$teacherName</option>";
        
    }
    
    $optionsSelect .= '</optgroup>';
    
    $optionsSelect .= '<optgroup label="Docenti Esterni">';
    #identificativi per docente esterno
    $idTP = "10";
	$idTG = "121";
	
	$teachersID = &getTeachersID($DBIConnection, $idTP, $idTG) or die "$!";
    
    while (my $teacher = $teachersID->fetchrow_hashref()) {
        
        my $teacherID = $teacher->{'ID'};
        my $nameSurnameQuery = "SELECT Persona.VARCHAR02 as Cognome, Persona.VARCHAR03 as Nome
FROM Persona
WHERE Persona.ID = $teacherID; ";
        
       my $queryHandle = $DBIConnection->prepare($nameSurnameQuery);
        $queryHandle->execute();
	
        my ($surname, $name) = $queryHandle->fetchrow_array();
        
        my $teacherName = $surname . ' ' . $name;
        
        $optionsSelect .= "<option value=\"$teacherName\">$teacherName</option>";
        
    }
	
    $optionsSelect .= '</optgroup>';
    
    $DBIConnection->disconnect();
    
    return $optionsSelect;
}

1;
