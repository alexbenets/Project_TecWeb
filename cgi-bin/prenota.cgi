#!/usr/bin/perl


package seleziona_voli_page;

use strict;
use CGI::Carp qw(fatalsToBrowser);
use CGI qw(:standard);
use CGI;
#use warnings;


require "common_functions/print_header.cgi";
require "common_functions/print_search.cgi";
require "common_functions/print_content.cgi";
require "common_functions/print_footer.cgi";
require "common_functions/check_form.cgi";
require "common_functions/Session.cgi";


sub getServizi
{
	my ($selezionati)=@_;

	my @servizi;
	for (my $i=0; $i<5; $i++){
		#id servizio, nome servizio, costo
		my @servizio=($i, "Servizio: $i", 20+$i);
		push @servizi, \@servizio; 
	}
	return \@servizi;
}

my %form;
foreach my $p (param()) {
    $form{$p} = param($p);
    #print "$p = $form{$p}<br>\n";
}


my $create=gestione_sessione::createSession();
gestione_sessione::setParam("location","/cgi-bin/prenota.cgi");



#dati recuperati dalle variabili di sessione


my $next=0;
if(defined($form{"conferma"} )){
	$next=1;
}
my $logged=gestione_sessione::getParam("logged");
if($next==1){ #se ho selezionato tutti i valori desiderati
	if($logged==1){
		print "Location: checkout.cgi\n\n";
	}else {
		print "Location: login.cgi\n\n";
	}
}

#$andata=0;
#$select_partenza="Milano - Linate";
#$select_arrivo="Roma - Fiumicino";
#$data_partenza="31/01/2016";
#$data_ritorno="28/02/2016";
#$select_passeggeri=2;



my $titolo="Seleziona il tuo volo";



my $session_cookie = CGI::Cookie->new(-name=>'SESSION',-value=>$create,-expires =>  '+2h',);

print CGI::header(-cookie=>$session_cookie);#imposto il cookie di sessione

print "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">
<html xmlns=\"http://www.w3.org/1999/xhtml\">
	<head>
		<link rel=\"stylesheet\" href=\"../style/main.css\" type=\"text/css\" media=\"screen\" charset=\"utf-8\"/>
		<title>$titolo</title>
	</head>
	
	<body>
";

my @menu_temp;
my @menu=("Home", "../index.html", "1");
push @menu_temp, \@menu; 
my @menu=("Home1", "index1.html", "0");
push @menu_temp, \@menu;
my @menu=("Contatti", "../contatti.html", "0");
push @menu_temp, \@menu;

#funzionamento: la funzione riceve un riferimento ad un array di riferimenti di array.
# esempio: RIF_MENU_1=array("Home", "pagina.html", "1"); //Il pulsante avrà il nome "Home", il riferimento a "pagina.html" e sarà selezionato sul CSS.
#          RIF_MENU_1=array("404", "404.html", "0"); //Il pulsante avrà il nome "404", il riferimento a "404.html" e NON sarà selezionato sul CSS.
#
print_header::setMenu(\@menu_temp);

my @path_temp;
my @path=("Home", "index.cgi");
push @path_temp, \@path;
my @path=("Ricerca voli", "search.cgi");
push @path_temp, \@path;
my @path=("Seleziona i voli disponibili", "seleziona_voli.cgi");
push @path_temp, \@path;
my @path=("Inserisci i dati dei passeggeri", "dati_passeggeri.cgi");
push @path_temp, \@path;
my @path=("Seleziona i servizi aggiuntivi", "servizi_aggiuntivi.cgi");
push @path_temp, \@path;
my @path=("Riepilogo prenotazione", "prenota.cgi");
push @path_temp, \@path;
print_header::setPath(\@path_temp);


my $andata=gestione_sessione::getParam("AR");
my $select_partenza=gestione_sessione::getParam("partenza");
my $select_arrivo=gestione_sessione::getParam("arrivo");
my $select_passeggeri=gestione_sessione::getParam("passeggeri");

#sezione variabili inerenti al volo di partenza
my $id_volo_partenza=gestione_sessione::getParam("Andata_id");
my $giorno_partenza=gestione_sessione::getParam("Andata_data");
my $andata_orario_partenza=gestione_sessione::getParam("Andata_partenza");
my $andata_orario_arrivo=gestione_sessione::getParam("Andata_arrivo");
my $andata_prezzo=gestione_sessione::getParam("Andata_prezzo");

#sezione variabili inerenti al volo di ritorno
my $id_volo_ritorno=gestione_sessione::getParam("Ritorno_id");
my $giorno_ritorno=gestione_sessione::getParam("Ritorno_data");
my $ritorno_orario_partenza=gestione_sessione::getParam("Ritorno_partenza");
my $ritorno_orario_arrivo=gestione_sessione::getParam("Ritorno_arrivo");
my $ritorno_prezzo=gestione_sessione::getParam("Ritorno_prezzo");

