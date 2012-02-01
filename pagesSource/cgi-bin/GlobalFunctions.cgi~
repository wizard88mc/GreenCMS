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
        $defaultMonth = localtime->mon() + 1;
    }
    else {
        $defaultMonth = $_[0];
    }
    if ($defaultMonth == 13) {
        $defaultMonth = 1;
    }
    
    my @months = ("Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", 
                  "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre");
    
    my $stringMonthsOptions = "";
    
    for (my $i = 1; $i < 13; $i++) {
        my $checked;
        my $index = $i;
        
        if (length($index) == 1) {
            $index = "0$index";
        }
        
        if ($defaultMonth eq $index) {
            $checked = ' selected="selected"';
        }
        my $arrayIndx = $i - 1;
        
        $stringMonthsOptions .= "<option value=\"$index\"$checked>@months[$arrayIndx]</option>";
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

#verifica se la data inserita è corretta
sub checkCorrectDate() {
    
    my ($day, $month, $year) = &getDateComponentsFromItalianDate($_[0]);
    
    if (($month == "11" or $month == "04" or $month == "06" or $month == "09") and $day == "31") {
           return false;	
	}
	if ($month == "02" && $day > 29) { return false; }
	else { return true; }
}

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

sub getTimeComponents() {
    
    $time = $_[0];
    
    my @components = (substr($time, 0, 2), substr($time,3, 2), substr($time, 6, 2)); 
    return @components;
}

1;
