#!/usr/bin/perl

use utf8;

binmode STDIN, ":utf8";
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";

#parametri: 
#    $_[0] - se la pagina è l'home page o meno
#    $_[1] - discriminante se voglio footer inglese o italiano

sub createFooter() {
	
	my $en = $_[1];
	
	my $footerText = '<div id="contatore"><script type="text/javascript">document.write(unescape("%3Cscript src=%27http://s10.histats.com/js15.js%27 type=%27text/javascript%27%3E%3C/script%3E"));</script>
<a href="http://www.histats.com" title="contatore utenti connessi"><script  type="text/javascript" >
try {Histats.start(1,1189861,4,0,0,0,"00010000");
Histats.track_hits();} catch(err){};
</script>Contatore</a></div>';
	
	#aprop pagina contenente il footer
	$footerText .= &openFile("../pagesSource/globalDetails/footer$en.html"); #estratto contenuto del footer
	
	#nel caso in cui questa pagina sia l'home page, cambio i link
	if ($_[0]) {
	
		my $pathSRC = "src=\"../";  #path di default per i link indicati da src
		my $pathHREF = "href=\"../"; #path di default per i link indicati da href 
		$footerText =~ s/$pathSRC/src="/g; 
		$footerText =~ s/$pathHREF/href="/g; 
	
	}
	
	return $footerText;
}

1;
