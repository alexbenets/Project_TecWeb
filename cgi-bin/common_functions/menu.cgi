#!/usr/bin/perl
package menu;

require      Exporter;
require 'common_functions/Session.cgi';
my @ISA       = qw(Exporter);
my $VERSION   = 1.00;         # Version number

use Time::Piece;
use CGI::Carp qw(fatalsToBrowser);
use strict;


#funzioni base
my $trovato;
sub add{
	my ($titolo, $pagina)=@_;
	my $pagina_sessione=gestione_sessione::getParam("location");
	$pagina_sessione=~/..\/([a-zA-Z0-9.]+)/;
	$pagina_sessione=$1;
	my $selezionato=($pagina eq $pagina_sessione)?1:0;
	if($selezionato==0){
		$selezionato=($pagina eq gestione_sessione::getParam("location"))?1:0;
	}
	my @temp=($titolo, $pagina, $selezionato);
	if($selezionato==1){
		$trovato=1;
	}
	return \@temp;
}

sub get{
	my ($ignora)=@_;
	
	my @menu_temp;
	my $create=gestione_sessione::createSession();
	if($ignora eq ''){
		$ignora=0;
		push @menu_temp, add("Home", "index.cgi"); 
	}else{
		$ignora=1;
		
		push @menu_temp, add("Home", "index.html"); 
	}
	if(($trovato==0) and (int($ignora)==0)){
		my $pagina_sessione=gestione_sessione::getParam("location");
		$pagina_sessione=~/([a-zA-Z0-9_]+).cgi/;
		my $titolo=$1;
		$pagina_sessione=~/([a-zA-Z0-9.]+)/;
		$pagina_sessione=$1;
		$titolo =~ s/_/ /;
		if(!($pagina_sessione eq "") and !((gestione_sessione::getParam("location") eq "utente.cgi"))){
			if(!(gestione_sessione::getParam("location") eq "login.cgi")){
				push @menu_temp,add($titolo,gestione_sessione::getParam("location"));
			}
		}
	}
	my $logged=gestione_sessione::getParam("logged");
	if(($logged==1) and ($ignora==0)){
		push @menu_temp, add("Area utente", "utente.cgi");
	}
	push @menu_temp, add("Compagnia", "../compagnia.html");
	push @menu_temp, add("Servizi", "../servizi.html");
	
	if((gestione_sessione::getParam("admin")==1)and ($ignora==0) and !(gestione_sessione::getParam("location") eq "admin.cgi")){
		push @menu_temp, add("Amministrazione", "admin.cgi");
	}
	
	if(($logged==1) and ($ignora==0)){
		push @menu_temp, add("Logout", "login.cgi?logout=1");
	}else{
		if($ignora==0){
			push @menu_temp, add("Login", "login.cgi");
		}else{
			push @menu_temp, add("Login", "cgi-bin/login.cgi");#per la parte statica
		}
	}
	return \@menu_temp;
}

1;