#!/usr/bin/perl


package pagina_utente;

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


my %form;


foreach my $p (param()) {
    $form{$p} = param($p);
    #print "$p = $form{$p}<br>\n";
}

my $modifica_dati_utente=int($form{"dati"});
my $modifica_prenotazioni=int($form{"prenotazioni"});

my $titolo="Area Amministrativa";


my $create=gestione_sessione::createSession();

if((gestione_sessione::getParam("logged")!=1) or (gestione_sessione::getParam("admin")!=1)){
	print "location: index.cgi\n\n";
	exit;
}

gestione_sessione::setParam("location","admin.cgi");


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
my @path=("Area amministratore", "admin.cgi");
push @path_temp, \@path;
print_header::setPath(\@path_temp);

print print_header::print();
print "		<div id=\"main\"><!-- div che contiene tutto il contenuto statico e/o dinamico-->"; #mega div
print '<div id="secondo_menu">
					<ul>
						<li><a href="admin_nazioni.cgi">Gestione Nazioni</a></li>
						<li><a href="admin_citta.cgi">Gestione Citt&agrave;</a></li>
						<li><a href="admin_aereoporti.cgi">Gestione Aereoporti</a></li>
						<li><a href="admin_tratte.cgi">Gestione Tratte</a></li>
						<li><a href="admin_voli.cgi">Gestione Voli</a></li>
						<li><a href="admin_servizi.cgi">Gestione Servizi</a></li>
					</ul>
				</div><!-- chiudo secondo menu -->';
my $testo='<div id="contenitore_sezioni"><!-- apro maxi contenitore per le sezioni -->
					
					<div class="sezione" id="S1"><!-- inizio div che contiene titolo e sezione dell\'articolo -->
						<h3>Benvenuto!</h3>
						<p>In questa pagina modificare i vari parametri inerenti agli aereoporti, citt&agrave; ecc...</p>
					</div><!-- chiudo sezione -->
					
					<div id="torna_su">
						<a href="#header">Torna su</a>
					</div>
			</div><!-- chiudo contenitore_sezioni -->	
			<div class="clearer"></div>
				';

print print_content::print($testo);
print "		</div>"; #chiudo il div main
print print_footer::print();
print "	</body>
</html>";