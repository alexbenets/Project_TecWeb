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

my $id_prenotazione=int($form{"id"});
my $elimina=int($form{"elimina"});




my $titolo="Area utente";


my $create=gestione_sessione::createSession();
my $result=0;
if($elimina==1){
	my $id_utente=int(gestione_sessione::getParam("id"));
	$result=database::modificaPrenotazione($id_utente, $id_prenotazione, 1);#elimino la prenotazione
}

if(gestione_sessione::getParam("logged")!=1){
	print "location: index.cgi\n\n";
	exit;
}

gestione_sessione::setParam("location","/cgi-bin/gestisci_prenotazione.cgi");


my $session_cookie = CGI::Cookie->new(-name=>'SESSION',-value=>$create,-expires =>  '+2h',);

print CGI::header(-cookie=>$session_cookie);#imposto il cookie di sessione

print "
<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">
<html xmlns=\"http://www.w3.org/1999/xhtml\">
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
my @path=("Area utente", "utente.cgi");
push @path_temp, \@path;
my @path=("Gestione prenotazioni", "gestisci_prenotazione.cgi");
push @path_temp, \@path;
print_header::setPath(\@path_temp);

print print_header::print();
print "	<div id=\"main\"><!-- div che contiene tutto il contenuto statico e/o dinamico-->"; #mega div
my $risultato="";
if($elimina==1 and $result==1){
	$risultato="<h3>La prenotazione $id_prenotazione &egrave; stata eliminata correttamente!</h3>";
}
if($elimina==1 and $result<0){
	$risultato="<h3 class=\"warning\">ATTENZIONE: la prenotazione non &egrave; stata cancellata</h3>";
}
my $testo='<div id="contenitore_sezioni">
		<div class="sezione"><!-- apro maxi contenitore per le sezioni -->
					<object>'.$risultato.'
						<fieldset>
							<p>Data: 2013-03-30</p>
							<p>Partenza: Milano Malpensa</p>
							<p>Arrivo: Roma Fiumicino</p>
							<p>Orario partenza: 00:00</p>
							<p><a href="gestisci_prenotazione.cgi?id=1&amp;elimina=1">Elimina</a></p>
						</fieldset>
					</object>
		</div><!-- chiudo prenotazione -->
		<div class="clearer"></div>
		</div><!-- chiudo contenitore sezioni -->';;

print print_content::print($testo);
print "		</div>
		<div class=\"clearer\"></div>"; #chiudo il div main
print print_footer::print();
print "	</body>
</html>";