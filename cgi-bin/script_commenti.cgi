#!/usr/bin/perl
package commenti;
use strict;
use DateTime;  #utilizzato per validare la data inserita
use Time::Piece;
use CGI::Carp qw(fatalsToBrowser);
use CGI qw(:standard);
use CGI;
#ancora un paio di considerazioni su come far funzionare le form e ok credo 
my $q = new CGI; #parte mia


require "common_functions/print_header.cgi";
#require "common_functions/print_search.cgi"; #inutile: non viene sfruttato in questa pagina.
require "common_functions/print_content.cgi";
require "common_functions/print_footer.cgi";
require "common_functions/Session.cgi";
require "common_functions/check_form.cgi";
require "common_functions/database.cgi";
require "common_functions/menu.cgi";

#INIZIO SUBROUTINEs
save_comm($presente, $c_rif){#deve salvare il commento sul file; due casi: A)il commento è nuovo => lo appendo alla fine del file
					 #B)il commento è vecchio=>devo sostiruire quel pezzo di testo con una nuova stringa, da creare con quel che ho
	($presente, $c_rif)=_@;
	open (comm, "+<file_commenti.txt") or die "could not open file";#leggi e appendi al posto giusto
	if($prensente!=NULL){#presente contiene null se commento non esiste, 1 altrimenti, c_rif è rif. al commento su cui operare 
		while(<comm>){
			my $line=_$;
			if($line=~m/$c_rif->{idC}/){ #dovrebbe iniziare a stampare al punto giusto
				foreach $key (keys %$c_rif){#stampa ogni campo dell'array
				my $value = $c_rif{$key};
				print comm "\n$key => $value\&";
				}			
			print ";";
			}
		}
	} 
	else{
		seek comm,0,2;#vai alla fine del file
		print"commento:";
		foreach $key (keys %$c_rif){#stampa ogni campo dell'array
			my $value = $c_rif{$key};
			print comm "\n$key => $value\&";
		}
		print ";"; 
	}		
	close comm;							
}

del_comm($idC){#subroutine che si prende carico di eliminare il commento SUL FILE contenente idC passato; deve sostituire con stringa vuota tutto quel che è contenito tra Commento X e ; con $idC=parametro passato
	$idC=_@;
	open (comm, "+<file_commenti.txt") or die "could not open file";#apri x lettura e scrittura senza blank del file
	my $del=0;
	while(<comm>){#dovrebbe cancellare, spero che non si limiti ad aprire un buco nel file
		my $line=$_;
		if($line=~m/idC=\$idC/){#cerco match -> cancello NB COSI NON MI DA PROBLEMI X TROVARE LA STRINGA? NON dovrebbe cerace letteralmente "$idC"...
			$del=1;
			print comm "";#prima riga da cancellare
		}
		if(del=1){
			while($line!=~m/idC/){#finchè non arrivo al nuovo commento cancella, visto che nn posso cancella re la linea "commento :" del precedente cancello la corrente
				print comm "";
			} 
		}
	}
	close comm;
}

sub yesorno($action, $idC){
	($action, $idC)=_@;
	if($action=="yes"){
		&del_comm;
		}
}
#FINE SUBROUTINE
#parte iniziale per la corretta visualizzazione della pagina

# NB !!! %form dovrebbe essere inutile xke non viene passato niente mediante il link
#my %form;


#foreach my $p (param()) {
#    $form{$p} = param($p);
    #print "$p = $form{$p}<br>\n";
# 

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
my $testoC= $q->param('testo');
my $action=$q->param('action');
my $form_control="<form action=\"script_commenti.cgi\" method=\"post\"> 
						<fieldset>
							<legend>commento</legend>
							<input type=\"hidden\" name=\"idC\" value=\"$idC\">
							<input type=\"hidden\" name=\"idV\" value=\"$idV\">
							<input type=\"hidden\" name=\"idUR\" value=\"$idUR\">
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
  

if($action=="salva"){
	#il commento non esiste e devo salvarlo => creo un nuovo hash e lo stampo
	#O il commento esiste e devo salvarlo => cerco l'hash con i giusti id e lo modifico	
	if($testoC==""){
        	$error_count=$error_count+1;
       		$testo.="<p>il tuo commento non &grave valido in quanto non fornisce sufficente informazione sul volo che hai effettuato</p>";
        }
        if ($error_count!=0){
        	$testo.= '$form_control';
        }
	my %to_save{
		idC=>$idC,
		idUR=>$idUR,
		idV=>$idV,
		cittaP=>NULL,
		cittaA=>NULL,
		valutazione=>$valutazione,
		titolo=>$titolo,
		testo=>$testoC
	};
	my $presente=NULL;
	if($to_save{idC}!=0){
		$presente=1;
	}
	my $ref_to_save=\%to_save;
	&save_comm($presente, $ref_to_save);
	$testo.= $q->("utente $idUR");
        $testo.= $q->p("volo $idV, valutazione $valutazione, titolo $titolo, testo $testo");
}
else{		
	#il commento esiste e devo eliminarlo, questo va fatto direttamente sul database ma prima controllo che l'autore voglia davvero eliminarlo
	$testo.="<p>vuoi eliminare il commento sul volo $idV?</p>"# dal database troveremo poi altri dati da scrivere x identificare il commento: data ecc
	$form_control="<form method=\"get\" action=\"&yesorno($idC)\">
		<fieldset>
			<input type=\"radio\" name=\"action\" value=\"1\"> Si</input><br>
			<input type=\"radio\" name=\"action\" value=\"0\" checked=\"cheched\"> No</input> 
			</br>
			<input type=\"submit\" value=\"submit\">
		</fieldset>
	</form>";
	$testo.=$form_control;
    $testo.="il commento effettuato dall'utente $idUR sul volo $idV è stato eliminato"
}
$testo.= '</div><!-- chiudo contenitore_sezioni -->	
			<div class="clearer"></div>';

#patre finale
print "		</div>"; #chiudo il div main
print print_footer::print();
print "	</body>
</html>";
