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
gestione_sessione::setParam("location","/cgi-bin/servizi_aggiuntivi.cgi");



my @servizi=@{getServizi()};

#dati recuperati dalle variabili di sessione
for(my $i=0; $i<scalar(@servizi); $i++){
	my @temp=@{@servizi[$i]};
	#temp: ID, Nome, Prezzo
	#verifico se il checkbox corrispondente è stato selezionato o meno e, nel caso, leggo/aggiorno il suo valore
	#sulla base di quanto impostato nelle variabili di sessione.
	if(defined($form{"prenota"})){
		
		my $selezionato=0;
		if(defined($form{"servizio$i"})){
			$selezionato=1;
		}else{
			$selezionato=0;
		}
			
		gestione_sessione::setParam("servizio$i",$selezionato);
		gestione_sessione::setParam("nome_servizio$i",@temp[1]);
		gestione_sessione::setParam("prezzo_servizio$i",@temp[2]);
	}
		
}

my $next=0;
if(defined($form{"prenota"} )){
	print "Location: prenota.cgi\n\n";
	exit;
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
print_header::setPath(\@path_temp);



print print_header::print();

print "		<div id=\"main\"><!-- div che contiene tutto il contenuto statico e/o dinamico-->"; #mega div
my $testo='
	<div class="sezione">
		<form action="servizi_aggiuntivi.cgi" method="post">
			<fieldset>';
for(my $i=0; $i<scalar(@servizi); $i++){
	my @temp=@{@servizi[$i]};
	my $selezionato=gestione_sessione::getParam("servizio$i");
	if($selezionato==1){
		$selezionato=' checked="checked"';
	}else{
		$selezionato="";
	}
	$testo.='<div>	<label for="servizio'.$i.'">'.@temp[1].' ('.@temp[2].'&euro;)</label>
			<input type="checkbox" id="servizio'.$i.'" name="servizio'.$i.'" value="1" '.$selezionato.'/></div>';
}

gestione_sessione::setParam("Numero_servizi", scalar(@servizi));
$testo.='
			<div>
				<button type="submit" id="prenota" name="prenota">
					<span>prenota</span>
				</button>	
			</div>
			</fieldset>
		</form>
	</div><!-- chiudo sessione -->
';

print print_content::print($testo);
print "		</div>"; #chiudo il div main
print print_footer::print();
print "	</body>
</html>";