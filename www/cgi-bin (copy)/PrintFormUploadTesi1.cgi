#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use HTML::Entities;
use utf8;
use CGI::Ajax;

binmode STDIN, ":utf8";
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";

require "WorkWithFiles.pl";
require "GlobalVariables.pl";
require "FunctionsUploadTesi.cgi";

my $upload_dir = $siteForCGI . "private/tesimagistrale";

$CGI::POST_MAX = 1024 * 10000000;

my $pjx = new CGI::Ajax('check_status' => \&check_status);
my $q   = CGI->new(\&hook);

sub hook {
            
    my ($filename, $buffer, $bytes_read, $data) = @_;
    
    $bytes_read ||= 0; 
          
    open(COUNTER, ">" . $upload_dir . '/' . $filename . '-meta.txt'); 
    
    my $per = 0; 
    if($ENV{CONTENT_LENGTH} >  0){ # This *should* stop us from dividing by 0, right?
        $per = int(($bytes_read * 100) / $ENV{CONTENT_LENGTH});
    }
    print COUNTER $per;
    close(COUNTER); 
     
}


sub check_status { 
   
   my $filename = $q->param('uploadedfile');
      $filename =~ s{^(.*)\/}{}; 

    return '' 
        if ! -f  $upload_dir . '/' . $filename . '-meta.txt'; 
        
    open my $META, '<', $upload_dir . '/' . $filename  . '-meta.txt' or die $!;
    my $s = do { local $/; <$META> };
    close ($META); 
    
   my $small = 500 - ($s * 5); 
   my $big = $s * 5; 
   
    my $r = '<h1>' . $s . '%</h1>'; 
       $r .= '<div style="width:' . $big . 'px;height:25px;background-color:#6f0;float:left"></div>'; 
       $r .= '<div style="width:' . $small . 'px;height:25px;background-color:#f33;float:left"></div>';
    return $r; 
    
}

sub dump_meta_file { 
   my $filename = $q->param('uploadedfile');
      $filename =~ s{^(.*)\/}{}; 
    unlink($upload_dir . '/' . $filename . '-meta.txt') or warn "deleting meta file didn't work..."; 
}

#costruisco la stringa per la form di upload di una tesi
sub formInsertTesi() {
	
	my $formString = <<CONTENT;
<form method="post" enctype="multipart/form-data">
	<fieldset>
	<legend>Dati Personali</legend>
	<div class="notes">
	<h1>Dati Personali</h1>
	<p class="last">Inserisci Nome, Cognome e Numero di Matricola (xxxxxx)</p>
	</div>
	<label for="name">Nome: </label>
	<input type="text" name="name" id="name" value="$input{'name'}" />
	<label for="surname">Cognome: </label>
	<input type="text" name="surname" id="surname" value="$input{'surname'}" />
	<label for="matricola">Matricola: </label>
	<input type="text" name="matricola" id="matricola" value="$input{'matricola'}" />
	</fieldset>
	<fieldset>
	<legend>Informazioni Tesi</legend>
	<div class="notes">
	<h1>Informazioni tesi</h1>
	<p>Titolo della tesi per intero</p>
	<p>File della tesi solo in formato pdf</p>
	<p>Abstract: breve riassunto della tesi proposta</p>
	<p class="last">Specifica se appartieni alla Laurea Magistrale o alla Laurea Specialistica</p>
	</div>
	<label for="titleTesi">Titolo della Tesi: </label>
	<input type="text" name=\"titleTesi\" id=\"titleTesi\" value=\"$input{'titleTesi'}\" />
	<label for="uploadedfile">File della Tesi: </label>
	<input type="file" name=\"uploadedfile\" id=\"uploadedfile\" />
	<label for="abstract">Abstract: </label>
	<textarea name="abstract" id="abstract" cols="20" rows="8" >$input{'abstract'}</textarea>
	<br /><br />
	<input type="radio" name="laurea" id="radioLM" value="LM" checked="checked" />
	<label for="radioLM">Laurea Magistrale</label><br /><br />
	<input type="radio" name="laurea" id="radioLS" value="LS" />
	<label for="radioLS">Laurea Specialistica</label>
	</fieldset>
	<fieldset>
	<legend class="hidden">Bottoni</legend>
	<input type="submit" name="submit" value="Carica" class="button" />
	<input type="reset" value="Reset" class="button" />
	<input type="hidden" name="yes_upload" value="1" />
	<input type="hidden" name="process" value="1" />
	</fieldset>
<script language="Javascript"> 
    setInterval("check_status(['check_upload__1', 'uploadedfile'], ['statusbar']);",'1000')
</script> 
	<div id="statusbar">
	</div>
</form>
CONTENT

	return $formString;
	
	
}


#controlla che il contenuto degli input di tipo testo non abbia qualcosa che non va bene
sub checkBadContent() {
	
	my $string = $_[0];

	if (index($string, "<?") != -1 || index($string, "?>") != -1 || index($string, "<\%") != -1 || index($string, "\%>") != -1
		|| index($string, "<script") != -1 || index($string, "</script") != -1) {
		return "bad";
		}

}

