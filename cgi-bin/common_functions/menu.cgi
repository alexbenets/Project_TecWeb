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
	my @temp=($titolo, $pagina, $selezionato);
	if($selezionato==1){
		$trovato=1;
	}
	return \@temp;
}

sub get{
	my $create=gestione_sessione::createSession();
	
	my @menu_temp;
	push @menu_temp, add("Home", "index.cgi"); 
	if($trovato==0){
		my $pagina_sessione=gestione_sessione::getParam("location");
		$pagina_sessione=~/..\/([a-zA-Z0-9_]+).cgi/;
		my $titolo=$1;
		$pagina_sessione=~/..\/([a-zA-Z0-9.]+)/;
		$pagina_sessione=$1;
		$titolo =~ s/_/ /;
		if(!($pagina_sessione eq "")){
			push @menu_temp,add($titolo,$pagina_sessione);
		}
	}
	my $logged=gestione_sessione::getParam("logged");
	if($logged==1){
		push @menu_temp, add("Area utente", "utente.cgi");
	}
	push @menu_temp, add("Storia", "storia.cgi");
	return \@menu_temp;
}

1;