#sezione variabili inerenti ai passeggeri
my $num_passeggeri=gestione_sessione::getParam("passeggeri");
my @passeggeri;
for(my $i=1; $i<=$num_passeggeri; $i++){
	my $nome=gestione_sessione::getParam("Nome$i");
	my $cognome=gestione_sessione::getParam("Cognome$i");
	my $cf=gestione_sessione::getParam("CF$i");
	my $nascita=gestione_sessione::getParam("nascita$i");
	my @temp=($nome, $cognome, $cf, $nascita);
	push @passeggeri, \@temp;
}

#sezione variabili inerenti ai servizi
my $num_servizi=gestione_sessione::getParam("Numero_servizi");
my @servizi;
for(my $i=0; $i<$num_servizi; $i++){
	my $selezionato=gestione_sessione::getParam("servizio$i");
	my $nome=gestione_sessione::getParam("nome_servizio$i");
	my $prezzo=gestione_sessione::getParam("prezzo_servizio$i");
	my @temp=($selezionato, $nome, $prezzo);
	push @servizi, \@temp;
}


#variabili generali

my $prezzo_biglietti=int($andata_prezzo)+int($ritorno_prezzo);
my $prezzo_servizi=0;
print print_header::print();



print "		<div id=\"main\"><!-- div che contiene tutto il contenuto statico e/o dinamico-->"; #mega div
my $testo='
	<div class="sezione">
		<form action="prenota.cgi" method="post">
			<fieldset>
				<div><!-- div h2 -->
					<h2>Riepilogo della prenotazione</h2>
				</div><!-- fine h2-->
				<div><!-- div partenza -->
					<h3>Partenza:</h3>
					<p>Volo N&deg; '.$id_volo_partenza.'</p>
					<p>Partenza il: '.$giorno_partenza.'</p>
					<p>Alle ore: '.$andata_orario_partenza.'</p>
					<p>Dall\'aereoporto '.$select_partenza.'</p>
					<p>Arrivo alle ore: '.$andata_orario_arrivo.'</p>
					<p>Nell\'aereoporto '.$select_arrivo.'</p>
					<p>
						<a href="search.cgi">modifica le date</a>
					</p>
				</div><!-- fine partenza -->';
if($andata==0){
$testo.='				<div><!-- div ritorno -->
					<h3>Ritorno:</h3>
					<p>Volo N&deg; '.$id_volo_ritorno.'</p>
					<p>Partenza il: '.$giorno_ritorno.'</p>
					<p>Alle ore: '.$andata_orario_partenza.'</p>
					<p>Dall\'aereoporto '.$select_arrivo.'</p>
					<p>Arrivo alle ore: '.$ritorno_orario_arrivo.'</p>
					<p>Nell\'aereoporto '.$select_partenza.'</p>
					<p>
						<a href="search.cgi">modifica le date</a>
					</p>
				</div><!-- fine ritorno -->';
}
$testo.='				<div><!-- div passeggeri -->';
if($num_passeggeri>0){
	$testo.='				<h3>Passeggeri:</h3>
					';

	for(my $i=0; $i<$num_passeggeri; $i++){
		my @temp=@{@passeggeri[$i]};
		$testo.='<div class="nomi_passeggeri"><!-- div per ogni passeggero -->
					<p>Nome: '.@temp[0].'</p>
					<p>Cognome: '.@temp[1].'</p>
					<p>Codice Fiscale: '.@temp[2].'</p>
					<p>Data di nascita '.@temp[3].'</p>
			</div><!-- fine div per ogni passeggero -->
					<p></p>
				';
	}
					
	$testo.='			<p>
						<a href="dati_passeggeri.cgi">modifica i dati dei passeggeri</a>
					</p>	
					';
}else{
	$testo.="	<div>
					<p>(Non si sono passeggeri aggiuntivi)</p>
				</div>";
}
$testo.='				
				</div><!-- fine div passeggeri -->
				<div><!-- div servizi -->
					<h3>Servizi aggiuntivi:</h3>
					';
for(my $i=0; $i<$num_servizi; $i++){
	my @temp=@{@servizi[$i]};
	if(@temp[0]==1){
		$testo.='	<p>'.@temp[1].', prezzo: '.@temp[2].'&euro; </p>';
		$prezzo_servizi+=int(@temp[2]);
	}
}
$testo.='		
				<p>
					<a href="servizi_aggiuntivi.cgi">modifica i servizi aggiuntivi</a>
				</p>	
				</div><!-- fine div servizi -->
				<div><!-- div costi -->
					<h3>COSTO TOTALE:</h3>
					<p>Biglietti: '.$prezzo_biglietti.'&euro; </p>
					<p>Servizi aggiuntivi: '.$prezzo_servizi.'&euro; </p>
					<p></p>
					<h3>Totale: '.($prezzo_biglietti+$prezzo_servizi).'&euro; </h3>
				</div><!-- fine div costi -->
				
				<div>
					<span>
						<a href="index.cgi">ANNULLA</a>
					</span>
					<button type="submit" id="conferma" name="conferma" value="1">
						<span>conferma</span>
					</button>
				</div>
			</fieldset>
		</form>
	</div><!-- chiudo sezione -->
';

print print_content::print($testo);
print "		</div>"; #chiudo il div main
print print_footer::print();
print "	</body>
</html>";