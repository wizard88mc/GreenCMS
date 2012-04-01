#!/usr/bin/perl -w

################################################# 
# abstract.cgi 
# 
# Scritto da Ombretta Gaggi 
# Versione:20/11/2009 
# 
#################################################

use strict 'refs';
use lib '..';
use CGI qw(:standard);
use CGI::Carp qw/fatalsToBrowser/;

$upload_dir = "../private/tesimagistrale"; 

$dir_lettura = "../private/tesimagistrale"; 

$dir_web = "http://docenti.math.unipd.it/gaggi/"; 


# path del file con l'elenco degli iscritti 
$file = '/opt/service.dipartimento/apache/sites/docenti/perl/gaggi/abstract.txt';

$flock="y"; 
#file locking. Don't change it to n unless your system has trouble using file locking.

$title="Inserimento Abstract Tesi";

$query = new CGI; 

print header();

&controllaForm;

$matricola = $query->param("matricola"); 
$filename = "$matricola.pdf"; 
$filename =~ s/.*[\/\\](.*)/$1/; 
$upload_filehandle = $query->upload("uploaded_file"); 


if ($upload_filehandle eq ''){
    $errore = "handle";
}

if (my $file = param('uploaded_file')) {
    my $tmpfile=tmpFileName($file);
    my $mimetype = uploadInfo($file)->{'Content-Type'} || '';
    print hr(),
          h2($file),
          h3($tmpfile),
          h4("MIME Type:",em($mimetype));
}


if (open UPLOADFILE,">$upload_dir/$filename"){ 
     binmode UPLOADFILE; 
     while ( <$upload_filehandle> ) 
     { 
         print UPLOADFILE; 
     } 
     close UPLOADFILE; 
 } else {$errore = "apertura file";}
 
 print $query->header ( ); 
 
 $title = "Inserimento avvenuto";
 $titolo = $query->param("titolo");
    
 &stampa_int;
 print "<div id='corpo'>\n";
 print "<h2>Inserimento avvenuto con successo</h2>\n";
 print "<p>L'abstract della tesi <i>$titolo</i> &egrave stato inserito. \n";
 print "</p>\n";
# print "<p> Consulta le <a href='leggi_abstract.cgi'>liste</a> degli abstract inseriti. </p>\n";
 print "</div>\n";
 &stampa_piede;
 
# controlla che tutti i valori siano stati inseriti 
sub controllaForm{
    if ($query->param('cognome') eq ""){ 
        $errore = "cognome"; 
        &stampa_errore;
    }
    if ($query->param('nome') eq "") {
        $errore = "nome"; 
        &stampa_errore;
    }
    if ($query->param('matricola') eq "") {
        $errore =  "matricola"; 
        &stampa_errore;
    }
    if ($query->param('laurea') eq ""){
        $errore =  "laurea"; 
        &stampa_errore;
    }
    if ($query->param('titolo') eq "") {
        $errore = "titolo"; 
        &stampa_errore;
    }
    if ($query->param("uploaded_file") eq "") {
        $errore =  "file"; 
        &stampa_errore;
    }
    if ($query->param('abstract') eq "") {
        $errore = "abstract"; 
        &stampa_errore;
    }
}  
    
# stampa intestazione pagina 
sub stampa_int{

print   qq{<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"  xml:lang="it" lang="it">
<head>
    <title>$title</title>
    <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"/>
    <meta name="title" content="Corso di Laurea in Informatica - Inserimento Abstract tesi di laurea" />
    <meta name="author" content="Ombretta Gaggi" />
    <meta name="language" content="italian it" />
    <link href="$dir_web/corsi.css" rel="stylesheet" type="text/css" media="screen"/>
    <link href="$dir_web/corsi_print.css" rel="stylesheet" type="text/css" media="print"/>
</head>

<body>

    <div id="header">
        <span id="logo"></span>
        <h1>Prova Finale</h1>
            <p>Laurea Triennale in Informatica<br/>
            Laurea Specialistica in Informatica<br/>
            Dipartimento di Matematica Pura ed Applicata - Universit&agrave; di Padova <br/></p>
    </div>

    <div id="path">Ti trovi in: Home &gt; $title</div>

};

}


#stampa il div piede della pagina 
sub stampa_piede{

print qq{
    <div id="piede">
        <img src="http://docenti.math.unipd.it/gaggi/img/css.bmp" class="valid" alt="CSS Valid!"/>
        <img src="http://docenti.math.unipd.it/gaggi/img/xhtml.bmp" class="valid" alt="XHTML 1.0 Valid!"/>
        Ultima modifica: <script type="text/javascript"  src="http://docenti.math.unipd.it/gaggi/ultima_modifica.js"></script>
    </div>
</div></body> </html>};
 
}


sub stampa_errore{
    $title = "Dati incompleti: $errore";
    &stampa_int;
       print "<div id='corpo'> \n";
       print "<h2>$title</h2>\n";
       print "<p>Si prega di compilare tutti i campi e di inviare nuovamente il form.</p>\n";
       print "<p align='center'><a href='http://informatica.math.unipd.it/cgi-bin/abs.cgi'> Indietro</a>.</p>\n";
       print "</div>\n";
       &stampa_piede;
       exit;
}
