#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use utf8;
use Time::localtime;
use Date::Calc qw(Add_Delta_Days Delta_Days Add_Delta_DHMS);

require "ConnectDatabase.pl";
require "GetTeachersID.pl";
require "GetTeacherInformations.pl";

#insieme di funzioni per la gestione delle news e del feedRSS

$fileXML .= "CommissioneLaurea.xml";


sub getOptionsProfessore() {
    
    my $optionsSelect = '<option value=""> - - - </option><optgroup label="Docenti Interni">';
    
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

sub insertCommissione() {
    
    eval {
    my %informazioni = %{$_[0]};
    
    my $parser = XML::LibXML->new();
		
	my $document = $parser->parse_file($fileXML);
	    
	my $root = $document->getDocumentElement;
    
	my @candidati = split(',', $informazioni{'candidati'});
	
	my $stringCandidati = '<Candidati>';
	
	foreach $candidato (@candidati) {
	    if ($candidato ne "") {
	        if (substr($candidato, 0, 1) eq " ") { $candidato =~ s/ //; }
	        $stringCandidati .= "<Candidato>$candidato</Candidato>";
	    }
	}
	$stringCandidati .= '</Candidati>';
	
	$informazioni{'giorno'} = &convertDateFromItalianToDB($informazioni{'giorno'});
	
	if (length($informazioni{'orario'}) == 4) {
	    $informazioni{'orario'} = '0' . $informazioni{'orario'};   
	}
	$informazioni{'orario'} .= ':00';
	
	my $stringComponenti = '<Componenti>';
	
	foreach my $componente (@{$informazioni{'componenti'}}) {
	    if ($componente ne "") {
	        $stringComponenti .= ", $componente";
	    }
	}
	$stringComponenti =~ s/, //;
	$stringComponenti .= '</Componenti>';
	
	my $stringSupplenti = '<Supplenti>';
	foreach my $supplente (@{$informazioni{'supplenti'}}) {
	    if ($supplente ne "") {
	        $stringSupplenti .= ", $supplente";
	    }
	}
	$stringSupplenti =~ s/, //;
	$stringSupplenti .= '</Supplenti>';
	
	my $stringNewNode = 
"<Commissione>
<Data>$informazioni{'giorno'}</Data>
<Ora>$informazioni{'orario'}</Ora>
<Aula>$informazioni{'aula'}</Aula>
<Presidente>$informazioni{'presidente'}</Presidente>
$stringComponenti
$stringSupplenti
$stringCandidati
</Commissione>";

    my $newNode = $parser->parse_balanced_chunk($stringNewNode);
    
    foreach $node($newNode->childNodes) {
        $root->addChild($node);
    }
  
    
    open(FILE, ">$fileXML") || die("Non riesco ad aprire il file");
    print FILE $document->toString();
    close(FILE);
    
    return 1;
    }
    or do { return 0; }
    
}

sub dividiCandidati() {
    
    my $turni = $_[0];
    
   my $parser = XML::LibXML->new();
		
	my $document = $parser->parse_file($fileXML);
	my $root = $document->getDocumentElement;
	
	my @listaCandidati = $root->findnodes('//Candidati/Candidato');
	
	my @nomiCandidati = ();
	
	foreach my $nodeCandidato (@listaCandidati) {
	    push(@nomiCandidati, $nodeCandidato->textContent);
	}
	
	@nomiCandidati = sort(@nomiCandidati);
	
	# ora ho tutti i nodi dei candidati, li devo dividere per il numero di turni
	my $totaleCandidati = scalar(@listaCandidati);
	my $candidatiPerTurniBase;
	my $resto;
	my @stringheTurniCandidati;
	
	# definisco il numero di candidati per ciascun turno, sulla base del numero 
	# totale ed il numero dei turni 
	{
	    use integer;
	    $candidatiPerTurnoBase = $totaleCandidati / $turni;
	    $resto = $totaleCandidati % $turni;
	}
	my @candidatiPerTurno;
	
	for (my $i = 0; $i < $turni; $i++) {
	     $candidatiPerTurno[$i] = $candidatiPerTurnoBase;   
	}
	
	my $i = 0;
	while ($i < $resto) {
	     $candidatiPerTurno[$i]++;
	     $i++;
	}
	
	my $partenza = 0;
	for (my $j = 0; $j < $turni; $j++) {
	    
	    my $fine = $partenza + $candidatiPerTurno[$j] - 1;
	    
	    my @candidatiTurno = @nomiCandidati[$partenza..$fine];
	    
	    my $stringaCandidatiTurno = '';
	    for my $candidato (@candidatiTurno) {
	        
	        $stringaCandidatiTurno .= ', ' . $candidato;
	    }
	    $stringaCandidatiTurno =~ s/, //;
	    
	    $stringheTurniCandidati[$j] = $stringaCandidatiTurno;
	    
	    $partenza = $partenza + $candidatiPerTurno[$j];
	}
    
    return @stringheTurniCandidati;
    
}

sub insertNuovaProclamazione() {
    
    #eval {
        my %informazioni = %{$_[0]};
        
        my $parser = XML::LibXML->new();
		
        my $document = $parser->parse_file($fileXML);
        my $root = $document->getDocumentElement;
        
        $informazioni{'giorno'} = &convertDateFromItalianToDB($informazioni{'giorno'});
        $informazioni{'orario'} .= ':00';
        
        my ($ore, $minuti, $secondi) = &getTimeComponents($informazioni{'orario'});
        my ($giorno, $mese, $anno) = &getDateComponentsFromDBDate($informazioni{'giorno'});
        
        my $turniTotali = $informazioni{'turni'};
        my $indiceTurni = 1;
        my @arrayCandidati = @{$informazioni{'candidati'}};
        
        my $stringTurni = '<Turni>';
        
        while ($indiceTurni <= $turniTotali) {
            my $indiceArray = $indiceTurni - 1;
            $stringTurni .= 
"<Turno><Ora>$ore:$minuti:$secondi</Ora>
<Candidati>$arrayCandidati[$indiceArray]</Candidati></Turno>";

            ($anno, $mese, $giorno, $ore, $minuti, $secondi) = 
                Add_Delta_DHMS($anno, $mese, $giorno, $ore, $minuti, $secondi, 
                    0, 0, $informazioni{'distacco'}, 0);
                if ($secondi == 0) {
                    $secondi = '00';
                }
                if ($ore < 10) { $ore = "0$ore"; }
                if ($minuti < 10) { $minuti = "0$minuti"; }

            $indiceTurni++;
            
        }
        $stringTurni .= '</Turni>';
        
        my $newNodeString = 
"<Proclamazione>
<Data>$informazioni{'giorno'}</Data>
<Orario>$informazioni{'orario'}</Orario>
<Aula>$informazioni{'aula'}</Aula>
<Presidente>$informazioni{'presidente'}</Presidente>
<Componenti>$informazioni{'commissione'}</Componenti>
<Supplenti>$informazioni{'supplenti'}</Supplenti>
$stringTurni
</Proclamazione>";

        my $nuovoNodoProclamazione = $parser->parse_balanced_chunk($newNodeString);
        
        foreach my $node ($nuovoNodoProclamazione->childNodes) {
            $root->addChild($node);
        }
    
        open(FILE, ">$fileXML") || die("Non riesco ad aprire il file");
        print FILE $document->toString();
        close(FILE);
        
        return 1;
    #}
    #or do { return 0; }
        
}

sub getNumeroCommissioneInTesto() {
    
    my @elenco = ('Prima', 'Seconda', 'Terza', 'Quarta', 'Quinta');
    my $posizione = $_[0];
    
    return $elenco[$posizione - 1];
}

sub getMeseTestuale() {
    
    my @mesi = ('Gennaio','Febbraio','Marzo','Aprile','Maggio','Giugno','Luglio',
        'Agosto','Settembre','Ottobre','Novembre','Dicembre');
    my $posizione = $_[0];
    
    return $mesi[$posizione - 1];
}

sub getNumeroRomano() {
 
    my $posizione = $_[0];
    my @numeri = ('I', 'II', 'III', 'IV', 'V', 'VI', 'VII');
    
    return $numeri[$posizione - 1];
    
}

sub creaPaginaCommissione() {
 
    #eval 
        my $paginaCreata;
        if ($_[0] == 0) {
            # devo creare pagina per la laurea
            $paginaCreata = &creaPaginaLaurea();
        }
        else {
            #devo creare pagina per la magistrale
            $paginaCreata = &creaPaginaMagistrale();
        }
        
        &deleteXMLFileContent();
        return $paginaCreata;
    #}
    #or do { return ""; }
}

sub creaPaginaLaurea() {
 
    my $percorsoBase = $sourcePath . 'pagesSource/laurea/source/';
    my $templatePagina = $percorsoBase . 'commissioni_template.html';
    my $paginaBase = &openFile($templatePagina);
    
    my $parser = XML::LibXML->new();
		
	my $document = $parser->parse_file($fileXML);
	my $root = $document->getDocumentElement;
    
    my $dataTitolo = $root->findvalue('//Proclamazione/Data');
    my ($giorno, $mese, $anno) = &getDateComponentsFromDBDate($dataTitolo);
    $mese = &getMeseTestuale($mese);
    
    my $stringOnThisPage = '';
    my $stringaTitolo = "Commissioni di Laurea, $giorno $mese $anno";
    my $stringElencoCommissioni = '';
    
    my @elencoCommissioni = $root->findnodes('//Commissione');
    my $counter = 1;
    
    foreach my $nodoCommissione (@elencoCommissioni) {
        
        my $numeroTestuale = &getNumeroCommissioneInTesto($counter);
        
        $stringOnThisPage .= 
        "<li><a href=\"#commissione$counter\">$numeroTestuale Commissione Laurea in Informatica</a></li>";
        
        my $commissioneTestualeCreata = &creaSingolaCommissione($nodoCommissione, $counter, 0);
        
        $stringElencoCommissioni .= $commissioneTestualeCreata;
        
        $stringElencoCommissioni .= 
        "<p class=\"tornaSu withBorderBottom\"><a href=\"#contentsLong\">Torna su &#9650;</a></p>";     
        
        $counter++;
    }
    
    my $nodoProclamazione = $root->find('//Proclamazione')->get_node(1);
    
    my $stringProclamazione = &creaProclamazione($nodoProclamazione);
        
    $stringProclamazione .= 
    "<p class=\"tornaSu withBorderBottom\"><a href=\"#contentsLong\">Torna su &#9650;</a></p>";
    
    $stringOnThisPage .= 
    "<li><a href=\"#proclamazioneLaurea\">Commissione Proclamazione Laurea in Informatica</a></li>";
    
    
    $paginaBase =~ s/<onThisPage\/>/$stringOnThisPage/;
    $paginaBase =~ s/<commissioniLaurea\/>/$stringElencoCommissioni/;
    $paginaBase =~ s/<proclamazioneLaurea\/>/$stringProclamazione/;
    
    my $meseNomePagina = substr($mese, 0, 3);
    $meseNomePagina =~ tr/A-Z/a-z/;
    
    my $nomePagina = "commissioni$giorno$meseNomePagina$anno.html";
    
    &createFile($percorsoBase . "$nomePagina", $paginaBase);
    
    &nuovaPaginaSource($stringaTitolo, $nomePagina, $giorno, $mese, $anno, 0);
    
    return $nomePagina;
    
}

sub creaPaginaMagistrale() {
    
    my $percorsoBase = $sourcePath . 'pagesSource/laureamagistrale/source/';
    my $templatePagina = $percorsoBase . 'commissioni_template.html';
    my $paginaBase = &openFile($templatePagina);
    
    my $parser = XML::LibXML->new();
		
	my $document = $parser->parse_file($fileXML);
	my $root = $document->getDocumentElement;
    
    my $dataTitolo = $root->findvalue('//Commissione/Data');
    my ($giorno, $mese, $anno) = &getDateComponentsFromDBDate($dataTitolo);
    $mese = &getMeseTestuale($mese);
    
    my $stringaTitolo = "Commissioni di Laurea, $giorno $mese $anno";
    my $stringElencoCommissioni = '';
    
    my @elencoCommissioni = $root->findnodes('//Commissione');
    my $counter = 1;
    
    foreach my $nodoCommissione (@elencoCommissioni) {
        
        my $numeroTestuale = &getNumeroCommissioneInTesto($counter);
        
        my $commissioneTestualeCreata = &creaSingolaCommissione($nodoCommissione, $counter, 1);
        
        $stringElencoCommissioni .= $commissioneTestualeCreata;
        
        $stringElencoCommissioni .= 
        "<p class=\"tornaSu withBorderBottom\"><a href=\"#contentsLong\">Torna su &#9650;</a></p>";     
        
        $counter++;
    }
    
    $paginaBase =~ s/<commissioneLaurea\/>/$stringElencoCommissioni/;
    
    my $meseNomePagina = substr($mese, 0, 3);
    $meseNomePagina =~ tr/A-Z/a-z/;
    
    my $nomePagina = "commissioniMagistrale$giorno$meseNomePagina$anno.html";
    
    &createFile($percorsoBase . "$nomePagina", $paginaBase);
    
    &nuovaPaginaSource($stringaTitolo, $nomePagina, $giorno, $mese, $anno, 1);
    
    return $nomePagina;
    
}

# dato un nodo XML rappresentante una commissione di Laurea, crea l'elenco 
# corrispondente da inserire all'interno della pagina
sub creaSingolaCommissione() {
 
    my $nodoCommissione = $_[0];
    my $ordineElenco = $_[1];
    my $laurea = $_[2];
    
    my $ordineTitolo = &getNumeroCommissioneInTesto($ordineElenco);
    my $aula = $nodoCommissione->find('Aula')->get_node(1)->firstChild->toString;
    
    my $titolo = "$ordineTitolo Commissione di Laurea in Informatica (Aula $aula)";
    if ($laurea == 1) {
        $titolo = 'Discussione e Proclamazione Laurea Magistrale in Informatica';   
    }
    
    my $data = $nodoCommissione->find('Data')->get_node(1)->firstChild->toString;
    my ($giorno, $mese, $anno) = &getDateComponentsFromDBDate($data);
    $mese = &getMeseTestuale($mese);
    
    my $orario = $nodoCommissione->find('Ora')->get_node(1)->firstChild->toString;
    $orario = substr($orario, 0, 5);
    my $orarioInizio = "<strong>Orario inizio: </strong> $giorno $mese $anno, ore $orario";
    
    my $presidente = $nodoCommissione->find('Presidente')->get_node(1)->firstChild->toString;
    $presidente = "<strong>Presidente: </strong>$presidente";
    
    my $componenti = $nodoCommissione->find('Componenti')->get_node(1)->firstChild->toString;
    my $supplenti = $nodoCommissione->find('Supplenti')->get_node(1)->firstChild->toString;
    
    my $commissione = "<strong>Commissione: </strong>$componenti (Supplenti: $supplenti)";
    
    my @candidati = $nodoCommissione->findnodes('Candidati/Candidato');
    my $stringCandidati = '<strong>Candidati: </strong>';
    
    foreach my $candidato (@candidati) {
        my $nomeCandidato = $candidato->firstChild->toString;
        $stringCandidati .= ", $nomeCandidato";    
    }
    $stringCandidati =~ s/,//;
    
    my $commissioneCompleta = 
"<dl id=\"commissione$ordineElenco\">
    <dt>$titolo</dt>
    <dd>$orarioInizio</dd>
    <dd>$presidente</dd>
    <dd>$commissione</dd>
    <dd>$stringCandidati</dd>
</dl>
";
    
    return $commissioneCompleta;
    
}

sub creaProclamazione() {
    
    my $nodoProclamazione = $_[0];
    
    my $aula = $nodoProclamazione->find('Aula')->get_node(1)->firstChild->toString;
    my $data = $nodoProclamazione->find('Data')->get_node(1)->firstChild->toString;
    my ($giorno, $mese, $anno) = &getDateComponentsFromDBDate($data);
    $mese = &getMeseTestuale($mese);
    my $orarioInizio = $nodoProclamazione->find('Orario')->get_node(1)->firstChild->toString;
    $orarioInizio = substr($orarioInizio, 0, 5);
    
    my $stringData = "<strong>Orario inizio: </strong> $giorno $mese $anno, $orarioInizio";
    
    my $presidente = $nodoProclamazione->find('Presidente')->get_node(1)->firstChild->toString;
    my $commissione = $nodoProclamazione->find('Componenti')->get_node(1)->firstChild->toString;
    my $supplenti = $nodoProclamazione->find('Supplenti')->get_node(1)->firstChild->toString;
    
    my $stringPresidente = "<strong>Presidente: </strong>$presidente";
    my $stringCommissione = "<strong>Commissione: </strong>$commissione (Supplenti: $supplenti)";
    
    my @elencoTurni = $nodoProclamazione->findnodes('Turni/Turno');
    
    my $stringaProclamazione = 
"<dl id=\"proclamazioneLaurea\">
    <dt>Proclamazione Laurea in Informatica</dt>
    <dd><strong>Luogo: </strong>$aula</dd>
    <dd><strong>Orario Inizio: </strong>$giorno $mese $anno, $orarioInizio</dd>
    <dd><strong>Presidente: </strong>$presidente</dd>
    <dd><strong>Commissione: </strong>$commissione (Supplenti: $supplenti)</dd>
";
    
    my $counter = 1;
    
    foreach my $turno (@elencoTurni) {
        
        my $ora = $turno->findvalue('Ora');
        my $ora = substr($ora, 0, 5);
        $ora =~ s/:/./;
        my $candidati = $turno->findvalue('Candidati');
        
        my $numeroTurno = &getNumeroRomano($counter);
        
        $stringaProclamazione .= "<dd><strong>$numeroTurno&deg; Turno, ore $ora: </strong>$candidati</dd>";
        
        $counter++;     
    }
    
    $stringaProclamazione .= "</dl>";
    
    return $stringaProclamazione;
}

sub nuovaPaginaSource() {
    
    my $titolo = $_[0];
    my $nomePagina = $_[1];
    my $giorno = $_[2]; my $mese = $_[3]; my $anno = $_[4];
    my $magistrale = ''; 
    if ($_[5] != 0) { $magistrale = ' Magistrale'; }
    my $magistraleSmall = $magistrale;
    $magistraleSmall =~ s/ //;
    $magistraleSmall =~ tr/A-Z/a-z/;
    
    my $nuovoNodoStringa = 
"<pageDetails isStatic=\"T\">
    <metaTags>
        <title>Laurea$magistrale in Informatica - Commissioni di Laurea, $giorno $mese $anno</title>
        <description>Pagina che contiene le commissioni di Laurea$magistrale del $giorno $mese $anno</description>
        <keywords>
            <keyword>Commissioni</keyword>
            <keyword>Laurea</keyword>
            <keyword>$giorno $mese $anno</keyword>
        </keywords>
    </metaTags>
    <pageTitle>$titolo</pageTitle>
    <secondLevelMenuNotSelected/>
    <otherParent>Appelli di Laurea/appellilaurea$magistraleSmall.html</otherParent>
    <contentsPageFileName>$nomePagina</contentsPageFileName>
</pageDetails>
";

    my $xmlSourceFile = $sourcePath . "pagesSource/laurea$magistraleSmall/source/xmlSource.xml";
    
    my $parser = XML::LibXML->new();
		
    my $document = $parser->parse_file($xmlSourceFile);
    my $root = $document->getDocumentElement;
    
    my $nuovoNodo = $parser->parse_balanced_chunk($nuovoNodoStringa);
    
    foreach my $nodo ($nuovoNodo->childNodes) {
        $root->addChild($nodo);   
    }
    
    open(FILE, ">$xmlSourceFile") || die("$xmlSourceFile");
    print FILE $document->toString();
    close(FILE);
}

sub deleteXMLFileContent() {
    
    my $parser = XML::LibXML->new();
		
	my $document = $parser->parse_file($fileXML);
	my $root = $document->getDocumentElement;
	
	my @childNodes = $root->childNodes;
	
	foreach my $child (@childNodes) {
	     $root->removeChild($child);   
	}
	
	open(FILE, ">$fileXML") || die("File not opened deleteXMLFileContent()");
    print FILE $document->toString();
    close(FILE);
}

1;
