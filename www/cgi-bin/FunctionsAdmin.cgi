#!/usr/bin/perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use utf8;

#file contenente le funzioni per la parte di amministrazione per l'area riservata, quindi nuovo utente,
#assegnazione permessi, rimozione...

$fileXML .= "UserPermission.xml";

#inserisce un nuovo utente nel file XML, al quale sarà possibile poi associare dei permessi
sub insertNewUser() {
	
	eval {
	
		#parametro in ingresso HASH contentente le informazioni del nuovo utente
		my %input = %{$_[0]};
		
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileXML);
		my $root = $document->getDocumentElement;
		
		#creo un nuovo ID per il nuovo utente
		my $newID = $root->findvalue("//TableUser/User[last()]/ID");
		if ($newID eq "") {
			$newID = 0;
		}
		$newID = $newID + 1;
		
		#recupero tabella Utenti
		my $tableUser = $root->find("//TableUser")->get_node(1);
		
		#creo stringa del nodo
		my $newUserString = 
		"<User>
			<ID>$newID</ID>
			<Name>$input{'name'}</Name>
			<Surname>$input{'surname'}</Surname>
			<UserID>$input{'userID'}</UserID></User>";
			
		#converto stringa in nodo ed aggiungo al file
		my $newNode = $parser->parse_balanced_chunk($newUserString);
		$tableUser->addChild($newNode);
	
		open(FILE, ">$fileXML") || die("Non riesco ad aprire il file");
		print FILE $document->toString();
		close(FILE);
		
		return 1;
	}
	or do { return 0; }
}

#restituisce l'elenco dei permessi come <option>
#due possibilità: o tutti i permessi (per associazione) o i permessi di un utente (per eliminazione)
sub getPermissions() {
	
	eval {
		#parametro in ingresso eventuale ID dell'utente
		my $userID = $_[0];
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileXML);
		my $root = $document->getDocumentElement;
		
		my $permissionList;
		
		#voglio averel semplicemente l'elenco dei permessi
		if ($userID eq "") {
			$permissionList = $root->findnodes("//TablePermission/Permission");
		}
		#voglio permessi associati ad un determinato utente
		else {
			$permissionList = $root->findnodes("//TableUserPermissions/UserPermission[UserID=$userID]/IDPermission");	
		}
		my $stringHTML = "";
		
		#creo lista di <option>, dove il valore identificativo in value è l'ID del permesso
		foreach my $permission ($permissionList->get_nodelist) {
			
			my $permissionID = $permission->textContent;
			$stringHTML .= "<option value=\"$permissionID\">$permissionID</option>";
		}
		
		return $stringHTML;
	}
	or do { return ""; }
	
}

#restituisce gli utenti registrati sotto forma di lista di <option>
sub getUsers() {
	
	eval {
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileXML);
		my $root = $document->getDocumentElement;
		
		#recupero elenco User registrati
		my $userList = $root->findnodes("//TableUser/User");
		
		my $stringHTML = "";
		
		#per ogni utente recupero informazioni
		#valore identificativo in value è l'ID dell'utente
		foreach my $user ($userList->get_nodelist) {
			
			my $userID = $user->findvalue('ID');
			my $userName = $user->findvalue('Name');
			my $userSurname = $user->findvalue('Surname');
			my $userNick = $user->findvalue('UserID');
			
			
			$stringHTML .= "<option value=\"$userID\">$userName $userSurname ($userNick)</option>";
		}
		
		return $stringHTML;
	}
	or do { return ""; }
	
}

