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
require "common_functions/database.cgi";
require "common_functions/menu.cgi";
sub getServizi
{
	return database::listServizi();
}

my %form;
foreach my $p (param()) {
    $form{$p} = param($p);
    #print "$p = $form{$p}<br>\n";
}


my $create=gestione_sessione::createSession();
gestione_sessione::setParam("location","/cgi-bin/prenota.cgi");


my $titolo="Seleziona il tuo volo";



my $session_cookie = CGI::Cookie->new(-name=>'SESSION',-value=>$create,-expires =>  '+2h',);

if(int(gestione_sessione::getCookie('prenotato'))==1){
	print "location: index.cgi\n\n";
}

my $prenotato_cookie = CGI::Cookie->new(-name=>'prenotato',-value=>"1",-expires =>  '+20s',);
#controllo per evitare il ricaricamento della pagina, che comporterebbe a prenotare un secondo volo.

print CGI::header(-cookie=>$session_cookie);#imposto il cookie di sessione

print "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">
<html xmlns=\"http://www.w3.org/1999/xhtml\" lang=\"it\" xml:lang=\"it\">
	<head>
		<link rel=\"stylesheet\" href=\"../style/main.css\" type=\"text/css\" media=\"screen\" charset=\"utf-8\"/>
		<title>$titolo</title>
	</head>
	
	<body>
";


#funzionamento: la funzione riceve un riferimento ad un array di riferimenti di array.
# esempio: RIF_MENU_1=array("Home", "pagina.html", "1"); //Il pulsante avrà il nome "Home", il riferimento a "pagina.html" e sarà selezionato sul CSS.
#          RIF_MENU_1=array("404", "404.html", "0"); //Il pulsante avrà il nome "404", il riferimento a "404.html" e NON sarà selezionato sul CSS.
#
print_header::setMenu(menu::get());

my @path_temp;
my @path=("Home", "index.cgi");
push @path_temp, \@path;
my @path=("Riepilogo prenotazione", "checkout.cgi");
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

if($andata==1){
	$id_volo_ritorno="";
	$giorno_ritorno="";
	$ritorno_orario_partenza="";
	$ritorno_orario_arrivo="";
	$ritorno_prezzo=0;
}

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

my $bagagli=int(gestione_sessione::getParam("bagagli"));

#sezione variabili inerenti ai servizi
my @servizi=@{getServizi()};
$id_volo_partenza=~/T([\d]+)V([\d]+)/;
my @gma=@{check_form::regexp_data($giorno_partenza)};
if(int(@gma[1])<10){
	@gma[1]="0".@gma[1];
}
if(int(@gma[0])<10){
	@gma[0]="0".@gma[0];
}
my $id_prenotazione_partenza=database::prenota(gestione_sessione::getParam("id"), "@gma[2]-@gma[1]-@gma[0]",$2, \@passeggeri,\@servizi,$bagagli);
my $id_prenotazione_ritorno=0;
if($andata==0){
	$id_volo_ritorno=~/T([\d]+)V([\d]+)/;
	@gma=@{check_form::regexp_data($giorno_ritorno)};
	$id_prenotazione_ritorno=database::prenota(gestione_sessione::getParam("id"), "@gma[2]-@gma[1]-@gma[0]",$2, \@passeggeri,\@servizi,$bagagli);

}

#variabili generali

my $prezzo_biglietti=int($andata_prezzo)+int($ritorno_prezzo);
my $prezzo_servizi=0;
print print_header::print();



print "		<div id=\"main\"><!-- div che contiene tutto il contenuto statico e/o dinamico-->"; #mega div

my $testo='
	<div class="sezione">
				<div><!-- div h2 -->
					<h2>Riepilogo della prenotazione</h2>
				</div><!-- fine h2-->
				<div><!-- div partenza -->
					<h2>PRENOTAZIONE N&deg; '.$id_prenotazione_partenza.' EFFETTUATA</h2>
					<h2>Partenza:</h2>
					<p>Volo N&deg; '.$id_volo_partenza.'</p>
					<p>Partenza il: '.$giorno_partenza.'</p>
					<p>Alle ore: '.$andata_orario_partenza.'</p>
					<p>Dall\'aereoporto '.$select_partenza.'</p>
					<p>Arrivo alle ore: '.$andata_orario_arrivo.'</p>
					<p>Nell\'aereoporto '.$select_arrivo.'</p>
					<p>Prezzo del biglietto: '.$andata_prezzo.'&euro;</p>
					
				</div><!-- fine partenza -->';
if($andata==0){
$testo.='				<div><!-- div ritorno -->
					<h2>PRENOTAZIONE N&deg; '.$id_prenotazione_ritorno.' EFFETTUATA</h2>
					<h2>Ritorno:</h2>
					<p>Volo N&deg; '.$id_volo_ritorno.'</p>
					<p>Partenza il: '.$giorno_ritorno.'</p>
					<p>Alle ore: '.$ritorno_orario_partenza.'</p>
					<p>Dall\'aereoporto '.$select_arrivo.'</p>
					<p>Arrivo alle ore: '.$ritorno_orario_arrivo.'</p>
					<p>Nell\'aereoporto '.$select_partenza.'</p>
					<p>Prezzo del biglietto: '.$ritorno_prezzo.'&euro;</p>
					
				</div><!-- fine ritorno -->';
}
$testo.='				<div><!-- div passeggeri -->';
if($num_passeggeri>0){
	$testo.='				<h2>Passeggeri:</h2>
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
					
}else{
	$testo.="	<div>
					<p>(Non ci sono passeggeri aggiuntivi)</p>
				</div>";
}
$testo.='				
				</div><!-- fine div passeggeri -->
				<div>
					<h2>BAGAGLI</h2>
					<p>
						<span>Numero di bagagli: </span>
						<span>'.$bagagli.'</span>
				</div>
				<div><!-- div servizi -->
					<h2>Servizi aggiuntivi:</h2>
					';
for(my $i=0; $i<scalar(@servizi); $i++){
	my @temp=@{@servizi[$i]};
	if(gestione_sessione::getParam("servizio".@temp[0])==1){
		$testo.='	<p>'.@temp[1].', prezzo: '.@temp[2].'&euro; </p>';
		$prezzo_servizi+=int(@temp[2]);
	}
}
$testo.='			
				</div><!-- fine div servizi -->
				<div><!-- div costi -->
					<h2>COSTO TOTALE:</h2>
					<p>Biglietti: '.$prezzo_biglietti.'&euro; </p>
					<p>Servizi aggiuntivi: '.$prezzo_servizi.'&euro; </p>
					<p></p>
					<h2>Totale: '.($prezzo_biglietti+$prezzo_servizi).'&euro; </h2>
				</div><!-- fine div costi -->
				
				<div>
					<span>
						<a href="index.cgi">Torna alla homepage</a>
					</span>
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