#funziona che controlla che gli input inseriti siano corretti rispetto a determinate specifiche
sub checkInputs() {
	
	my $errors = "";
	
	#nome deve avere almeno tre caratteri ed essere solo caratteri, no numeri
	if ($input{'name'} !~ /^\D{3}(\D)*$/ || (&checkBadContent($input{'name'}) ne "")) {
    	$errors .= "Nome inserito non corretto<br />";
    }
    #uguale al nome
    if ($input{'surname'} !~ /^\D{3}(\D)*$/ || (&checkBadContent($input{'surname'}) ne "")) {
    	$errors .= "Cognome inserito non corretto<br />";
    }
    #matricola deve essere di sei numeri e basta
    if ($input{'matricola'} !~  /^\d{6}$/ || (&checkBadContent($input{'matricola'}) ne "")) {
    	$errors .= "Numero matricola errato<br />";
    }
    if (defined($input{'titleTesi'}) && (length($input{'titleTesi'}) < 5 || &checkBadContent($input{'titleTesi'}))) {
    	$errors .= "Titolo della tesi errato<br />";
    }
    if (defined($input{'abstract'}) && (length($input{'abstract'}) < 20 || &checkBadContent($input{'abstract'}))) {
    	$errors .= "Abstract errato<br />";
	}
	
	
	return $errors;
	
}

#carica il file della tesi
sub upload_that_file { 

    my $q = shift; 
    
    my $fh       = $q->upload('uploadedfile');
    my $filename = $q->param('uploadedfile');
    
    return '' if ! $filename; 
    
    my $outfile = $upload_dir . '/' . '-' . $q->param('uploadedfile');
    
    open (OUTFILE, '>' . $outfile) 
        or die("can't write to " . $outfile . ": $!");        
    
    while (my $bytesread = read($fh, my $buffer, 1024)) { 
        print OUTFILE $buffer; 
    } 
    
    close (OUTFILE);
    chmod(0666, $outfile);  
    
}

{
	#apro il file di template per la pagina di upload
	my $pageTemplateUpload = &openFile($siteForCGI . "laureamagistrale/uploadtesi.html");	
	utf8::decode($pageTemplateUpload);
	
	#modifico i link per farlo corrispondere al path corretto
	my $srcPath = "src=\"../";
	my $hrefPath = "href=\"../";
	my $newSRC = "src=\"/$folderBase";
	my $newHREF = "href=\"/$folderBase";
	
	#modifico link del menu di secondo livello
	my $linkOrario = "/$folderBase" . "laureamagistrale/orario.html";
	my $linkIndirizzi = "/$folderBase" . "laureamagistrale/indirizzimagistrale.html";
	my $linkCorsi = "/$folderBase" . "laureamagistrale/corsimagistrale.html";
	my $linkPianoStudi = "/$folderBase" . "laureamagistrale/pianostudimagistrale.html";
	my $linkTesi = "/$folderBase" . "laureamagistrale/tesimagistrale.html";
	my $linkAppelliLaurea = "/$folderBase" . "laureamagistrale/appellilaureamagistrale.html";
	my $linkReferenti = "/$folderBase" . "laureamagistrale/referentimagistrale.html";
	my $linkEsami = "/$folderBase" . "laureamagistrale/esamimagistrale.html";
	my $oldIndex = "href=\"index.html\"";
	my $newIndex = "href=\"/" . $folderBase . "laureamagistrale/index.html\"";
	
	$pageTemplateUpload =~ s/$oldIndex/$newIndex/g;
	$pageTemplateUpload =~ s/orario.html/$linkOrario/g;
	$pageTemplateUpload =~ s/indirizzimagistrale.html/$linkIndirizzi/g;
	$pageTemplateUpload =~ s/corsimagistrale.html/$linkCorsi/g;
	$pageTemplateUpload =~ s/esamimagistrale.html/$linkEsami/g;
	$pageTemplateUpload =~ s/pianostudimagistrale.html/$linkPianoStudi/g;
	$pageTemplateUpload =~ s/tesimagistrale.html/$linkTesi/g;
	$pageTemplateUpload =~ s/appellilaureamagistrale.html/$linkAppelliLaurea/g;
	$pageTemplateUpload =~ s/referentimagistrale.html/$linkReferenti/g;
	
	$pageTemplateUpload =~ s/$srcPath/$newSRC/g; 
	$pageTemplateUpload =~ s/$hrefPath/$newHREF/g; 
	
	#devo stampare form per upload delle tesi
	if (index($pageTemplateUpload, "<formUploadTesi/>") != -1) {

		$input{'name'} = $q->param('name');
		$input{'surname'} = $q->param('surname');
		$input{'matricola'} = $q->param('matricola');
		$input{'titleTesi'} = $q->param('titleTesi');
		$input{'fileTesi'} = $q->param('fileTesi');
		$input{'abstract'} = $q->param('abstract');
		$input{'laurea'} = $q->param('laurea');
		$input{'submit'} = $q->param('submit');
		
		my $form = &formInsertTesi();
		
		#utente ha cliccato sul bottone submit
		if ($input{'submit'} eq "Carica") {
			#verifico eventuali errori nell'input
			my $errors = &checkInputs();
			
			if ($errors eq "") {
				
				#provo ad uploadare il file
				my $tryUpload = &upload_that_file($q);
				
				#non ci sono errori
				if ($tryUpload eq "") {
					
					#inserisco tesi in file xml
					&insertNewTesi(\%input);
					$form = "<p>Inserimento avvenuto correttamente</p>";
				}
				else {
					$form = "<div id=\"message\">$tryUpload</div>$form";
				}
			}
			else {
				
				$form = "<div id=\"message\">$errors</div>$form";
			}
		}
		
		$pageTemplateUpload =~ s/<formUploadTesi\/>/$form/;
		
	}
	else {
		
		#nessuna form attiva
		my $textNotActive = "<p>La form per l'inserimento degli abstract per gli appelli di laurea non &egrave; al momento disponibile</p>";
		
		$pageTemplateUpload =~ s/<formNonAttiva\/>/$textNotActive/g; 			
	
	}
		
			
if($input{'submit'} eq "Carica"){ 
print <<CONTENT;
Content-type:text/html\n\n
$pageTemplateUpload

CONTENT

	dump_meta_file();   
}
else {         
	print $pjx->build_html( $q, $pageTemplateUpload);
}

}