#elimina un utente dal file XML, più tutti gli eventuali permessi ad esso associati
sub deleteUser() {
	
	eval {
	
		#parametro di ingresso l'ID dell'utente
		my $userID = $_[0]; 	
		
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileXML);
		my $root = $document->getDocumentElement;
		
		#recupero nodo dell'utente da eliminare sull base del suo ID
		my $userNode = $root->find("//TableUser/User[ID=$userID]")->get_node(1);
		#recupero il padre del nodo ed elimino il nodo
		my $parent = $userNode->parentNode;
		$parent->removeChild($userNode);
		
		#recupero l'insieme dei permessi associati a quel determinato utente
		my $userPermissions = $root->find("//TableUserPermissions/UserPermission[UserID=$userID]");
		
		#per ogni nodo che indica un permesso associato all'utente, recupero il padre del nodo e lo elimino
		foreach $permission ($userPermissions->get_nodelist) {
			
			$parent = $permission->parentNode;
			$parent->removeChild($permission);
			
		}
		
		open(FILE, ">$fileXML") || die("Non riesco ad aprire il file");
		print FILE $document->toString();
		close(FILE);
		
		return 1;
	}
	or do { return 0; }
	
}

#assegna un permesso ad un utente
sub assignPermission() {
	
	eval {
		#parametri di ingresso: ID dell'utente e ID del permesso
		my $userID = $_[0];
		my $permissionID = $_[1];
	
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileXML);
		my $root = $document->getDocumentElement;
		
		#verifico che il nuovo permesso che si vuole assegnare non sia in realtà già assegnato
		my $actual = $root->findvalue("//TableUserPermissions/UserPermission[IDPermission=\"$permissionID\" and UserID=$userID]/IDPermission");
		
		#se il valore di $actual è diverso dalla stringa vuota, significa che l'utente ha già assegnato quel determianto permesso
		if ($actual ne "") {
			return "Permesso già assegnato";
		}
		
		#verifico che l'utente al quale si vuole assegnare il permesso non sia in realtà un amministratore, che ha già tutti i permessi	
		my $admin = $root->findvalue("//TableUserPermissions/UserPermission[IDPermission=\"Admin\" and UserID=$userID]/IDPermission");
		
		if ($admin ne "") {
			return "L'utente è amministratore";
		}
		
		#nel caso in cui il permesso che si vuole assegnare sia Admin, elimino tutti i permessi assegnati precedentemente
		#perchè l'amministratore ha tutti i permessi
		if ($permissionID eq "Admin") {
			
			#recupero i nodi che indicano un eventuale permesso già assegnato all'utente
			my $permissionsList = $root->find("//TableUserPermissions/UserPermission[UserID=$userID]");
			
			foreach $permission ($permissionsList->get_nodelist) {
				my $parent = $permission->parentNode;	
				$parent->removeChild($permission);
				
			}
		}
		
		#inserisco nuovo permesso
		my $newStringNode = 
		"<UserPermission>
			<IDPermission>$permissionID</IDPermission>
			<UserID>$userID</UserID></UserPermission>";
			
		my $newNode = $parser->parse_balanced_chunk($newStringNode);
		my $tableUserPermissions = ($root->find("//TableUserPermissions"))->get_node(1);
		
		$tableUserPermissions->addChild($newNode);
		
		open(FILE, ">$fileXML") || die("Non riesco ad aprire il file");
		print FILE $document->toString();
		close(FILE);
		
		return "Inserimento Avvenuto";
	}
	or do {
		return "Operazione non completata. Riprovare"; 
	}
}	

#elimina un permesso associato ad un utente
sub deletePermission() {
	
	eval {
		#parametri di ingresso: ID dell'utente e l'ID del permesso da eliminare
		my $userID = $_[0];
		my $permissionID = $_[1];
	
		my $parser = XML::LibXML->new();
		
		my $document = $parser->parse_file($fileXML);
		my $root = $document->getDocumentElement;
		
		#recupero il nodo che indica il permesso
		#sono sicuro di trovarlo perchè permetto di eliminare ad un utente solamente i permessi ad esso associati
		my $permission = $root->find("//TableUserPermissions/UserPermission[IDPermission=\"$permissionID\" and UserID=$userID]")->get_node(1);
		
		my $parent = $permission->parentNode;
		$parent->removeChild($permission);
		
		open(FILE, ">$fileXML") || die("Non riesco ad aprire il file");
		print FILE $document->toString();
		close(FILE);
		
		return 1;
	}
	or do { return 0; }
	
}


