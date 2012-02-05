#!/usr/bin/perl

#creates a list oh HTML options for a select element that needs days
sub getDaysOptions() {

    my $defaultDay;
    if (!$_[0]) {
        $defaultDay = localtime->mday();
    }
    else {
        $defaultDay = $_[0];
    }
    my $stringOptionsDays = "";
    
    for ($i = 1; $i <= 31; $i++) {
        my $checked;
        if ($defaultDay == $i) {
            $checked = ' selected="selected"';
        }
        my $valueDay = "$i";
        if (length($valueDay) == 1) {
            $valueDay = "0$valueDay";
        }
        $stringOptionsDays .= "<option value=\"$valueDay\"$checked>$i</option>";   
    }
	
    return $stringOptionsDays;
	
}

#creates a list oh HTML options for a select element that needs months
sub getMonthsOptions() {

    my $defaultMonth;
    if (!$_[0]) {
        $defaultMonth = localtime()->mon();
        $defaultMonth++;
    }
    else {
        $defaultMonth = $_[0];
    }
    
    my @months = ("Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", 
                  "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre");
    
    my $stringMonthsOptions = "";
    
    for ($i = 1; $i < 13; $i++) {
        my $selected = '';
        my $index = $i;
        
        if (length($index) == 1) {
            $index = "0$index";
        }
        
        if ($defaultMonth == $i) {
            $selected = ' selected="selected"';
        }
        my $arrayIndx = $i - 1;
        
        $stringMonthsOptions .= "<option value=\"$index\"$selected>$months[$arrayIndx]</option>";
    }
    
    return $stringMonthsOptions;
    
}

#creates a list oh HTML options for a select element that needs years
sub getYearsOptions() {
    
    my $defaultYear;
    if (!$_[0]) {
        $defaultYear = localtime->year() + 1900;
    }
    else {
        $defaultYear = $_[0];
    }
    my $stringYearsOptions = "";
    my $actualYear = localtime->year() + 1900;
    
    for ($i = 0; $i <= 3; $i++) {
        my $year = $actualYear + $i;
        my $selected = '';
        
        if ($defaultYear == $year) {
            $selected = ' selected="selected"';
        }
        
        $stringYearsOptions .= "<option value=\"$year\"$selected>$year</option>";
    }
    
    return $stringYearsOptions;
}

#prende una data nel formato yyyy-mm-dd e restituisce le componenti (dd, mm, yyyy)
sub getDateComponentsFromDBDate() {
    my $date = $_[0];
    
    my @components = (substr($date, 8, 2), substr($date, 5, 2), substr($date, 0, 4));
    
    return @components;
}

#prende una data nel formato dd/mm/yyyy e restituisce le componenti (dd, mm, yyyy)
sub getDateComponentsFromItalianDate() {
    my $date = $_[0];
    
    my @components = (substr($date, 0, 2), substr($date, 3, 2), substr($date, 6, 4));
    
    return @components;
}

#dates converter from format dd/mm/yyyy to format yyyy-mm-dd
sub convertDateFromItalianToDB() {
    
    my $date = $_[0];
    
    my ($day, $month, $year) = &getDateComponentsFromItalianDate($date);
    
    return $year . "-" . $month . "-" . $day;
    
}

#dates converter from format yyyy-mm-dd to format dd/mm/yyyy
sub convertDateFromDBToItalian() {
    
    my $date = $_[0];
    
    my ($day, $month, $year) = &getDateComponentsFromDBDate($date);
    return $day . "/" . $month . "/" . $year;
}

# restituisce la data attuale nel formato YYYY-MM-DD
sub getCurrentDate() {
    
    my $currentYear = localtime->year() + 1900;
	my $currentMonth = localtime->mon();
	$currentMonth++;
	my $currentDay = localtime->mday();
    
	if (length($currentMonth) == 1) {
        $currentMonth = "0$currentMonth";	
    }
    if (length($currentDay) == 1) {
        $currentDay = "0$currentDay";	
    }
    
    my @currentDate = ($currentYear, $currentMonth, $currentDay);
    return @currentDate;
}

#verifica se la data inserita è corretta
sub checkCorrectDate() {
    
    my ($day, $month, $year) = &getDateComponentsFromItalianDate($_[0]);
    
    if (($month == "11" or $month == "04" or $month == "06" or $month == "09") and $day == "31") {
           return false;	
	}
	if ($month == "02" && $day > 29) { return false; }
	else { return true; }
}

# controlla se due date sono in ordine cronologico corretto, ovvero la seconda 
# dopo la prima, con formato delle date in GG-MM-AAAA
sub checkDatesCronologicallyCorrect() {
    my $start = $_[0];
    my $end = $_[1];
    
    my ($startDay, $startMonth, $startYear) = &getDateComponentsFromItalianDate($start);
    my ($endDay, $endMonth, $endYear) = &getDateComponentsFromItalianDate($end);
    
    my $differenceYear = $endYear - $startYear;
    my $differenceMonth = $endMonth - $startMonth;
    my $differenceDay = $endDay - $startDay;
    
    if (($differenceYear > 0) || 
        ($differenceYear == 0 && $differenceMonth > 0) ||
        ($differenceYear == 0 && $differenceMonth == 0 && ($differenceDay > 0 || $differenceDay == 0))) {
    return true;
        }
        else {
            return false;
        }
        
}

# restituisce ore, minuti e secondi di un orario in formato hh:mm:ss
sub getTimeComponents() {
    
    my $time = $_[0];
    
    my @components = (substr($time, 0, 2), substr($time,3, 2), substr($time, 6, 2)); 
    return @components;
}

# converte i link da segnalink tra parentesi quadre a link html
sub convertLinks() {
    
    my $text = $_[0];
    my $openTagLink = '[link]';
    my $closeTagLink = '[/link]';
    
    my $positionLink = index($text, $openTagLink);
    
    while ($positionLink != -1) {
        
        #posizione di fine del link
        my $endLink = index($text, $closeTagLink, $positionLink);
        
        my $link = substr($text, $positionLink + length($openTagLink), $endLink - $positionLink - length($openTagLink));
        # elimino gli spazi e costruisco link con testo uguale al link
        $link =~ s/ //g;
        $link = "<a href=\"$link\">$link</a>";
        substr($text, $positionLink, $endLink + length($closeTagLink) - $positionLink, $link);

        $positionLink = index($text, $openTagLink, $positionLink + length($link));
    }
    
    return $text;
}

# elimina da una stringa i tag che identificano un link
sub removeLinkTags() {
    
    my $text = $_[0];
    my $openTagLink = '\[link\]';
    my $closeTagLink = '\[/link\]';
    
    $text =~ s/$openTagLink//g;
    $text =~ s/$closeTagLink//g;
    
    return $text;
    
}

1;
