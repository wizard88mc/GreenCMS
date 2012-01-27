#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use CGI::Cookie;
use CGI::Session;
use utf8;

sub createSecondLevelMenu {

	my $stringMenu = "<div id=\"utilities\">";
	
	$page = new CGI;
	%cookies = fetch CGI::Cookie;
	$sessionID = $cookies{'CGISESSIONID'}->value;
	$session = new CGI::Session("drive:File", $sessionID, {Directory=>"/tmp"});
	
	my $stringPermission = $session->param('userPermission');
	
	if (index($stringPermission, "Seminari") != -1 || $stringPermission eq "Admin") {
		$stringMenu .="
<h1>Seminari</h1>
	<ul>
		<li><a href=\"NewSeminary.cgi\">Nuovo Seminario</a></li>
		<li><a href=\"NewMailingList.cgi\">Nuova Mailing List</a></li>
		<li><a href=\"NewContact.cgi\">Nuovo Utente</a></li>
		<li><a href=\"ModifyContact.cgi\">Modifica Utente</a></li>
		<li><a href=\"AssociateMailingContact.cgi\">Associare Utente - Mailing List</a></li>
		<li><a href=\"DeleteSeminar.cgi\">Elimina Seminario</a></li>
		<li><a href=\"DeleteContact.cgi\">Eliminazione Utente</a></li>
		<li><a href=\"DeleteAssociationMailingContact.cgi\">Elimina Contatto da Mailing List</a></li>
		<li><a href=\"DeleteMailingList.cgi\">Eliminazione Mailing List</a></li>
	</ul>";
	}
	
	$stringMenu .= "
<h1>News</h1>
	<ul>
		<li><a href=\"NewNews.cgi\">Nuova News</a></li>
		<li><a href=\"EditNews.cgi\">Modifica News</a></li>
		<li><a href=\"DeleteNews.cgi\">Elimina News</a></li>
	</ul>";
	
	
	if (index($stringPermission, "CCS") != -1 || $stringPermission eq "Admin") {
		$stringMenu .= "
<h1>CCS</h1>
	<ul>
		<li><a href=\"NewCCS.cgi\">Nuovo Verbale CCS</a></li>
		<li><a href=\"ApproveCCS.cgi\">Approva Riunione CCS</a></li>
	</ul>";
	}

	if (index($stringPermission, "Dottorandi") != -1 || $stringPermission eq "Admin") {
	
		$stringMenu .= "
<h1>Dottorandi</h1>
	<ul>
		<li><a href=\"NewPHDStudent.cgi\">Nuovo Dottorando</a></li>
		<li><a href=\"NewSupervisor.cgi\">Nuovo Supervisore</a></li>
		<li><a href=\"NewCycle.cgi\">Nuovo Ciclo</a></li>
		<li><a href=\"EditPHDStudent.cgi\">Modifica Dottorando</a></li>
		<li><a href=\"EditSupervisor.cgi\">Modifica Supervisore</a></li>
		<li><a href=\"EditCycle.cgi\">Modifica Ciclo</a></li>
		<li><a href=\"DeletePHDStudent.cgi\">Elimina Dottorando</a></li>
		<li><a href=\"UpdatePagePHDStudents.cgi\">Aggiorna Pagina Dottorato</a></li>
	</ul>";

	}
	
	$stringMenu .= "
<h1>Documenti</h1>
	<ul>
		<li><a href=\"NewDocument.cgi\">Nuovo Documento</a></li>
		<li><a href=\"DeleteDocument.cgi\">Elimina Documento</a></li>
	</ul>";
	
	if ($stringPermission eq "Admin") {
		$stringMenu .= "
<h1>Amministratore</h1>
	<ul>
		<li><a href=\"NewUser.cgi\">Nuovo Utente</a></li>
		<li><a href=\"DeleteUser.cgi\">Elimina Utente</a></li>
		<li><a href=\"AssignPermission.cgi\">Assegna Privilegi</a></li>
		<li><a href=\"RemovePermission.cgi\">Rimuovi Privilegi</a></li>
	</ul>";
	}
	
	$stringMenu .= "
<h1>Laurea</h1>
	<ul>";
	if ($stringPermission eq "Admin") {
		$stringMenu .= "
		<li><a href=\"ManageUploadTesi.cgi\">Gestione form upload</a></li>
		<li><a href=\"ArchiveLaureaSession.cgi\">Archivia Sessiona Laurea</a></li>";
	}
		$stringMenu .= "<li><a href=\"DownloadThesis.cgi\">Download Tesi</a></li>
	</ul>";
	

	$stringMenu .= "<br /><br />
	<a href=\"Logout.cgi\">Logout</a>
</div>";

	utf8::encode($stringMenu);
	
	return $stringMenu;
}

1;
