#!/usr/bin/perl
http://www.tutorialspoint.com/perl/perl_cgi.htm
#pagina dalla quale sceglire la prenotazione (dunque il volo) sulla quale esprimere un commento;  
#richiama la pagina modifica commento contenente la form per scrivere un nuovo commento
#se esiste gia un commento fatto dall'utente registrato su quel volo allora viene invece richiamata una form per modificare o eliminare il commnto
package commenti;
use strict;
use DateTime;  #utilizzato per validare la data inserita
use Time::Piece;
use CGI::Carp qw(fatalsToBrowser);
use CGI qw(:standard);
use CGI;

require "common_functions/print_header.cgi";
#require "common_functions/print_search.cgi"; #inutile: non viene sfruttato in questa pagina.
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

my $id_prenotazione=int($form{"idP"}); # se 0=> do we need it?
my $titolo="Area utente";


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

#my %tratte=database::listTratte();
#print_search::set_tratte(%tratte);

my @path_temp;
my @path=("Home", "index.cgi");
push @path_temp, \@path;
my @path=("Area utente", "utente.cgi");
push @path_temp, \@path;
print_header::setPath(\@path_temp);

print print_header::print();
print "		<div id=\"main\"><!-- div che contiene tutto il contenuto statico e/o dinamico-->"; #mega div
print '<div id="secondo_menu">
					<ul>
						<li><a href="utente.cgi?dati=1">Dati personali</a></li>
						<li><a href="utente.cgi?prenotazioni=1">Prenotazioni</a></li>
						<li><a href="utente.cgi">Commenti</a></li> <!--ho eliminato il "?commenti=1" credo che sia inutile visto che non mi pare utile in nessun luogo !!! controlla pagina Utente-->
					</ul>
				</div><!-- chiudo secondo menu -->';
my $testo='<div id="contenitore_sezioni"><!-- apro maxi contenitore per le sezioni -->
					
					<div class="sezione" id="S1"><!-- inizio div che contiene titolo e sezione dell\'articolo -->
						<h3>Benvenuto!</h3>
						<p>In questa pagina potrai modificare selezionare una prenotazione sulla quale esprimere un commento, o modificare un commento gi\&agrave espresso un parere</p>			esprimere il tuo parere sull\'esperienza di volo avuta con noi.</p>
					</div><!-- chiudo sezione -->
					
					<div id="torna_su">
						<a href="#header">Torna su</a>
					</div>';

#qui comincia davvero la mia parte !!! in mezzo stavano i casi trattati da marco nella pagina utente.cgi
#questo script deve visualizzare i voli effettuati dall'utente (sono voli x i quali l'utente ha fatto una prenotazione, con data di partenza passata rispetto al giorno in cui si scrive)
#il path dovrebbe essere: -> trova le prenotazioni dell'utente @prenotazioni: /database/tabPrenotazione/prenotazione[@idUR=$utente]/@idP; $utente=id utente registrato
#						  -> trova le prenotazioni con data passata: foreach $prenotazione(@prenotazioni){
#																				if($prenotaznione/data è passata){
#																					inserisci $pernotazione in  @commentabili;
#																			 }
#devo ora mostrare i dati di ogni volo: ->dalla tabella prenotazioni recupero: dataPartenza o idV
#                                                                              foreach $commentabile(@commentabili){
#                                                                                 /database/tabPrenotazione/prenotazione[@idP=$commentabili]/dataPartena e @idV
# => possiamo infilare questo in qualche modo in un ARRAY DI HASH (cosi che ogni elemento dell'array che andiamo a creare vontiene i campo che servono)
#-> della tebella volo visualizza: oraPartenza e trova idT
#-> dalla tabella tratta trova la durata X RICAVARE L'orario arrivo, idApP e idApA
#->dalla tabella aereoporto trova nome e idC
#->dalla tabella citta trova il nome delle due citta collegate dal volo
#WHEW!  
# =>  IMPORTANTE: CON ID DEL VOLO-> cerco se esiste commento eseguito dall'utente su quel volo 
#se si ->bottone sulla prenotazione x visualizzarlo salva commento
#altrimenti form vuota x fare un nuovo commento


#per visualizzare prenotazioni utente
my @prenotazioni=@{database::getPrenotazioni(gestione_sessione::getParam("id"))}; #secondo parametro di dubbia importanza: ", $id_prenotazione"
my $today = Time::Piece->new();
	foreach my $tmp (@prenotazioni)
	{#!!!
	 #immagino che qui servirebbe un modo per rendere cliccabile l'intera sezione della prenotazione, che dovrebbe chiamare lo script per mostrare la form corrispondante
	 #questa chiamata dovrebbe passare l'idUR e l'idV => se esiste commento form visualizzata piena, con pulsante salva e elimina; altrimenti vuota con solo pulasante salva
		if(@prenotazione[6]<$today){# se dataPartenza @prenotazione[3] e < della data di oggi (print search la contiene cerca) => aggiungi a $testo, altrimenti ignora
			$testo.="
			<div class=\"sezione\"><!-- apro maxi contenitore per le sezioni -->";
			my @prenotazione=@{$tmp};
				$testo.="
				<a href=\"modifica_commenti.cgi?idP='.@prenotazione[0].'\"> <!--noto adesso che questo portava ancora a stampa_prenotazione-->
				<object>
					<fieldset>
								<p>Data: '.@prenotazione[6].'</p> 
								<p>Partenza: '.@prenotazione[3].'</p>
								<p>Arrivo: '.@prenotazione[4].'</p>
								<p>Orario partenza: '.@prenotazione[7].'</p>
					</fieldset>				
				</object>
				</a>
				<!--<p><a href=\"modifica_commenti.cgi?idP='.@prenotazione[0].'\">modifica commenti</a></p> non più necessario credo-->
				";
			#my @temp=($id, $posti_occupati, "T$tratta"."V$id_volo", $aereoporto_partenza,$aereoporto_arrivo,$data_prenotazione, $data_partenza, $ora_partenza, $prezzo, $bagagli, \@servizi_prenotati); 
			$testo.="</div><!-- chiudo prenotazione -->
			<div class=\"clearer\"></div>";
		}
	}
$testo.= "</div><!-- chiudo contenitore_sezioni -->	
		<div class=\"clearer\"></div>";

print print_content::print($testo);
print "		</div>"; #chiudo il div main
print print_footer::print();
print "	</body>
</html>";
