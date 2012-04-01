#!/usr/bin/perl

use DBI;
use DBD::mysql;
use utf8;

sub connectDatabase() {

	my $database = $_[0];
	#parametri di connessione al database
	my $hostname = "127.0.0.1";
	my $port = "3307";
	my $username = "cclinf";
	my $password = "Gaggi.10";
	
	my $dsn = "dbi:mysql:$database:$hostname:$port";
	
	my $DBIConnect = DBI->connect($dsn, $username, $password);
	
	#restituisco la connessione al database creata
	return $DBIConnect;
	
}

1;
