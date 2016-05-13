#!/usr/bin/perl
package commenti;
use strict;
use DateTime;  #utilizzato per validare la data inserita
use Time::Piece;
use CGI::Carp qw(fatalsToBrowser);
use CGI qw(:standard);
use CGI;

my $q = new CGI; #parte mia


require "common_functions/print_header.cgi";
#require "common_functions/print_search.cgi"; #inutile: non viene sfruttato in questa pagina.
require "common_functions/print_content.cgi";
require "common_functions/print_footer.cgi";
require "common_functions/Session.cgi";
require "common_functions/check_form.cgi";
require "common_functions/database.cgi";
require "common_functions/menu.cgi";

#parte iniziale per la corretta visualizzazione della pagina

# NB !!! %form dovrebbe essere inutile xke non viene passato niente mediante il link
#my %form;


#foreach my $p (param()) {
#    $form{$p} = param($p);
    #print "$p = $form{$p}<br>\n";
#} 

#my $id_prenotazione=int($form{"idP"}); 
my $idUR=gestione_sessione::getParam("id");
my $titolo="Area utente";


my $create=gestione_sessione::createSession();

if(gestione_sessione::getParam("logged")!=1){
	print "location: index.cgi\n\n";
	exit;
}

gestione_sessione::setParam("location","utente.cgi");


my $session_cookie = CGI::Cookie->new(-name=>'SESSION',-value=>$create,-expires =>  '+2h',);

print CGI::header(-cookie=>$session_cookie);#imposto il cookie di sessione
sub yesorno($action){
	$action=_@;
	if($action=="yes"){
		return true;
		}
	else{
		return false;
	}
}

print "
<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">
<html xmlns=\"http://www.w3.org/1999/xhtml\" lang=\"it\" xml:lang=\"it\">
	<head>
		<link rel=\"stylesheet\" href=\"../style/main.css\" type=\"text/css\" media=\"screen\" charset=\"utf-8\"/>
		<title>$titolo</title>
	</head>
	
	<body>
";
print_header::setMenu(menu::get());
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
						<li><a href="utente.cgi">Commenti</a></li>
					</ul>
				</div><!-- chiudo secondo menu -->';
my $testo='<div id="contenitore_sezioni"><!-- apro maxi contenitore per le sezioni -->
					
					<div class="sezione" id="S1"><!-- inizio div che contiene titolo e sezione dell\'articolo -->
						<h3>Benvenuto!</h3>
						<p>In questa pagina potrai manipolare il commento espresso sul volo prenotato mediante la prenotazione che hai selezionato.</p>
					</div><!-- chiudo sezione -->
					
					<div id="torna_su">
						<a href="#header">Torna su</a>
					</div>
				';

#done parte iniziale di visualizzazione pagina 

#form da manipolare NB SERVE UNA FUNZIONE PER VALIDARLA
#SE la form deve essere SALVATA
#la funzione controllerà se esistono campi vuoti:
#se il select valutazione è vuoto ""=>$errore.=non è stata  impostata una valutazione
#se il titolo è ""=>$errore.=non si è dato titolo al commento
#se il testo è""=>$errore.=il commento è vuoto
#puo esseci solo voto o solo commento con titolo MA l'utente deve dare conferma che è proprio quello che vuole inserire(!!! troppo complicato?)
#SE INVECE la form va ELIMINATA
#chiedo conferma e chiudo

my $error_count=0;
my $idC = $q->param('idC');
my $idV = $q->param('idV');
my $valutazione = $q->param('valutazzione');
my $titolo = $q->param('titolo');
my $testo= $q->param('testo');
my $form_control="<form action=\"script_commenti.cgi\" method=\"post\"> 
						<fieldset>
							<legend>commento</legend>
							<input type=\”hidden\” name=\”idC\” value=\”$idC\”>
							<input type=\”hidden\” name=\”idV\” value=\”$idV\”>
							<input type=\”hidden\” name=\”idUR\” value=\”$idUR\”>
							Valutazione:
							<select name=\"valutazione\">
								<option value=\"0\" checked=\"checked\">non valutato</option>
								<option value=\"1\">1</option>
								<option value=\"2\">2</option>
								<option value=\"3\">3</option>
								<option value=\"4\">4</option>
								<option value=\"5\">5</option>
							</select>
							</br>
							</br>
							<label for=\"titolo\">Titolo:</label>
							<input type=\"text\" name=\"titolo\" id=\"titolo\">$titolo</br>
							<textarea name=\"testo\" rows=\"5\" col=\"30\">$testo</br>
							<input type=\"submit\" value=\"Salva\">
						</fieldset>
					</form>";

if(($c1{idC}==0 and $c1{submit}==true and $q->param()) || ($c1{idC}!=0 and $c1{submit}==true)){  

	#il commento non esiste e devo salvarlo => creo un nuovo hash e lo stampo
	# O SE il commento esiste e devo salvarlo => cerco l'hash con i giusti id e lo modifico
		
		if(testo==""){
        	$error_count=$error_count+1;
        		$testo.="il tuo commento non &grave valido in quanto non fornisce sufficente informazione sul volo che hai effettuato";
        }
        if ($error_count!=0){
        	$testo.= '$form_control';
        }
		$testo.= $q->("utente $idUR");
        $testo.= $q->p("volo $idV, valutazione $valutazione, titolo $titolo, testo $testo");

     	%c1= {
			idC => $idC
			idV => $idV #usando local posso creare variabili del pachage x passare?
			idUR => $idUR
			valutazione =>$valutazione
			titolo =>$titolo
			testo =>$testo
			submit =>true #usiamo un valore booleano? T<=> ho analizzato la form e devo salvare; F altrimenti
			cancella =>  false#usiamo un valore booleano? T<=> ho analizzato la form, è un commento scritto da cancellare; F altrimenti
		};
}
else{		
	#il commento esiste e devo eliminarlo, questo va fatto direttamente sul database ma prima controllo che l'autore voglia davvero eliminarlo
	$testo.="vuoi eliminare il commento sul volo $V?"# dal database troveremo poi altri dati da scrivere x identificare il commento: data ecc
	$form_control="<form method=\"get\" action=\"&yesorno\">
		<fieldset>
			<input type=\"radio\" name=\"yesorno\" value=\"1\"> Si</input><br>
			<input type=\"radio\" name=\"yesorno\" value=\"0\" checked=\"cheched\"> No</input> 
			</br>
			<input type=\"submit\" value=\"Salva\">
		</fieldset>
	</form>";
	$testo.=$form_control;
	if(&yesorno){
		for (keys %c1){
       		delete $c1{$_}; #ok?
    	}
    }
    $testo.="il commento effettuato dall'utente $idUR sul volo $idV è stato eliminato"
}
$testo.= '</div><!-- chiudo contenitore_sezioni -->	
			<div class="clearer"></div>';

#patre finale
print "		</div>"; #chiudo il div main
print print_footer::print();
print "	</body>
</html>";
