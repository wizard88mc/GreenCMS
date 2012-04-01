#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use utf8;
use Time::localtime;
use Date::Calc qw(Add_Delta_Days Delta_Days);

$parser = XML::LibXML->new();

$document = $parser->load_html(location => 'appellilaurea.html', clean_namespaces=>0,
                                no_defdtd=>1);
$root = $document->getDocumentElement;

$nodoElenco = $root->find('//ul[@id=\'dateLaurea\']')->get_node(1);
@nodiElenco = $root->findnodes('//ul[@id=\'dateLaurea\']/li');

$nodoCorretto;
$i = 0; $ok = 0;

while ($ok == 0) {
    if (index($nodiElenco[$i]->findvalue('a'), 'Orari e Commissioni') == -1) {
        $nodoCorretto = $nodiElenco[$i];
        $ok++;
    }
    $i++;
}

$testo = $nodoCorretto->findvalue('.');

$paginaNuova = '(<a href="prova.html" title="prova.html">Orari e commissioni</a>)';

$testo .= " $paginaNuova";

$nuovoNodoStringa = "<li>$testo</li>";
$nuovoNodo = $parser->parse_balanced_chunk($nuovoNodoStringa);

$root->replaceChild($nuovoNodo, $nodoCorretto);

open(FILE, ">appellilaurea.html") || die("Non riesco ad aprire il file");
print FILE $document->toStringHTML();
close(FILE);

1;