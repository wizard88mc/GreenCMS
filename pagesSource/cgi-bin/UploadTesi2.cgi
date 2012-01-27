#!/usr/bin/perl -w

$|++; 

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use HTML::Entities;
use utf8;
use CGI::Ajax;

binmode STDIN, ":utf8";
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";


my $Upload_Dir = "/var/www/private/tesimagistrale"; 

my $pjx = new CGI::Ajax('check_status' => \&check_status);
my $q   = CGI->new(\&hook);

my $pjx = new CGI::Ajax('check_status' => \&check_status);
my $q   = CGI->new(\&hook);

sub hook {
            
    my ($filename, $buffer, $bytes_read, $data) = @_;
    
    $bytes_read ||= 0; 
          
    open(COUNTER, ">" . $Upload_Dir . '/' . $filename . '-meta.txt'); 
    
    my $per = 0; 
    if($ENV{CONTENT_LENGTH} >  0){ # This *should* stop us from dividing by 0, right?
        $per = int(($bytes_read * 100) / $ENV{CONTENT_LENGTH});
    }
    print COUNTER $per;
    close(COUNTER); 
     
}

my $init_rand_string = 0; 
if(!$q->param('process')){ 
    $init_rand_string = generate_rand_string(); 
}

my $d = <<EOF
 
<html>
    <head>
    </head>
    <body>
        <form name="default_form" enctype="multipart/form-data" method="post">
            <p>
                <input type="file" name="uploadedfile" />
            </p>
            <input type="hidden" name="yes_upload" value="1" />
            <input type="hidden" name="process" value="1" />
            <input type="hidden" name="rand_string" id="rand_string" value="$init_rand_string" />
            <p>
                <input type="submit" value="upload." />
            </p>
<script language="Javascript"> 
    setInterval("check_status(['check_upload__1', 'rand_string', 'uploadedfile'], ['statusbar']);",'1000')
</script> 
            <div id="statusbar">
            </div>
    </body>
</html>

EOF
; 

my $outfile = $Upload_Dir . '/' . $q->param('rand_string') . '-' . $q->param('uploadedfile');
my $p = <<EOF

<html>
    <head>
    </head>
    <body>
        <h1>
            Done!: 
        </h1>
        <hr /> 
        <p> 
         $outfile
        </p>
    </body>
</html>

EOF
; 

main(); 

sub main { 

    if($q->param('process')){ 
        if($q->param('yes_upload')) { 
            upload_that_file($q); 
        }   
        print $q->header(); 
        print $p; 
        dump_meta_file();   
    }
    else {         
        print $pjx->build_html( $q, $d);
    }
}


sub upload_that_file { 

    my $q = shift; 
    
    my $fh       = $q->upload('uploadedfile');
    my $filename = $q->param('uploadedfile');
    
    return '' if ! $filename; 
    
    my $outfile = $Upload_Dir . '/' . $q->param('rand_string') . '-' . $q->param('uploadedfile');
    
    open (OUTFILE, '>' . $outfile) 
        or die("can't write to " . $outfile . ": $!");        
    
    while (my $bytesread = read($fh, my $buffer, 1024)) { 
        print OUTFILE $buffer; 
    } 
    
    close (OUTFILE);
    chmod(0666, $outfile);  
    
}


sub check_status { 
   
   my $filename = $q->param('uploadedfile');
      $filename =~ s{^(.*)\/}{}; 

    return '' 
        if ! -f  $Upload_Dir . '/' . $filename . '-meta.txt'; 
        
    open my $META, '<', $Upload_Dir . '/' . $filename  . '-meta.txt' or die $!;
    my $s = do { local $/; <$META> };
    close ($META); 
    
   my $small = 500 - ($s * 5); 
   my $big = $s * 5; 
   
    my $r = '<h1>' . $s . '%</h1>'; 
       $r .= '<div style="width:' . $big . 'px;height:25px;background-color:#6f0;float:left"></div>'; 
       $r .= '<div style="width:' . $small . 'px;height:25px;background-color:f33;float:left"></div>';
    return $r; 
    
}


sub dump_meta_file { 
   my $filename = $q->param('uploadedfile');
      $filename =~ s{^(.*)\/}{}; 
    unlink($Upload_Dir . '/' . $filename . '-meta.txt') or warn "deleting meta file didn't work..."; 
}


sub generate_rand_string { 

    my $chars = shift || 'aAeEiIoOuUyYabcdefghijkmnopqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ23456789';
    my $num   = shift || 1024;
    
    require Digest::MD5;
    
    my @chars = split '', $chars;
    my $ran;
    for(1..$num){
        $ran .= $chars[rand @chars];
    }
    return Digest::MD5::md5_hex($ran); 
 }
