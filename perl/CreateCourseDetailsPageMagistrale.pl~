#!/usr/bin/perl

use HTML::Entities;
use utf8;

binmode STDERR, ":utf8";

require "GetCourseSite.pl";

#parametri: 
#    $_[0] - hash contenente le informazioni del corso
#    $_[1] - discriminante se la pagina è in italiano o in inglese

sub createCourseDetailsPageMagistrale() {
	
	my %informations = %{$_[0]};
	my $en = $_[1];
	my $break = "<br />";
	my $goDown = "\n";
	my $slash = "/";
	
	#nome del corso
	my $course = $informations{"teachingName"};
	utf8::encode($course);
	
	#professore del corso
	my $teacher = "";
	if (length($informations{"teacher"}) < 5) {
		$teacher = "In Attesa di Assegnazione";
	}
	else {
		my $tytle = substr($informations{"teacher"}, 0, index($informations{"teacher"}, " "));
		if ($tytle eq "Prof.") {
			$tytle = "<abbr title=\"Professor\">$tytle</abbr>";
		}
		if ($tytle eq "Prof.ssa") {
			$tytle = "<abbr title=\"Professoressa\">$tytle</abbr>";
		}
		if ($tytle eq "Dott.") {
			$tytle = "<abbr title=\"Dottor\">$tytle</abbr>";
		}
		if ($tytle eq "Dott.ssa") {
			$tytle = "<abbr title=\"Dottoressa\">$tytle</abbr>";
		}
		$teacher = $tytle . substr($informations{"teacher"}, index($informations{"teacher"}, " "));
	}
	
	utf8::encode($teacher);
	
	# numero CFU del corso
	my $CFU = $informations{"CFU"};
	my $curriculum = $informations{"curriculum"};
	
	#recupero informazioni sul periodo di svolgimento del corso
	my %periodInformations = %{$informations{"period"}};
	my $year = $periodInformations{"anno"};
	my $period = $periodInformations{"trimestre"};
	
	my $beginning = $periodInformations{"inizio"};
	#trasformo la stringa del periodo in gg/mm/aaaa
	$beginning = substr($beginning, 8, 2) . "/" . substr($beginning, 5, 2) . "/" . substr($beginning, 0, 4);
	
	my $end = $periodInformations{"fine"};
	#trasformo la stringa del periodo in gg/mm/aaaa
	$end = substr($end, 8, 2) . "/" . substr($end, 5, 2) . "/" . substr($end, 0, 4);
	
	my %courseDescription = %{$informations{"informations"}};
	
	
	#programma del corso
	my $courseProgram = $courseDescription{"programmacorso"};
	$courseProgram =~ s/\&/\&amp;/g;
	$courseProgram =~ s/</\&lt\;/g;
	$courseProgram =~ s/>/\&gt\;/g;
	#sostituisco eventuali \n con tag html <br />
	$courseProgram =~ s/$goDown/$break/g;
	utf8::encode($courseProgram);
	
	
	my $prerequisites = $courseDescription{"prerequisiti"};
	$prerequisites =~ s/\&/\&amp;/g;
	$prerequisites =~ s/</\&lt\;/g;
	$prerequisites =~ s/>/\&gt\;/g;
	#sostituisco eventuali \n con tag html <br />
	$prerequisites =~ s/$goDown/$break/g;
	if (length($prerequisites) < 5) {
		$prerequisites = "- -";  #se non c'è scritto nulla o se la stringa inserita è --, uniformo per tutti a - -
	}
	utf8::encode($prerequisites);
	
	my $propedeuticities = $courseDescription{"propedeuticita"};
	$propedeuticities =~ s/\&/\&amp;/g;
	$propedeuticities =~ s/</\&lt\;/g;
	$propedeuticities =~ s/>/\&gt\;/g;
	#sostituisco eventuali \n con tag html <br />
	$propedeuticities =~ s/$goDown/$break/g;
	if (length($propedeuticities) < 5) {
		$propedeuticities = "- -";  #se non c'è scritto nulla o se la stringa inserita è --, uniformo per tutti a - -
	}
	utf8::encode($propedeuticities);
	
	
	my $didatticHelps = $courseDescription{"ausilididattici"};
	$didatticHelps =~ s/\&/\&amp;/g;
	$didatticHelps =~ s/</\&lt\;/g;
	$didatticHelps =~ s/>/\&gt\;/g;
	#sostituisco eventuali \n con tag html <br />
	$didatticHelp =~ s/$goDown/$break/g;
	if (length($didatticHelp) < 5) {
		$didatticHelps = "- -";  #se non c'è scritto nulla o se la stringa inserita è --, uniformo per tutti a - -
	}
	utf8::encode($didatticHelps);
	
	
	my $books = $courseDescription{"testididattici"};
	$books =~ s/\&/\&amp;/g;
	$books =~ s/</\&lt\;/g;
	$books =~ s/>/\&gt\;/g;
	$books =~ s/$goDown/$break/g;
	utf8::encode($books);
	
	my %hours = %{$informations{"hours"}};
	my $frontalHour = $hours{"ore_frontali"};
	my $laboratoryHour = $hours{"ore_lab"};
	my $exerciseHour = $hours{"ore_esercizi"};
	
	my $siteLink = &getCourseSiteMagistrale($course);
	
	my $textPage = &openFile($sitePath . "laureamagistrale/corsitemplate$en.html");
	
	#sostiuisco "nomeCorso" con il nome del corso
	$textPage =~ s/"nomeCorso"/$course/g; 
	
	#da qui in poi inserisco le informazioni di ogni singolo corso, sostituendo nell'apposito tag inserito nella pagina di template
	$textPage =~ s/<numCFU\/>/$CFU/;
	$textPage =~ s/<teacher\/>/$teacher/;
	$textPage =~ s/<anno\/>/$year/;
	$textPage =~ s/<trimestre\/>/$period/;
	$textPage =~ s/<inizio\/>/$beginning/;
	$textPage =~ s/<fine\/>/$end/;
	$textPage =~ s/<curriculum\/>/$curriculum/;
	$textPage =~ s/<oreFrontali\/>/$frontalHour/;
	$textPage =~ s/<oreLaboratorio\/>/$laboratoryHour/;
	$textPage =~ s/<oreEsercizi\/>/$exerciseHour/;
	$textPage =~ s/<programmaCorso\/>/$courseProgram/;
	$textPage =~ s/<prerequisiti\/>/$prerequisites/;
	$textPage =~ s/<propedeuticita\/>/$propedeuticity/;
	$textPage =~ s/<ausiliDidattici\/>/$didatticHelps/;
	$textPage =~ s/<testiRiferimento\/>/$books/;
	$textPage =~ s/<linkAlSito\/>/$siteLink/;
	
	my $fileName = $informations{"teachingName"};
	$fileName = encode_entities($fileName);
	#elimino accenti o eventuali altre entità html per costruire il nome della pagina
	$fileName =~ s/&agrave;/a/g;
	$fileName =~ s/&Agrave;/a/g;
	$fileName =~ s/&atilde;/a/g;
	$fileName =~ s/&Atilde;/a/g;
	$fileName =~ s/&Nbsp;//g;
	$fileName =~ s/&nbsp;//g;
	$fileName =~ s/'//g;
	$fileName =~ s/&.+;//g;
	
	#metto tutto in lowercase
	$fileName = lc($fileName);
	
	#elimino eventuali spazi
	$fileName =~ s/ //g; 
	
	$fileName .= "$en.html";
	my $otherLanguage  = $fileName;
	my $courseTemplate = "corsitemplate.html";
	
	if ($en eq "en") {
		$otherLanguage =~ s/en.html/.html/g;
	}
	else {
		$otherLanguage =~ s/.html/en.html/g;
		$courseTemplate =~ s/.html/en.html/g;
	}
	
	$textPage =~ s/$courseTemplate/$otherLanguage/g;
	#utf8::encode($textPage);
		
	&createFile($sitePath . "laureamagistrale/$fileName", $textPage);

	print "Page Course Created Magistrale: $fileName\n";
	return $fileName;
}

1;
