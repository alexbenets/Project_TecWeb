#!/usr/bin/perl
package database;

use XML::XPath;
use XML::XPath::XMLParser;
require      Exporter;

my @ISA       = qw(Exporter);
my $VERSION   = 1.00;         # Version number


use CGI::Carp qw(fatalsToBrowser);
use strict;

sub get{
	my ($xpath)=@_;
	my $xp = XML::XPath->new(filename => 'database.xml');
	return $xp->find($xpath); # find all paragraphs
	
}

sub set{
}

sub listServizi{
	my @servizi;
	my $lista_servizi=get('/database/tabServizio/servizio');
	foreach my $servizio ($lista_servizi->get_nodelist){
		my $id_servizio=$servizio->getAttribute("idS");
		my $nome_servizio=$servizio->find("nome");
		my $descrizione=$servizio->find("descrizione");
		my $costo=$servizio->find("prezzo");
		my @temp=($id_servizio, $nome_servizio, $costo, $descrizione);
		push @servizi,\@temp;
	}
	return \@servizi;
}

sub listTratte{


#funzionamento: 
#creo array associativo {ID, valore} di Nazione
#per ogni ID Nazione, mi creo l'array associativo di città
#per ogni città, mi creo l'array associativo degli aereoporti



	#my @aereoporti_temp=("Linate", "Malpensa");
	#my %temp;
	
	#$temp{"Milano"}=\@aereoporti_temp;
	
	#my @aereoporti_temp=("Fiumicino");
	#$temp{"Roma"}=\@aereoporti_temp;
	#$partenze {"Italia"}=\%temp;
	
	#my @aereoporti_temp=( "Charles de gaulle");
	#	my %temp;
	#	$temp{"Parigi"}=\@aereoporti_temp;
	#	$partenze {"Francia"}=\%temp;
	

#mi genero l'array delle tratte
my %partenze;
my $nazioni_get= get('/database/tabNazione/nazione');
foreach my $node ($nazioni_get->get_nodelist) {
        my $id=$node->getAttribute("idN");
        my $nome_nazione=$node->find('nome');
        my $citta=get('/database/tabCitta/citta[@idN='.$id.'][flagServita="true"]');
        my %citta_temp;
        my $count_stato=0;
        foreach my $node_citta($citta->get_nodelist){
        	my $count_citta=0;
        	my $id_citta= $node_citta->getAttribute("idC");
        	my $nome_citta= $node_citta->find('nome');
        	my $aereoporti=get('/database/tabAereoporto/aereoporto[@idC='.$id_citta.'][flagAttivo="true"]');
        	my @aereoporti_temp;
        	foreach my $aereoporto($aereoporti->get_nodelist){
        		$count_stato++;
        		$count_citta++;
        		my $id_aereoporto=$aereoporto->getAttribute("idAp");
        		my $nome_aereoporto=$aereoporto->find('nome');
        		#print "<p>$nome_nazione: $nome_citta - $nome_aereoporto</p>";
        		push @aereoporti_temp, $nome_aereoporto;
        	}
        	if($count_citta>0){#se esistono aereoporti nella città
        		$citta_temp{"$nome_citta"}=\@aereoporti_temp;
        	}
        }
        if($count_stato>0){#se esistono aereoporti nello stato
        	$partenze {"$nome_nazione"}=\%citta_temp;
        }
}
#foreach my $node ($nazioni_get->get_nodelist) {
#	print $node;
#}
return %partenze;

}