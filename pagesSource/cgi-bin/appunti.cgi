foreach my $userMailing ($usersMailing->get_nodelist) {
		
		my $contactID = $userMailing->findvalue('IDContact');
	
		my $contact = $root->find("//TableContact/Contact[ID=$contactID]")->get_node(1);
		my $contactEmail = $contact->findvalue('Email') . "\n";
		
		my $msg = MIME::Lite::TT::HTML->new( 
			From        =>  'mciman@studenti.math.unipd.it',
			To          =>  'wizard88mc@gmail.com', 
			Subject     =>  'Nuovo Seminario', 
			Template    =>  {
           	   html    =>  'test.html',
           	   text 	=> 'test.txt',
           	},
           	Charset     => 'utf8',
           	TmplOptions =>  \%options, 
           	TmplParams  =>  \%params, 
           	); 
	
        $msg->send;
	
	}
	
	my $sendmail = "/usr/sbin/sendmail -t";
	my $reply_to = "Reply-to: mciman\@studenti.math.unipd.it\n";
	my $subject = "Subject: Nuovo Seminario\n";
	my $content = "Messaggio di prova.";
	my $send_to = 'To: wizard88_mc@yahoo.it';
	
	open(SENDMAIL, "|$sendmail") or die "Cannot open $sendmail: $!";
	print SENDMAIL $reply_to;
	print SENDMAIL $subject;
	print SENDMAIL $send_to;
	print SENDMAIL "Content-type: text/plain\n\n";
	print SENDMAIL $content;
	close(SENDMAIL);
