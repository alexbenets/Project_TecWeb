#!/usr/bin/perl


package registrati_page;
use CGI::Carp qw(fatalsToBrowser);
use strict;

use CGI qw(:standard);
use CGI;



require "common_functions/print_header.cgi";
require "common_functions/print_search.cgi";
require "common_functions/print_content.cgi";
require "common_functions/print_footer.cgi";
require "common_functions/check_form.cgi";
require "common_functions/Session.cgi";
require "common_functions/database.cgi";
require "common_functions/menu.cgi";
require "common_functions/aggiorna_index.cgi";

print CGI::header();#imposto il cookie di sessione
#my ($nome, $cognome, $cf, $nascita, $email, $password)=@_;
#my ($nome_andata, $nome_ritorno, $passeggeri, $data)=@_;
#my ($tratta, $orario_partenza, $prezzo, $attivo,$id)=@_;
#print database::addServizio("Bus navetta","Bus navetta per la stazione dei treni pi&ugrave; vicina", "10", 2);
#my @lista=@{database::listAereoporti("Milano")};
#print scalar(@lista);
#foreach my $tmp (@lista){
#	my @stato=@{$tmp};
#	print "<p>".@stato[0]." - ".@stato[1]."</p>";
#}

#my @tratte=@{database::getTratta()};
#foreach my $tratta (@tratte){
#	my @tmp=@{$tratta};
#	my $testo="@tmp[0]: @tmp[1] - @tmp[2], @tmp[3] minuti";
#	$testo =~/([0-9]+)([\s:\s])([a-zA-Z\s]+)([\s-\s])([a-zA-Z\s]+)([,])([\s]*)([0-9]+)/;
#	print "<p>$testo</p><p>$1, $3, $5, $8</p>";
#}


aggiorna_index::aggiorna();

#print print_search::print();
#print $casella;
#my @tmp=@{check_form::regexp_data("1/2/2016")};
#print "@tmp[0]/@tmp[1]/@tmp[2]";
#my @voli=@{database::getVoli()};
#foreach my $volo (@voli){
#	my @v=@{$volo};
	#$id_volo,
	#		$orario,
	#		$aereoporto_partenza,
	#		$aereoporto_arrivo
#	print "<p>id:@v[0] ora partenza: @v[1], partenza: @v[2] arrivo: @v[3]</p>";
#}
#print database::addStato("Francia", 2);

#print database::getTratta("Malpensa", "Fiumicino");

#print database::removeServizio(2);
#print database::aggiornaUtente(1,"Nome", "Cognome", "CF", "nascita", "password", "nuova password");
#	my ($id, $nome, $cognome, $cf, $nascita, $password, $nuova_password)=@_;
#my @prenotazioni=@{database::getPrenotazioni(3)};

#my @temp=($id, $posti_occupati, "T$tratta"."V$id_volo", $aereoporto_partenza,$aereoporto_arrivo,$data_prenotazione, $data_partenza, $ora_partenza, $prezzo, $bagagli, \@servizi_prenotati); 

#foreach 
#print scalar(@prenotazioni);
#(//citta[@idC=(//aereoporto[@idAp=(//tratta[@idT=3]/@idApP)]/@idC)]/nome) |
#| (//aereoporto[@idAp=(//tratta[@idT=3]/@idApA)]/nome)
#print database::get('(//citta[@idC=(//aereoporto[@idAp=(//tratta[@idT=3]/@idApP)]/@idC)])/nome')." ".database::get('//aereoporto[@idAp=(//tratta[@idT=3]/@idApP)]/nome');
#print database::salvaServizio(1,2);