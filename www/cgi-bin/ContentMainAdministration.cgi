#!/usr/bin/perl

use utf8;

binmode STDIN, ":utf8";
binmode STDOUT; ":utf8";
binmode STDERR, ":utf8";

require "CreateSecondLevelMenu.cgi";

sub contentMainAdministrator() {

	my $stringSecondLevel = &createSecondLevelMenu();
print <<CONTENT;
<div id="contents-right">
	<div id="utilities">
	$stringSecondLevel;
	</div>
	<div id="contents">
	<h1>Pannello di Amministrazione</h1>
	<p>Benvenuto/a nell'Area riservata . . .<br />
	Alla tua destra troverai il menu con i link che puoi utilizzare 
	a seconda del tuo livello di accesso . . .
	</div>
</div>
CONTENT
}
