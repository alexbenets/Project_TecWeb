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
gestione_sessione::setParam("location","/cgi-bin/servizi_aggiuntivi.cgi");



my @servizi=@{getServizi()};

#dati recuperati dalle variabili di sessione
for(my $i=0; $i<scalar(@servizi); $i++){
	my @temp=@{@servizi[$i]};
	#temp: ID
	#verifico se il checkbox corrispondente è stato selezionato o meno e, nel caso, leggo/aggiorno il suo valore
	#sulla base di quanto impostato nelle variabili di sessione.
	if(defined($form{"prenota"})){
		
		my $selezionato=0;
		if(defined($form{"servizio".@temp[0]})){
			$selezionato=1;
		}
			
		gestione_sessione::setParam("servizio".@temp[0],$selezionato);
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
	my $selezionato=gestione_sessione::getParam("servizio".@temp[0]);
	if($selezionato==1){
		$selezionato=' checked="checked"';
	}else{
		$selezionato="";
	}
	$testo.='<div>	<label for="servizio'.@temp[0].'">'.@temp[1].' ('.@temp[2].'&euro;)</label>
			<p><input type="checkbox" id="servizio'.@temp[0].'" name="servizio'.@temp[0].'" value="1" '.$selezionato.'/></p>
			<p>'.@temp[3].'</p>
			</div>';
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