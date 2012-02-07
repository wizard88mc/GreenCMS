#!/usr/bin/perl

sub updateFormTags() {
    
    # pagina che contiene il tag con il valore attuale della form
    my $pathToPage = 'laureamagistrale/uploadtesi.html';
    my $pageUpload = $sitePath . '/' . $pathToPage;
    
    my $pageUploadString = &openFile($pageUpload);
    
    my $pageSourceUploadTesi = '../pagesSource/laureamagistrale/source/uploadtesi.html';
    my $pageSourceUploadTesiEn = '../pagesSource/laureamagistrale/source/uploadtesien.html';
    my $pageSourceString = &openFile($pageSourceUploadTesi);
    my $pageSourceStringEn = &openFile($pageSourceUploadTesiEn);
    
    # definisco i tag di form aperta o chiusa
    my $formUploadOpened = '<formUploadTesi/>';
    my $formUploadClosed = '<formNonAttiva/>';
    
    if (index($pageUploadString, $formUploadOpened) != -1) {
        
        # se all'interno del sorgente ho form chiusa, sostituisco con tag 
        # di form aperta
        if (index($pageSourceString, $formUploadClosed) != -1) {
            $pageSourceString =~ s/$formUploadClosed/$formUploadOpened/g;
            $pageSourceStringEn =~ s/$formUploadClosed/$formUploadOpened/g;
            &createFile($pageSourceUploadTesi, $pageSourceString);
            &createFile($pageSourceUploadTesiEn, $pageSourceStringEn);
        }
    }
    # form è chiusa, devo verificare che sia chiusa anche nei sorgenti
    else {
        
        if (index($pageSourceString, $formUploadOpened) != -1) {
            $pageSourceString =~ s/$formUploadOpened/$formUploadClosed/g;
            $pageSourceStringEn =~ s/$formUploadOpened/$formUploadClosed/g;
            &createFile($pageSourceUploadTesi, $pageSourceString);
            &createFile($pageSourceUploadTesiEn, $pageSourceStringEn);
        }
        
    }
    
    # prendo in considerazione ora la form di upload delle presentazioni 
    $pathToPage = 'laureamagistrale/uploadpresentazioni.html';
    $pageUpload = $sitePath . '/' . $pathToPage;
    
    $pageUploadString = &openFile($pageUpload);
    
    my $pageSourceUploadPresentazione = '../pagesSource/laureamagistrale/source/uploadpresentazioni.html';
    my $pageSourceUploadPresentazioneEn = '../pagesSource/laureamagistrale/source/uploadpresentazionien.html';
    
    $pageSourceString = &openFile($pageSourceUploadPresentazione);
    $pageSourceStringEn = &openFile($pageSourceUploadPresentazioneEn);
    
    $formUploadOpened = '<formUploadPresentation/>';
    
    if (index($pageUploadString, $formUploadOpened) != -1) {
        
        # se all'interno del sorgente ho form chiusa, sostituisco con tag 
        # di form aperta
        if (index($pageSourceString, $formUploadClosed) != -1) {
            $pageSourceString =~ s/$formUploadClosed/$formUploadOpened/g;
            $pageSourceStringEn =~ s/$formUploadClosed/$formUploadOpened/g;
            &createFile($pageSourceUploadPresentazione, $pageSourceString);
            &createFile($pageSourceUploadPresentazioneEn, $pageSourceStringEn);
        }
    }
    # form è chiusa, devo verificare che sia chiusa anche nei sorgenti
    else {
        if (index($pageSourceString, $formUploadOpened) != -1) {
            $pageSourceString =~ s/$formUploadOpened/$formUploadClosed/g;
            $pageSourceStringEn =~ s/$formUploadOpened/$formUploadClosed/g;
            &createFile($pageSourceUploadPresentazione, $pageSourceString);
            &createFile($pageSourceUploadPresentazioneEn, $pageSourceStringEn);
        }
        
    } 
}

1;
