#!/usr/bin/perl -w

use utf8;
use XML::LibXSLT;
use XML::LibXML;
use Encode;

require "GlobalVariables.pl";

#leggo i parametri ricevuti dalla get
  $buffer = $ENV{'QUERY_STRING'};
  my @pairs = split(/&/, $buffer);
  foreach $pair (@pairs) {
  my ($name, $value) = split(/=/, $pair);
  $value =~ tr/+/ /;
  $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/;
  $name =~ tr/+/ /;
  $name =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C",hex($1))/;
  $input{$name} = $value;}
  
  my $parser = XML::LibXML->new();
  my $xslt = XML::LibXSLT->new();
  
  my $ordinamento ="";
  my $paginaCorsi = $siteForCGI . "laureamagistrale/corsimagistraleen.html";
  
  #scelgo il file xsl da applicare in base al parametro colonna reperito dalla get
  if ($input{'colonna'} eq "docenti") {
    $ordinamento = "ordinaDocenteen.xsl";
  } 
  if ($input{'colonna'} eq "corsi") {
    $ordinamento = "ordinaCorsien.xsl";
  } 
  if ($input{'colonna'} eq "anno") {
    $ordinamento = "ordinaAnnoTrimestreen.xsl";
  } 
  if ($input{'colonna'} eq "trimestre") {
    $ordinamento = "ordinaTrimestreAnnoen.xsl";
  } 
    
  if ($ordinamento eq "") {
    #stampa pagina di errore
  }
  
  my $source = $parser->parse_file($paginaCorsi);
  my $style_doc = $parser->parse_file($ordinamento);
  
  my $stylesheet = $xslt->parse_stylesheet($style_doc);
  
  my $results = $stylesheet->transform($source);
  
  #modifica dei path perche' la pagina prima era fuori dalla cartella cgi-bin
  #trasform il documento xml in una stringa
  my $nuovaPagina = $results->toString; 
  utf8::decode($nuovaPagina);
  
  #variabili per modificare i path
  my $path = "laureamagistrale/";
  
  my $srcPath = "src=\"../";
  my $hrefPath = "href=\"../";
  #noref serve per fare in modo che non vengano applicate le regole successive
  my $newSRC = "src=\"../$folderBase";
  my $newHREF = "noref=\"../$folderBase";
  my $linkOrg = "noref=\"../$folderBase" . $path;
  my $oldLinkOrg = "href=\"";
  
  #preservo i link assoluti 
  $nuovaPagina =~ s/href=\"http/hnoref=\"http/g; 
  $nuovaPagina =~ s/href=\"\//hnoref=\"\//g; 
  #preservo i link alla stessa pagina
  $nuovaPagina =~ s/href=\"#/hnoref=\"#/g; 
  #preservo i link che tornano indietro con ..
  $nuovaPagina =~ s/href=\"..\//hnoref=\"..\//g;
  
  #modifica dei path del menu' del secondo livello
  $nuovaPagina =~ s/$oldLinkOrg/$linkOrg/g; 
  #modifica dei path di immagini e script (src)
  $nuovaPagina =~ s/$srcPath/$newSRC/g; 
   
  #rimetto a posto i link che tornano indietro con ..
  $nuovaPagina =~ s/hnoref=\"..\//href=\"..\//g;
  $nuovaPagina =~ s/$hrefPath/$newHREF/g; 
    
  #rimetto a posto i link preservati
  $nuovaPagina =~ s/hnoref=\"/href=\"/g;  
  $nuovaPagina =~ s/noref=\"/href=\"/g;
  
  print "Content-Type: text/html\n";
  print "Content-Encoding: utf8\n\n";
  
  #print $stylesheet->output_as_bytes($results);
  print $nuovaPagina;
