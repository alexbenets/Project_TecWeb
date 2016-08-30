#!/usr/bin/perl
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


my $q = new CGI; #parte maria, forse userò l'altro metodo wait

#require "common_functions/aggiorna_index.cgi";


#parte iniziale per la corretta visualizzazione della pagina

# NB !!! %form dovrebbe essere inutile xke non viene passato niente mediante il link
my %form;


foreach my $p (param()) {
    $form{$p} = param($p);
}
 

#my $id_prenotazione=int($form{"idP"}); 
#my $idUR=gestione_sessione::getParam("id");
#my $titolo="Area utente";


my $create=gestione_sessione::createSession();

#if(gestione_sessione::getParam("logged")!=1){
#	print "location: index.cgi\n\n";
#	exit;
#}

#gestione_sessione::setParam("location","utente.cgi");


#print CGI::header(-cookie=>$session_cookie);#imposto il cookie di sessione
my $session_cookie = CGI::Cookie->new(-name=>'SESSION',-value=>$create,-expires =>  '+2h',);

print CGI::header(-cookie=>$session_cookie);#imposto il cookie di sessione

my $titolo="Funzioni commento";

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
my @path=("Modifica commenti", "script_commenti.cgi");
push @path_temp, \@path;
print_header::setPath(\@path_temp);

print print_header::print();
print "		<div id=\"main\"><!-- div che contiene tutto il contenuto statico e/o dinamico-->"; #mega div
print '<div id="secondo_menu">
					<ul>
						<li><a href="utente.cgi?dati=1">Dati personali</a></li>
						<li><a href="utente.cgi?prenotazioni=1">Prenotazioni</a></li>
					</ul>
				</div><!-- chiudo secondo menu -->';
#print print_search::print(0, $ar, $select_partenza, $select_arrivo, $data_partenza, $data_ritorno, $select_passeggeri,1);

#done parte iniziale di visualizzazione pagina 

#form da manipolare NB SERVE UNA FUNZIONE PER VALIDARLA
#SE la form deve essere SALVATA
#la funzione controllerà se esistono campi vuoti:
#se il select valutazione &egrave; vuoto ""=>$errore.=non &egrave; stata  impostata una valutazione
#se il titolo &egrave; ""=>$errore.=non si &egrave; dato titolo al commento
#se il testo &egrave;""=>$errore.=il commento &egrave; vuoto
#puo esseci solo voto o solo commento con titolo MA l'utente deve dare conferma che &egrave; proprio quello che vuole inserire(!!! troppo complicato?)
#SE INVECE la form va ELIMINATA
#chiedo conferma e chiudo

my $error_count=0;
my $idC = $q->param('idC');
my $idV = $q->param('idV');
my $idUR=$q->param('idUR');
my $cittaP= $q->param('cittaP');
my $cittaA= $q->param('cittaA');
my $valutazione = $q->param('valutazione');
my $titolo = $q->param('titolo');
my $testoC= $q->param('testo');


my $form_control="";

#sub addCommento {
#	my ($titolo, $valutazione, $testo, $idV, $idUR)=@_;
my $result=database::addCommento($titolo, $testoC, $idV, $idUR);
  
if ($result<1){#$testoC==NULL
	$form_control="
				<h3>Il Commento sul volo $idV da $cittaP a $cittaA non &egrave; stato salvato perch&egrave; poco informativo</h3>
				<p>per essere considerato valido il commento deve contenere</p>	
				<div class=\"commento sezione\">
					<form action=\"script_commenti.cgi\" method=\"post\"> 
						<fieldset>
							<legend>commento</legend>
							<input type=\"hidden\" name=\"idC\" value=\"$idC\"></input>
							<input type=\"hidden\" name=\"idV\" value=\"$idV\"></input>
							<input type=\"hidden\" name=\"idUR\" value=\"$idUR\"></input>
							<input type=\"hidden\" name=\"cittaP\" value=\"$cittaP\"></input>
							<input type=\"hidden\" name=\"cittaA\" value=\"$cittaA\"></input>
							<div>
								<label for=\"valutazione\">Valutazione:</label>
								<select id=\"valutazione\" name=\"valutazione\">";
								for(my $i_temp=1; $i_temp<=5; $i_temp++){
									$form_control.="<option value=\"$i_temp\"";
									if ($i_temp==int($valutazione)){
										$form_control.="selected=\"selected\"";
									}
									$form_control.=">$i_temp</option>";
								}
								$form_control.="
								</select>
							</div>
							
							<div class=\"clearer\"></div>
							<div>
								<label for=\"titolo\">Titolo:</label>
								<input type=\"text\" name=\"titolo\" id=\"titolo\">$titolo</input>
							</div>
							<div class=\"clearer\"></div>
							<div>
								<label for=\"testo\">Testo:</label>
								<textarea name=\"testo\" id=\"testo\" rows=\"5\" cols=\"30\">$testoC</textarea>
							</div>
							<div class=\"clearer\"></div>
							<input type=\"hidden\" name=\"action\" value=\"salva\"></input>	
							<div>
								<button type=\"submit\" id=\"salva\" name=\"salva\" value=\"salva\">
										<span>Salva</span>
									</button>
							</div>
							<div class=\"clearer\"></div>
						</fieldset>
					</form>
				</div> <!-- chiudo commento -->
					";
}
else{
	$form_control= "<h3>Commento sul volo $idV da $cittaP a $cittaA</h3>
				<p>Il commento &egrave; stato salvato</p>
				<div class=\"commento\">
					<h2 class=\"titoloC\">$titolo</h2>
					<p class=\"valutazioneC\">valutazione: $valutazione</p> 
					<p class=\"testoC\">$testoC</p>
				</div>
			</div>";
}

print print_content::print($form_control);
print "		</div>"; #chiudo il div main
print print_footer::print();
print "	</body>
</html>";
