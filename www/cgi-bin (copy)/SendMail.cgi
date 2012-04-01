#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use MIME::Lite::TT::HTML;
use Net::SMTP;
use utf8;

use Time::Zone;

sub retrieveDate{
	#recupero giorno, mese, anno e giorno della settimana
        my ($min, $oggi, $anno, $mese, $stringaData);
        my (@lt) = ();

        @lt     = localtime();
        
        # Estrae il minuto attuale
        $min = @lt[1];
        # Estrae il giorno della settimana a tre lettere
        $oggi = (Sun,Tue,Wed,Thu,Fri,Sat)[$lt[6]];
        # Estrae l'anno
        $anno = 1900+@lt[5];
        #Estrae il mese
        $mese = (Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov, Dec)[$lt[4]];
        

        $stringaData = $oggi . ", " . $lt[3] . " " . $mese . " " . $anno
             . " " . sprintf("%02d:%02d:%02d", $lt[2], $lt[1], $lt[0] )
            . " +" . sprintf("%02d%02d", (&tz_offset() / 3600), 0);

        return $stringaData;
}


sub sendMail() {
		my %inputs = %{$_[0]};

		$smtp = Net::SMTP->new('smtp.math.unipd.it', 
					Hello => 'informatica.math.unipd.it',
					Timeout => 30,
					Debug => 1,
					);

		$smtp->mail("$inputs{'email'}");
		$smtp->to("$inputs{'emailTo'}");
		$smtp->data();
		$smtp->datasend("MIME-Version: 1.0\n");
		$smtp->datasend("Content-Type: text/plain; charset=UTF-8\n");
		
		$smtp->datasend("From: $inputs{'email'}\n");
		$smtp->datasend("To: $inputs{'emailTo'}\n");
		$smtp->datasend("Date: " . &retrieveDate() . "\n");
		$smtp->datasend("Subject: $inputs{'subject'} \n\n");
		
		$smtp->datasend("$inputs{'message'}");
		$smtp->dataend();
		$smtp->quit;
		
		return "";
	
}

1;
