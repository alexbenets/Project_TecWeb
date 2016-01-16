#!/usr/bin/perl
package gestione_sessione;

require      Exporter;

my @ISA       = qw(Exporter);
my $VERSION   = 1.00;         # Version number


use CGI::Carp qw(fatalsToBrowser);
use strict;

use CGI qw(:standard);
use CGI;
use CGI::Session;    
use CGI::Cookie;


#utilizzo: createSession(): 
#							- 	crea una nuova sessione, se necessario e restituisce l'ID sessione.
#							- 	aggiorna la scadenza a +2 ore, così da permettere agli utenti di effettuare tutte le operazioni
#								necessarie con tranquillità
#
#destroySession(): elimina la sessione corrente.
#setParam(parametro, valore): imposta il parametro desiderato.
#getParam(parametro): restituisce il parametro desiderato.
#getSessionCookie(): restituisce il valore del cookie di sessione.
#	NON DOVREBBE ESSERE RICHIAMATA ALL'ESTERNO DI QUESTO FILE.
#	SFORTUNATAMENTE PERL NON PERMETTE DI IMPOSTARE LA VISIBILITÀ DEI METODI

sub getSessionCookie{
	my %cookies = CGI::Cookie->fetch;
    if(!defined(%cookies)){
    	return undef;#non c'è nulla da eliminare, visto che non esiste nemmeno il cookie di sessione.
    }
    return $cookies{'SESSION'}->value; #ritorno l'id sessione.
}



sub destroySession{
	
	my $session = CGI::Session->load(getSessionCookie())  or die;
	if(!($session->is_expired | $session->is_empty))
	{
		
		
		$session->delete();
		$session->close();
		$session->flush();
		return 1; #distrutta correttamente
	}
	return 0; #non ho potuto distruggerla per qualche motivo, magari era già scaduta o non esisteva più?
}

sub createSession{#creo una nuova sessione, se non esistente.
	my $id=getSessionCookie();
	my $session = CGI::Session->load($id)  or die;
	if(!($session->is_expired | $session->is_empty)) #se la sessione esiste già, allora ritorno solo l'ID da utilizzare per impostare il cookie di sessione
	{
		return $id;# non ho bisogno di creare una nuova sessione: basta già quella attuale.
	}
	$session = new CGI::Session("driver:File", undef, {Directory=>"/tmp"});
	$session->expire('+2h');
	$session->flush();
	return $session->id();
}

sub setParam{

	my ($nome, $valore)=@_;
	
	my $session = CGI::Session->load(getSessionCookie())  or die;
	if($session->is_expired | $session->is_empty)
	{
		return 0; #salvataggio impossibile, non esiste la sessione!
	} 
	$session->param($nome, $valore);
	return 1;
}
sub getParam{
	
	my ($nome)=@_;
	
	my $session = CGI::Session->load(getSessionCookie())  or die;
	if($session->is_expired | $session->is_empty)
	{
		return undef; #cosa leggo, se non esiste la sessione?
	}
	return $session->param($nome);
	#lettura completata
}

1;