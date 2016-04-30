#!/usr/bin/perl

package commenti;
use strict;
use CGI::Carp qw(fatalsToBrowser);
use CGI qw(:standard);
use CGI;
#pagina per la creazione di nuovi commenti o la modifica/eliminazione
#deve ricevere dei parametri dalla pagina di visualizzazione: idP dal quale ricavare idUR, idV ( e se serve idCommento, datacommento, titolo, contenuto, voto(se esiste, zero altrimenti))
my %form;


foreach my $p (param()) {
    $form{$p} = param($p);
    #print "$p = $form{$p}<br>\n";
}

my $idPrenotazione=int($form{"idP"}); # se 0=> voglio vis tutte le prenot else modifica commento/crea NB un SOLO commento
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
						<li><a href="utente.cgi?commenti=1">Commenti</a></li>
					</ul>
				</div><!-- chiudo secondo menu -->';
my $testo='<div id="contenitore_sezioni"><!-- apro maxi contenitore per le sezioni -->
					
					<div class="sezione" id="S1"><!-- inizio div che contiene titolo e sezione dell\'articolo -->
						<h3>Benvenuto!</h3>
						<p>In questa pagina potrai modificare i tuoi dati e le tue prenotazioni (fino a 2 giorni prima della partenza), nonch&egrave 
						esprimere il tuo parere sull\'esperienza di volo avuta con noi.</p>
					</div><!-- chiudo sezione -->
					
					<div id="torna_su">
						<a href="#header">Torna su</a>
					</div>
			</div><!-- chiudo contenitore_sezioni -->	
			<div class="clearer"></div>
				';
#fine di parte copiata che dovrebbe formare la parte comune a tutte le pagine del sito
#i dati di questa dovrebbero essere presi dal database
my $form_comm='<form action="script_commenti.cgi" method="post">  
	<fieldset>
		<legend>commento</legend>
		<input type=”hidden” name=”idC” value=”$idC”>
		<input type=”hidden” name=”idV” value=”$idV”>
		<input type=”hidden” name=”idUR” value=”$idUR”>
		Valutazione:
		<select name="valutazione">
			<option value="0"></option>
			<option value="1">1</option>
			<option value="2">2</option>
			<option value="3">3</option>
			<option value="4">4</option>
			<option value="5">5</option>
		</select>
		</br>
		<label for="titolo">Titolo:</label>
		<input type="text" name="titolo" id="titolo"></br>
		testo:
		<textarea name="testo" rows="5" col="30"></br>
		<input type="submit" value="Salva">
		<input type="button" value="elimina"> <!--(???)occhio che sono entrambi di tipo submit non so se valgono giusti così-->
	</fieldset>
</form>';

my $form_vuota='<form>
	<fieldset action="script_commenti.cgi" method="post">
		<legend>nuovo commento</legend>
		<input type=”hidden” name=”idC” value=”0”>
		<input type=”hidden” name=”idV” value=”$idV”>
		<input type=”hidden” name=”idUR” value=”$idUR”>
		Valutazione:
		<select name="valutazione">
			<option value="0" checked="checked"></option>
			<option value="1">1</option>
			<option value="2">2</option>
			<option value="3">3</option>
			<option value="4">4</option>
			<option value="5">5</option>
		</select>
		</br>
		Titolo:
		<input type="text" name="titolo"></br>
		testo:
		<textarea name="testo" rows="5" col="30"></br>
		<input type="submit" value="Salva">
	</fieldset>
</form>';
my $idP=;#passato da visualizza_commenti, COME lo inizializzo???
$idUR=; #ricavato direttamente dal database, presente nella prenotazione 
$idV=; #idem
if($idUR!=0 and $idV!=0){
	if($idCo!=0){
		#esiste un commento effettuato dall'utente su quel volo, uso $form_comm
		$text.=$form_comm;
	}
	else
		#non esiste alcun commento dell'utente sul volo selezionato, uso $form_vuota
		$text.=$form_vuota;
}


#form da manipolare NB SERVE UNA FUNZIONE PER VALIDARLA
#SE la form deve essere SALVATA
#la funzione controllerà se esistono campi vuoti:
#se il select valutazione è vuoto ""=>$errore.=non è stata  impostata una valutazione
#se il titolo è ""=>$errore.=non si è dato titolo al commento
#se il testo è""=>$errore.=il commento è vuoto
#puo esseci solo voto o solo commento con titolo MA l'utente deve dare conferma che è proprio quello che vuole inserire(!!! troppo complicato?)
#SE INVECE la form va ELIMINATA
#chiedo conferma e chiudo

$testo.= '</div><!-- chiudo contenitore sezioni -->';

print print_content::print($testo);
print "		</div>"; #chiudo il div main
print print_footer::print();
print "	</body>
</html>";


