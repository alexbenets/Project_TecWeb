#!/usr/bin/perl

package commenti;
use strict;
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

#pagina per la creazione di nuovi commenti o la modifica/eliminazione
#deve ricevere dei parametri dalla pagina di visualizzazione: idP dal quale ricavare idUR, idV ( e se serve idCommento, datacommento, titolo, contenuto, voto(se esiste, zero altrimenti))
my %form;


foreach my $p (param()) {
    $form{$p} = param($p);
    #print "$p = $form{$p}<br>\n";
}

my $idPrenotazione=int($form{"idP"}); 
my $titolo="Area utente";
my $idUR=gestione_sessione::getParam("id");  
my $idC=0; #se esiste un commento eseguito da idUR si idV=> prendo dal database il valore, altrimenti il valore iniziale è zero e dovroò calcolare il primo valore libero x salvare
my $idV=0;
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
						<li><a href="utente.cgi">Commenti</a></li>
					</ul>
				</div><!-- chiudo secondo menu -->';
my $testo='<div id="contenitore_sezioni"><!-- apro maxi contenitore per le sezioni -->
					
					<div class="sezione" id="S1"><!-- inizio div che contiene titolo e sezione dell\'articolo -->
						<h3>Benvenuto!</h3>
						<p>In questa pagina potrai scrivere, modificare, eliminare commenti che vuoi esprimere sulla tua esperienza di volo con noi.</p>
					</div><!-- chiudo sezione -->
					
					<div id="torna_su">
						<a href="#header">Torna su</a>
					</div>';
#fine di parte copiata che dovrebbe formare la parte comune a tutte le pagine del sito
#i dati di questa dovrebbero essere presi dal database

#INIZIO SUBROUTINES
sub build_comment(commenti_ref){#divide il testo del file in singoli blocchi ciascuno contenete un solo commento
	open(my $comm, 'filecommenti.txt') or die "could not open file";
	my $commenti_ref=@_;
	my @commenti=\@{$commenti_ref};
	my $i=0;
	while(<$comm>){
		my $line=$_;
		chomp($line);
		if ($line=~m/commento:/){
			push(\@{@commenti}, $line);#dovrebbe essere l'alternativa migliore xke CREA esplicitamente il nuovo elemento, e l'array inizia vuoto 
			}
		else 
			{	
				@commenti[$i].=$line;
			}
		#alternativa if($line!=~m/;/){
			#${commenti_ref}[$i].=$line;
		#}
		#else{
			#${commenti}[$i].=$line;
			#$i=$i+1;
		#}
		if($line=~m/;/){
			$i=$i+1;
		}
	close ($comm) or die "could not close";
	return $commenti_ref;
}

sub find_comment{#cerca in @commenti il commento con i dati passati dal main, crea l'oggetto commento attraverso un hash x renderlo + maneggevole e lo ritorna

}

#FINE SUBROUTINES
my $form_comm="<form action=\"script_commenti.cgi\" method=\"post\">  <!--modifica così che passi i dati da utente-->
	<fieldset>
		<legend>commento</legend>
		<input type=\"hidden\" name=\"idC\" value=\"$idC\"> <!--DUBBIO INFAME COSì CONTIENE I DATI CHE DEVE CONTENERE? -->
		<input type=\"hidden\" name=\"idV\" value=\"$idV\">
		<input type=\"hidden\" name=\"idUR\" value=\"$idUR\">
		Valutazione:
		<select name=\"valutazione\">";

my $form_vuota="<form>
	<fieldset action=\"script_commenti.cgi\" method=\"post\">
		<legend>nuovo commento</legend>
		<input type=\"hidden\" name=\"idC\" value=\"0\">
		<input type=\"hidden\" name=\"idV\" value=\"$idV\">
		<input type=\"hidden\" name=\"idUR\" value=\"$idUR\">
		Valutazione:
		<select name=\"valutazione\">
			<option value=\"0\" checked=\"checked\"></option>
			<option value=\"1\">1</option>
			<option value=\"2\">2</option>
			<option value=\"3\">3</option>
			<option value=\"4\">4</option>
			<option value=\"5\">5</option>
		</select>
		</br>
		Titolo:
		<input type=\"text\" name=\"titolo\"></br>
		testo:
		<textarea name=\"testo\" rows=\"5\" col=\"30\"></br>
		<input type=\"submit\" value=\"Salva\">
	</fieldset>
</form>";

if($idUR!=0 and $idV!=0){
	if($idC!=0){
		#esiste un commento effettuato dall'utente su quel volo, uso $form_comm
		$testo.=$form_comm;
		my $i=0;
		my %C_attuale={};#commento che abbia volo e autore corretto !!!
		for(;$i<6; $i++){
			if($i==$C_attuale{"valutazione"}){
				$testo.="<option value=\"$i\" checked=\"checked\">$i</option>";
			}
			else{
				$testo.="<option value=\"$i\">$i</option>";
			}
		}
		$testo.="</select>
					</br>
					<label for=\"titolo\">Titolo:</label>
					<input type=\"text\" name=\"titolo\" id=\"titolo\">".$C_attuale{"titolo"}."</input>
					</br>
					testo:
					<textarea name=\"testo\" rows=\"5\" col=\"30\"></br>
					<input type=\"radio\" name=\"action\" value=\"salva\" checked> Male<br>
				  	<input type=\"radio\" name=\"action\" value=\"elimina\"> Female<br>					
					<input type=\"submit\" value=\"submit\">
				</fieldset>
			</form>";
		}
	}
	else{
		#non esiste alcun commento dell'utente sul volo selezionato, uso $form_vuota
		$testo.=$form_vuota;
	}
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

$testo.= '</div>	
		<div class="clearer"></div>';

print print_content::print($testo);
print "		</div>"; #chiudo il div main
print print_footer::print();
print "	</body>
</html>";


