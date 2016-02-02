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
my $titolo="Stampa prenotazione";


my $create=gestione_sessione::createSession();

if(gestione_sessione::getParam("logged")!=1){
	print "location: index.cgi\n\n";
	exit;
}

gestione_sessione::setParam("location","utente.cgi");


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

print "		<div id=\"main\"><!-- div che contiene tutto il contenuto statico e/o dinamico-->"; #mega div
my $testo='<div class="contenitore_sezioni">';
my @prenotazioni=@{database::getPrenotazioni(gestione_sessione::getParam("id"), $id_prenotazione)};
	foreach my $tmp (@prenotazioni)
	{
							$testo.="<div class=\"sezione\"><!-- apro maxi contenitore per le sezioni -->";
							my @prenotazione=@{$tmp};
							$testo.='
								<dl>
									<dt>Prenotazione N&deg; '.@prenotazione[0].'</dt>
									<dt>Volo: '.@prenotazione[2].'</dt>
									<dt>Data di prenotazione: '.@prenotazione[5].'</dt>
									<dt>Data di partenza: '.@prenotazione[6].'</dt>
									<dt>Partenza: '.@prenotazione[3].'</dt>
									<dt>Arrivo: '.@prenotazione[4].'</dt>
									<dt>Orario partenza: '.@prenotazione[7].'</dt>
								</dl>
							</div><!-- chiudo prenotazione -->
							<div class="clearer"></div>';
							$testo.="<div class=\"sezione\"><!-- apro maxi contenitore per le sezioni -->";
							
							$testo.='<h3>Passeggeri</h3>';
							my @passeggeri=@{@prenotazione[11]};
							foreach my $pt (@passeggeri){
								my @passeggero=@{$pt};
								$testo.="
								<p>Nome: @passeggero[0]</p>
								<p>Cognome: @passeggero[1]</p>
								<p>Codice Fiscale: @passeggero[2]</p>
								<p>Data di nascita: @passeggero[3]</p>
								";
							}
							$testo.='
							</div><!-- chiudo prenotazione -->
							<div class="clearer"></div>';
							$testo.='<a href="index.cgi">Torna alla pagina principale</a>
					';
		#$id, $posti_occupati, "T$tratta"."V$id_volo", $aereoporto_partenza,$aereoporto_arrivo,$data_prenotazione, $data_partenza, $ora_partenza, $prezzo, $bagagli, \@servizi_prenotati,\@utenti
		
	}
$testo.= '</div><!-- chiudo contenitore sezioni -->';
print print_content::print($testo);
print "		</div>"; #chiudo il div main
print "	</body>
</html>";