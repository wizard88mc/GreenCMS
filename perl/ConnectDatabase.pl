#/usr/bin/perl

use DBI;
use DBD::mysql;
use utf8;

binmode STDIN, ":utf8";
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";

sub connectDatabase() {

	my $hostname = "localhost";
	my $port = "3306";
	my $database = "facolta_scienze";
	my $username = "scienze";
	my $password = "Fs-P348!";
	
	my $dsn = "dbi:mysql:$database:$hostname:$port";
	
	my $DBIConnect = DBI->connect($dsn, $username, $password);
	
	return $DBIConnect;
	
}
