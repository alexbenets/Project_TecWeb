#!/usr/bin/perl


package index_page;

use strict;
use CGI::Carp qw(fatalsToBrowser);
use CGI qw(:standard);
use CGI;


require "common_functions/print_header.cgi";
require "common_functions/print_search.cgi";
require "common_functions/print_content.cgi";
require "common_functions/print_footer.cgi";
require "common_functions/Session.cgi";
require "common_functions/check_form.cgi";
require "common_functions/database.cgi";
require "common_functions/menu.cgi";
my $titolo="Home";


my $create=gestione_sessione::createSession();
gestione_sessione::setParam("location","/cgi-bin/index.cgi");


my $ar=gestione_sessione::getParam("AR");
my $select_partenza=gestione_sessione::getParam("partenza");
my $select_arrivo=gestione_sessione::getParam("arrivo");
my $data_partenza=check_form::leggi_data(gestione_sessione::getParam("data_partenza"));
my $data_ritorno=check_form::leggi_data(gestione_sessione::getParam("data_ritorno"));
my $select_passeggeri=gestione_sessione::getParam("passeggeri");

my $session_cookie = CGI::Cookie->new(-name=>'SESSION',-value=>$create,-expires =>  '+2h',);

print CGI::header(-cookie=>$session_cookie);#imposto il cookie di sessione

print "
<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">
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

my %tratte=database::listTratte();
print_search::set_tratte(%tratte);

my @path_temp;
my @path=("Home", "index.cgi");
push @path_temp, \@path;
print_header::setPath(\@path_temp);

print print_header::print();
print "		<div id=\"main\"><!-- div che contiene tutto il contenuto statico e/o dinamico-->"; #mega div
print print_search::set_date(0, $ar, $select_partenza, $select_arrivo, $data_partenza, $data_ritorno, $select_passeggeri,1);
my $testo='
				<div id="presentazione">
					
					<p>Benvenuto nel sito ufficiale della compagnia aerea low cost A-ir</p>
					<p>Qui potrai trovare tutte le informazioni riguardanti la nostra compagnia, il nostro personale, la nostra flotta e scoprire tutte le destinazioni che puoi scegliere per la tua vacanza o per il tuo viaggio di affari!</p>
					<p>Cosa stai aspettando? Prenota subito il tuo volo!!</p>
				</div>';
print print_content::print($testo);
print "		</div>"; #chiudo il div main
print print_footer::print();
print "	</body>
</html>";